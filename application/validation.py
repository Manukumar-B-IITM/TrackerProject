from sqlalchemy import true
from werkzeug.exceptions import HTTPException
from flask import make_response, abort
import json


class SchemaValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(data), status_code)


class BusinessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        data = {"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(data), status_code)


class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response("", status_code)


def validateTrackerData(tdata):
    # Validate Tracker data
    if tdata["name"] is None or tdata["name"] == "":
        abort(400)

    return True


def validateTrackerLogData(tdata):
    # Validate Tracker data
    return True
