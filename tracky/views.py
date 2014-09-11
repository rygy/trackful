import requests

from datetime import datetime, timedelta

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

    markers = [(start_location['lat'], start_location['lng']),
               (end_location['lat'], end_location['lng'])]

    try:
        for coord in activity.waypoints.split():
            markers.append((get_cords(coord)['lat'], get_cords(coord)['lng']))
    except AttributeError:
        pass

    #print markers

    start_end_map = Map(
        style="height:500px;width:500px;margin:0;",
        identifier="view-side",
        lat=start_location['lat'],
        lng=start_location['lng'],

        markers=markers
    )

    maps = {'start_map': start_map,
            'end_map': end_map,
            'start_end_map': start_end_map
    }

    print dir(maps['start_map'])
    print maps['start_end_map'].identifier
    print maps['start_end_map'].center[0]
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


@app.route('/meals/show/<string:meal_type>')
def view_by_meal(meal_type=None):
    meals = session.query(Meal).filter(Meal.meal == meal_type)

    meals = meals.order_by(Meal.entry_date.desc())
    meals = meals.all()

    return render_template('meals.html',
                           meals=meals
    )


@app.route('/activity/<int:activity_id>')
def view_activity(activity_id=0):
    activity = session.query(Activity).get(activity_id)

    current = datetime.utcnow()
    past_24_hours = current - timedelta(hours=24)

    activity2 = session.query(Activity).filter(Activity.entry_date.between(current, past_24_hours))

    print activity2
    print activity2.all()

    return render_template('activity.html', activity=activity)


@app.route('/meal/<int:meal_id>')
def view_meal(meal_id=0):
    meal = session.query(Meal).get(meal_id)

    return render_template('meal.html', meal=meal)

@app.route('/activity/add', methods=['GET', 'POST'])
def add_activity():
    form = NewActivity()

    if request.method == 'POST':
        try:
            start_time = datetime.strptime(str(form.start_time.data), '%b %d %Y %I:%M%p')
            end_time = datetime.strptime(str(form.end_time.data), '%b %d %Y %I:%M%p')
            duration = str(end_time - start_time)

            if form.waypoints.data:
                waypoints = form.waypoints.data
            else:
                waypoints = None

            activity = Activity(title=form.title.data,
                                activity=form.activity.data,
                                start_time=start_time,
                                end_time=end_time,
                                duration=duration,
                                start_location=form.start_location.data,
                                end_location=form.end_location.data,
                                notes=form.notes.data,
                                calories=form.calories.data,
                                waypoints=waypoints
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
            activity.calories = form.calories.data

            if form.waypoints.data:
                activity.waypoints = form.waypoints.data

            session.commit()
        except ValueError as e:
            print e
            flash('Please enter date in correct format')
            return render_template('edit_activity.html', form=form)

        flash('Acvitity Edited!')

        return redirect(url_for('entries'))
    return render_template('edit_activity.html', form=form)


@app.route('/meal/<int:meal_id>/edit', methods=['GET', 'POST'])
def edit_meal(meal_id=None):

    meal = session.query(Meal).get(meal_id)
    form = NewMeal(obj=meal)

    if request.method == 'POST':

        meal.meal = form.meal.data,
        meal.contents = form.contents.data
        meal.calories = form.calories.data

        session.commit()

        flash('Meal Edited!')

        return redirect(url_for('meals'))

    return render_template('edit_meal.html', form=form)


@app.route('/meal/<int:meal_id>/delete', methods=['GET', 'POST'])
def delete_meal(meal_id=None):

    meal = session.query(Meal).get(meal_id)

    session.delete(meal)

    flash('Meal Deleted!')

    return redirect(url_for('meals'))


@app.route('/activity/<int:activity_id>/delete', methods=['GET', 'POST'])
def delete_activity(activity_id=None):

    activity = session.query(Activity).get(activity_id)

    session.delete(activity)

    flash('Activity Deleted!')

    return redirect(url_for('entries'))


@app.route('/test_date')
def test_date():
    return render_template('datetime.html')