from flask import render_template

from tracky import app
from database import session
from models import Activity


@app.route("/")
def entries():

    activities = session.query(Activity)
    activities = activities.order_by(Activity.entry_date.desc())
    activities = activities.all()

    print activities

    return render_template("activities.html",
                           activities=activities
    )


