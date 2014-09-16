import datetime
import os
import sys
import getpass

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.moment import Moment

from werkzeug.security import generate_password_hash

from tracky import app
from tracky.models import Activity
from tracky.database import session, Base

from flask.ext.googlemaps import GoogleMaps

manager = Manager(app)
GoogleMaps(app)
moment = Moment(app)


@manager.command
def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


@manager.command
def seed_activites():

    content = """An Example pre-populated activity entry - Just some notes..."""

    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now() + datetime.timedelta(hours=1)
    duration = str(end_time - start_time)

    for i in range(25):
        entry = Activity(
            title="Test Activity #{}".format(i),
            activity='Running',
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            start_location='5004 Richenbacher Ave Alexandria, VA 22304',
            end_location='5008 Richenbacher Ave Alexandria, VA 22304',
            notes=content,
            calories=100
        )
        session.add(entry)
    session.commit()


@manager.command()
def seed_meals():



class DB(object):
    def __init__(self, metadata):
        self.metadata = metadata

migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    try:
        t = sys.argv[1]
        pass
    except IndexError:
        run()
    manager.run()
