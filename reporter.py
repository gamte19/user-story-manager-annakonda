from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for
import json

with open('connection_data.json') as json_data:
    data = json.load(json_data)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@localhost/story'.format(data['db_name'], data['passwd'])
app.debug = True
db = SQLAlchemy(app)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_title = db.Column(db.String())
    user_story = db.Column(db.String())
    acceptance_criteria = db.Column(db.String())
    business_value = db.Column(db.Integer())
    estimation = db.Column(db.Float())
    status = db.Column(db.String())

    def __init__(self, story_title, user_story, acceptance_criteria, business_value, estimation, status):
        self.story_title = story_title
        self.user_story = user_story
        self.acceptance_criteria = acceptance_criteria
        self.business_value = business_value
        self.estimation = estimation
        self.status = status


@app.route('/')
@app.route('/list', methods=['GET'])
def list():
    story = Story.query.all()
    return render_template('list.html', story=story)


@app.route('/post_story', methods=['GET'])
def create_story():
    return render_template('form.html', story='', action=url_for('post_story'))


@app.route('/post_story', methods=['POST'])
def post_story():
    story = Story(request.form['story_title'], request.form['user_story'], request.form['acceptance_criteria'],
                  request.form['business_value'], request.form['estimation'], request.form['status'])
    db.session.add(story)
    db.session.commit()
    return redirect(url_for('list'))


@app.route('/del/<story_id>', methods=['GET'])
def dell(story_id):
    Story.query.filter(Story.id == story_id).delete()
    db.session.commit()
    return redirect(url_for('list'))


@app.route('/post_story/<story_id>', methods=['GET'])
def update_story(story_id):
    story = Story.query.filter(Story.id == story_id).first()
    print(story)
    return render_template('form.html', story=story, action=url_for('post_update', story_id=story_id))


@app.route('/update_story/<story_id>', methods=['POST'])
def post_update(story_id):
    Story.query.filter(Story.id == story_id).update(dict(story_title=request.form['story_title'],
                                                    user_story=request.form['user_story'],
                                                    acceptance_criteria=request.form['acceptance_criteria'],
                                                    business_value=request.form['business_value'],
                                                    estimation=request.form['estimation'],
                                                    status=request.form['status']))
    db.session.commit()
    return redirect(url_for('list'))


if __name__ == "__main__":
    app.run()
    db.create_all()
