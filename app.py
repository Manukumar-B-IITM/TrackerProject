import enum
import io

# import re
import base64
from datetime import datetime, timedelta
from math import remainder

# import humanize
import os
from flask import Flask
from sqlalchemy import Numeric, true
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
import logging
import matplotlib.pyplot as plt
import numpy as np

# from flask import current_app as app
from flask import request, url_for
from flask import render_template, redirect, abort
from application.models import Tracker, Activity
import application.validation as validation


logging.basicConfig(
    filename="debug.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


app = None


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv("ENV", "development") == "production":
        app.logger.info("Currently no production config is setup.")
        raise Exception("Currently no production config is setup.")
    else:
        app.logger.info("Staring Local Development.")
        print("Staring Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    app.logger.info("App setup complete")
    print("App setup complete")
    return app


app = create_app()

# Import all the controllers so they are loaded
# from application.controllers.tracker_controllers import *


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/", methods=["GET"])
def home():
    if request.method == "GET":
        trackers, lastTimestamps = getTrackers()
        return (
            render_template(
                "home.html", trackers=trackers, lastTimestamps=lastTimestamps
            ),
            200,
        )


# Tracker endpoints
# @app.route("/tracker/<tid>", methods=["GET"])
# def trackerInfo(tid):
#     tracker = Tracker.query.filter(Tracker.id == tid).first()
#     return render_template("tracker_overview.html", tracker = tracker)


@app.route("/tracker/create", methods=["GET", "POST"])
def create_tracker():
    if request.method == "GET":
        return render_template("tracker_create.html"), 200
    elif request.method == "POST":
        if createTracker(request.form) == False:
            abort(500)
        return redirect(url_for("home"))


@app.route("/tracker/<int:tid>/update", methods=["GET", "POST"])
def update_tracker(tid):
    if request.method == "GET":
        tracker = Tracker.query.filter(Tracker.id == tid).first()
        return render_template("tracker_update.html", tracker=tracker)
    elif request.method == "POST":
        if updateTracker(request.form, tid) == False:
            abort(500)
        return redirect(url_for("home"))


@app.route("/tracker/<int:tid>/delete")
def delete_tracker(tid):
    if request.method == "GET":
        if deleteTracker(tid):
            return redirect(url_for("home"))


@app.after_request
def after_request(response):
    header = response.headers
    header["Access-Control-Allow-Origin"] = "*"
    return response


@app.route("/tracker/<int:tid>/log", methods=["GET", "POST"])
def activity_log(tid):
    if request.method == "GET":
        return render_template("log_create.html", tracker=getTracker(tid)), 200
    elif request.method == "POST":
        if create_log(request.form, tid):
            return redirect(url_for("home"))
        abort(400)


@app.route("/tracker/<int:tid>/overview", methods=["GET"])
def tracker_overview(tid):
    if request.method == "GET":
        tracker, activities = getTrackerData(tid)
        # prepareCharts(tracker, activities)
        # getbase64LineChartsImg(activities)
        return render_template(
            "tracker_overview.html",
            tracker=tracker,
            activities=activities,
            # imgURL=url_for("static", filename="trend.png"),
            base64Img=getBase64ImgStr(tracker, activities),
        )


@app.route("/activity/<int:aid>/update", methods=["GET", "POST"])
def update_activity(aid):
    if request.method == "GET":
        activity = getActivity(aid)
        return render_template(
            "log_update.html",
            activity=activity,
            tracker=getTracker(activity.tracker_id),
        )
    elif request.method == "POST":
        if updateActivity(request.form, aid) == False:
            abort(500)
        return redirect(url_for("home"))


@app.route("/activity/<int:aid>/delete")
def delete_activity(aid):
    if request.method == "GET":
        if deleteActivity(aid):
            return redirect(url_for("home"))


###################################################################
# Tracker Controller
###################################################################


def getTrackers():
    trackers = db.session.query(Tracker).all()
    lastTimeStamps = {}
    for t in trackers:
        activity = (
            db.session.query(Activity)
            .filter(Activity.tracker_id == t.id)
            .order_by(Activity.timestamp.desc())
            .first()
        )
        if activity is None:
            lastTimeStamps[t.id] = "No Logs yet"
        else:
            lastTimeStamps[t.id] = convertToNaturalday(activity.timestamp)

    return trackers, lastTimeStamps


def createTracker(data):
    # try:
    if validateTrackerData(data):
        tracker = Tracker(
            name=data["name"],
            description=data["desc"],
            type=data["t_type"],
            settings=data["settings"],
            user_id=1,  # TODO Hardcoded to one user
        )
        db.session.add(tracker)
        db.session.commit()
        return True
    return False


# except:
#     db.session.rollback()
#     return False


def updateTracker(data, tid):
    try:
        if validation.validateTrackerData(data):
            tracker = db.session.query(Tracker).filter(Tracker.id == tid).first()
            if tracker != None:
                tracker.name = data["name"]
                tracker.description = data["desc"]
                db.session.flush()
                db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
        return False


def deleteTracker(tid):
    try:
        tracker = Tracker.query.filter(Tracker.id == tid).first()
        if tracker is not None:
            db.session.delete(tracker)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
        return False


def getTracker(tid):
    tracker = Tracker.query.filter(Tracker.id == tid).first()
    return tracker


def getTrackerData(tid):
    tracker = getTracker(tid)
    activities = (
        db.session.query(Activity)
        .filter(Activity.tracker_id == tid)
        .order_by(Activity.timestamp)
        .all()
    )
    return tracker, activities


#####################################################################
# Activity Controller                                               #
#####################################################################


def create_log(data, tid):
    # try:
    if validateTrackerLogData(data, tid):
        # TODO handle the timestamp better with UTC timestamps
        activity = Activity(
            timestamp=getPythonTime(data["timestamp"]),
            value=",".join(request.form.getlist("tvalue")),  # joining by ','
            note=data["note"],
            tracker_id=tid,
        )
        db.session.add(activity)
        db.session.commit()
        return True
    return False


# except:
#     db.session.rollback()
#     return False


def updateActivity(data, aid):
    # try:
    if validation.validateTrackerLogData(data):
        activity = db.session.query(Activity).filter(Activity.id == aid).first()
        if activity != None:

            activity.timestamp = getPythonTime(data["timestamp"])
            activity.value = ",".join(request.form.getlist("tvalue"))
            activity.note = data["note"]

            db.session.flush()
            db.session.commit()
        return True
    return False


# except:
#     db.session.rollback()
#     return False


def deleteActivity(aid):
    try:
        activity = Activity.query.filter(Activity.id == aid).first()
        if activity is not None:
            db.session.delete(activity)
            db.session.commit()
            return True
        return False
    except:
        db.session.rollback()
        return False


def getActivity(aid):
    activity = Activity.query.filter(Activity.id == aid).first()
    return activity


##########################################################################
# UTILS
##########################################################################
def getPythonTime(tp):
    return datetime(
        int(tp[0:4]), int(tp[5:7]), int(tp[8:10]), int(tp[11:13]), int(tp[14:16])
    )


def getBase64ImgStr(tracker, activities):
    if len(activities) > 0:
        plt.figure()
        if tracker.type == TRACKERTYPE.Numeric.value:
            return getBase64LineChartImg(activities)
        elif tracker.type == TRACKERTYPE.Multi.value:
            return getBase64PieChart(activities)
        elif tracker.type == TRACKERTYPE.Time_Duration.value:
            return getBase64BarChart(activities)
        elif tracker.type == TRACKERTYPE.Bool.value:
            return getBase64BoolBarChart(activities)


def getBase64LineChartImg(activities):

    x = []
    y = []

    for a in activities:
        x.append(a.timestamp)
        y.append(float(a.value))

    # naming the x axis
    plt.xlabel("Time")
    # naming the y axis
    plt.ylabel("Values")
    plt.xticks(rotation=45)
    plt.yticks(np.arange(min(y), max(y) + 1, (max(y) + 1 - min(y)) / 10))

    plt.title("Trend over time")
    plt.tight_layout()
    plt.plot(x, y, marker="o")

    return getBase64Img()


def getBase64PieChart(activities):

    y = {}
    total = 0
    for a in activities:
        for opt in a.value.split(","):
            total += 1
            if opt not in y.keys():
                y[opt] = 0
            y[opt] += 1

    perc = [y[k] / total for k in y.keys()]
    keys = y.keys()

    plt.pie(perc, labels=keys)

    return getBase64Img()


def getBase64BarChart(activities):
    xTimeStamp = []
    minutesY = []

    for a in activities:
        xTimeStamp.append(a.timestamp)
        timeValues = a.value.split(",")
        minutesY.append(
            (int(timeValues[0]) * 60) + int(timeValues[1]) + int(timeValues[2]) / 60
        )

    # naming the x axis
    plt.xlabel("Time")
    # naming the y axis
    plt.ylabel("Minutes")

    plt.xticks(rotation=45)
    plt.yticks(
        np.arange(
            min(minutesY), max(minutesY) + 1, (max(minutesY) + 1 - min(minutesY)) / 10
        )
    )

    plt.title("Trend over time")
    plt.tight_layout()
    plt.plot(xTimeStamp, minutesY, marker="o")

    return getBase64Img()


def getBase64BoolBarChart(activities):
    x = ["Yes", "No"]
    yesCount = 0
    NoCount = 0

    for a in activities:
        if a.value == "1":
            yesCount += 1
        else:
            NoCount += 1
    plt.bar(x, [yesCount, NoCount])

    return getBase64Img()


def getBase64Img():
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format="jpg")
    my_stringIObytes.seek(0)
    imgStr = base64.b64encode(my_stringIObytes.read())

    return imgStr.decode()


# ENUMS
# TRACKERTYPE = {"numeric": 1, "multi": 2, "time_duration": 3, "bool": 4}
class TRACKERTYPE(enum.Enum):
    Numeric = 1
    Multi = 2
    Time_Duration = 3
    Bool = 4


# TRACKERTYPE.NUMER


#########################################################################
# Errors
#########################################################################


@app.errorhandler(400)
def bad_request(e):
    return render_template("400.html", msg=e.description), 400


@app.errorhandler(500)
def internal_error(e):
    return render_template("500.html"), 500


def validateTrackerData(tdata):
    # Validate Tracker data
    if tdata["name"] is None or tdata["name"] == "":
        abort(400, "Tracker Name is mandatory")

    if not tdata["name"].isalpha():
        abort(400, "Only alphabets are allowed for Tracker Name")

    if tdata["t_type"] is None or tdata["t_type"] == "":
        abort(400, "Tracker Type is mandatory")

    if tdata["t_type"] not in ["1", "2", "3", "4"]:
        abort(400, "Invalid tracker type")

    if tdata["t_type"] == "2" and (
        tdata["settings"] is None or tdata["settings"] == ""
    ):
        abort(
            400,
            "For multichoice tracker, setting field is mandatory. Choices should be entered as comma separated values.",
        )

    return True


def validateTrackerLogData(tdata, tid):
    # Validate Tracker data
    if tdata["timestamp"] is None or tdata["timestamp"] == "":
        abort(400, "Tracker log timestamp is mandatory.")
    try:
        getPythonTime(tdata["timestamp"])
    except:
        abort(400, "Tracker log timestamp is invalid/malformed.")

    tracker = db.session.query(Tracker).filter(Tracker.id == tid).first()

    if tracker is None:
        abort(400, "Tracker id is not valid.")

    if tracker.type == 1:
        try:
            float(tdata["value"])
        except:
            abort(400, "Log value should be Numeric. ex: 10, 2.5 ...")

    if tracker.type == 2:
        possibleValues = tracker.settings.split(",")
        for op in request.form.getlist("tvalue"):
            if op not in possibleValues:
                abort(
                    400,
                    "Invalid option for the Multi tracker. Allowed values are "
                    + possibleValues,
                )

    if tracker.type == 3:
        timeValues = request.form.getlist("tvalue")
        for t in timeValues:
            if not t.isdigit():
                abort(400, "Time duration values are not correct")

    if tracker.type == 4 and tdata["tvalue"] not in ["1", "0"]:
        abort(400, "Only yes/no allowed")

    return True


def convertToNaturalday(dt):
    count = (datetime.now() - dt).days
    if count == 0:
        return "Today"
    elif count == 1:
        return "Yesterday"
    elif count > 1 and count < 31:
        return count + " day(s) ago"
    elif count > 30 and count < 366:
        return (
            "" + str(int(count / 30)) + " Month(s) " + str(count % 30) + " Day(s) ago"
        )
    elif count > 365:
        noOfYears = str(int(count / 365))
        remaining = str(count % 365)
        return "" + noOfYears + " Year(s) " + remaining + " Day(s) ago"

    return (datetime.now() - dt).days


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=False)
