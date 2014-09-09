import requests

from datetime import datetime

from flask import render_template, request, flash, redirect, url_for
from forms import NewActivity, NewMeal

from tracky import app
from database import session
from models import Activity, Meal

from flask.ext.googlemaps import Map


@app.route('/view_map/<int:activity_id>')
def gmap(activity_id=0):

    activity = session.query(Activity).get(activity_id)

    start_location = get_cords(activity.start_location)
    end_location = get_cords(activity.end_location)

    start_map = Map(
        style="height:500px;width:500px;margin:0;",
        identifier="view-side",
        lat=start_location['lat'],
        lng=start_location['lng'],

        markers=[(start_location['lat'], start_location['lng'])]
    )

    end_map = Map(
        style="height:500px;width:500px;margin:0;",
        identifier="view-side",
        lat=end_location['lat'],
        lng=end_location['lng'],

        markers=[(end_location['lat'], end_location['lng'])]
    )

    start_end_map = Map(
        style="height:500px;width:500px;margin:0;",
        identifier="view-side",
        lat=start_location['lat'],
        lng=start_location['lng'],

        markers=[(start_location['lat'], start_location['lng']),
                 (end_location['lat'], end_location['lng'])]
    )

    maps = {'start_map': start_map,
            'end_map': end_map,
            'start_end_map': start_end_map
    }

    return render_template('mapit.html', maps=maps)


def get_cords(location):

    url = 'http://maps.google.com/maps/api/geocode/json?'

    params = {
        'address': location,
        'sensor': False
    }

    r = requests.get(url, params=params)

    return r.json()['results'][0]['geometry']['location']


@app.route("/")
def entries():

    activities = session.query(Activity)
    activities = activities.order_by(Activity.entry_date.desc()).limit(5)
    activities = activities.all()

    return render_template("activities.html",
                           activities=activities
    )


@app.route("/meals")
def meals():

    meals = session.query(Meal)
    meals = meals.order_by(Meal.entry_date.desc()).limit(5)
    meals = meals.all()

    return render_template("meals.html",
                           meals=meals
    )


@app.route('/activity/<int:activity_id>')
def view_activity(activity_id=0):
    activity = session.query(Activity).get(activity_id)

    start_location = get_cords(activity.start_location)
    end_location = get_cords(activity.end_location)

    print start_location['lat'], start_location['lng']
    print end_location

    return render_template('activity.html', activity=activity)


@app.route('/activity/add', methods=['GET', 'POST'])
def add_activity():
    form = NewActivity()

    if request.method == 'POST':
        try:
            start_time = datetime.strptime(str(form.start_time.data), '%b %d %Y %I:%M%p')
            end_time = datetime.strptime(str(form.end_time.data), '%b %d %Y %I:%M%p')
            duration = str(end_time - start_time)

            activity = Activity(title=form.title.data,
                                activity=form.activity.data,
                                start_time=start_time,
                                end_time=end_time,
                                duration=duration,
                                start_location=form.start_location.data,
                                end_location=form.end_location.data,
                                notes=form.notes.data,
                                calories=form.calories.data
                                )

            session.add(activity)
            session.commit()
        except ValueError:
            flash('Please enter date in correct format')
            return render_template('add_activity.html', form=form)

        flash('Acvitity Added!')

        return redirect(url_for('entries'))

    return render_template('add_activity.html', form=form)


@app.route('/meal/add', methods=['GET', 'POST'])
def add_meal():
    form = NewMeal()

    if request.method == 'POST':

        meal = Meal(meal=form.meal.data,
                    contents=form.contents.data,
                    calories=form.calories.data
        )

        session.add(meal)
        session.commit()

        flash('Meal Added!')

        return redirect(url_for('meals'))

    return render_template('add_meal.html', form=form)

@app.route('/activity/<int:activity_id>/edit', methods=['GET', 'POST'])
def edit_activity(activity_id=None):

    activity = session.query(Activity).get(activity_id)
    form = NewActivity(obj=activity)

    if request.method == 'POST':
        try:
            start_time = datetime.strptime(str(form.start_time.data), '%b %d %Y %I:%M%p')
            end_time = datetime.strptime(str(form.end_time.data), '%b %d %Y %I:%M%p')
            duration = str(activity.end_time - activity.start_time)

            activity.title = form.title.data
            activity.activity = form.activity.data
            activity.start_time = start_time
            activity.end_time = end_time
            activity.duration = duration
            activity.start_location = form.start_location.data
            activity.end_location = form.end_location.data
            activity.notes = form.notes.data

            session.commit()
        except ValueError as e:
            print e
            flash('Please enter date in correct format')
            return render_template('edit_activity.html', form=form)

        flash('Acvitity Edited!')

        return redirect(url_for('entries'))
    return render_template('edit_activity.html', form=form)