# SI 364
# Winter 2018
# HW 2 - Part 1

# This homework has 3 parts, all of which should be completed inside this file (and a little bit inside the /templates directory).

# Add view functions and any other necessary code to this Flask application code below so that the routes described in the README exist and render the templates they are supposed to (all templates provided are inside the templates/ directory, where they should stay).

# As part of the homework, you may also need to add templates (new .html files) to the templates directory.

#############################
##### IMPORT STATEMENTS #####
#############################
from flask import Flask, request, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, ValidationError
from wtforms.validators import Required
import requests
import json

#####################
##### APP SETUP #####
#####################

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstring'

####################
###### FORMS #######
####################


####################
###### ROUTES ######
####################

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/user/<name>')
def hello_user(name):
    return '<h1>Hello {0}<h1>'.format(name)


class artistForm(FlaskForm):
    artist = StringField('Enter artist', validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/artistform')
def artist_form():
    simpleForm = artistForm()
    return render_template('artistform.html', form=simpleForm)


@app.route('/artistinfo', methods=['GET', 'POST'])
def artist_info():
    form = artistForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        params = {}
        params['term'] = form.artist.data
        response = requests.get(
            'https://itunes.apple.com/search', params=params)
        results = json.loads(response.text)['results']
        return render_template('artist_info.html', objects=results)
    flash('All fields are required!')
    # this redirects you to itunes_form if there are errors
    return redirect(url_for('artist_form'))


'''
@app.route('/artistlinks')
def links():
    return render_template('artist_links.html')


@app.route('/specific/song/<artist_name')
def specific():
    return render_template('specific_artist.html')


@app.route('/album_entry')
@app.route('/album_result')
'''
if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
