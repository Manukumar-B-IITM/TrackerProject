from flask import current_app as app
from flask import request, url_for
from flask import render_template, redirect, abort
from application.models import Tracker, Activity


# @app.route("/", methods=["GET"])
# def home():
#     if request.method == "GET":
#         return render_template("home.html"),200
        

# # Tracker endpoints
# # @app.route("/tracker/<tid>", methods=["GET"])
# # def trackerInfo(tid):
# #     tracker = Tracker.query.filter(Tracker.id == tid).first()
# #     return render_template("tracker_overview.html", tracker = tracker)

# @app.route("/tracker/create", methods=["GET", "POST"])
# def create_tracker():
#     if request.method == "GET":
#         return render_template("create_tracker.html"), 200
#     elif request.method == "POST":
#         if createTracker(request.form) == False:
#             abort(500)
#         redirect(url_for("home"))

# @app.route("/tracker/<tid>/overview", methods=["GET"])
# def tracker_overview(tid):
#     tracker = Tracker.query.filter(Tracker.id == tid).first()
#     activities = Activity.query.filter(Activity.tracker_id == tid)
#     return render_template("tracker_overview.html", tracker = tracker, activities = activities)

# @app.route("/tracker/<tid>/update", methods=["GET", "POST"])
# def update_tracker(tid):
#     if request.method == "GET":
#         tracker = Tracker.query.filter(Tracker.id == tid).first()
#         return render_template("tracker_update.html", tracker = tracker)
#     elif request.method == "POST":
#         if updateTracker(request.form) == False:
#             abort(500)
#         redirect(url_for("home"))


# @app.after_request
# def after_request(response):
#     header = response.headers
#     header["Access-Control-Allow-Origin"] = "*"
#     return response

# Create Tracker 
# def createTracker(data):
  
#     return False

# def updateTracker(data):
#     return False

