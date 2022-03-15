from flask import current_app as app

@app.errorhandler(400)
def student_exist(e):
  return 400
    # return render_template('student_exist.html'), 400

@app.errorhandler(500)
def something_wrong(e):
  return 500
    # return render_template('something_wrong.html'), 500
