from flask_wtf import Form
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired


class NewActivity(Form):
    title = StringField('Activity Title', validators=[DataRequired()])
    activity = SelectField('Activity Type', choices=[('Sailing', 'Sailing'),
        ('Running', 'Running'),
        ('Cycling', 'Cycling'),
        ('Walking', 'Walking')],
                           validators=[DataRequired()])
    start_time = StringField('Starting Date / Time', description='Ex: Jun 4 2014 5:23PM', validators=[DataRequired()])
    end_time = StringField('Ending Date / Time', description='Ex: Jun 4 2014 5:23PM', validators=[DataRequired()])
    start_location = StringField('Starting Location', validators=[DataRequired()])
    end_location = StringField('Ending Location', validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])
    calories = StringField('Calories Burned')
    date = StringField('Entry Date', description='Ex: Jun 4 2014 5:23PM - Defaults to now.')
    waypoints = StringField('Additional Waypoints')


class NewMeal(Form):
    meal = SelectField('Meal', choices=[('Breakfast', 'Breakfast'),
                                        ('Lunch', 'Lunch'),
                                        ('Brunch', 'Brunch'),
                                        ('Dinner', 'Dinner'),
                                        ('Linner', 'Linner'),
                                        ('Other', 'Other')])

    contents = StringField('Meal Contents')
    calories = StringField('Total Calories')
