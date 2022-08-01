from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import datetime

config = {
  "apiKey": "AIzaSyAuw7ZoeAE7YKkDuWbhjJ-3KEG8dPnIqME",
  "authDomain": "first-firebase-web-32cfb.firebaseapp.com",
  "projectId": "first-firebase-web-32cfb",
  "storageBucket": "first-firebase-web-32cfb.appspot.com",
  "messagingSenderId": "690175495951",
  "appId": "1:690175495951:web:14a2b43b24cccb0b10787a",
  "measurementId": "G-XNW9C2B0WT",
  "databaseURL": "https://first-firebase-web-32cfb-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)

            return redirect(url_for('add_tweet'))
        except:
           error = "Authentication failed"
           return error
    else: 
        return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['name']
        username = request.form['user']
        Bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            user = {"name": full_name, "email": email}
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "signing up failed"
            return error
    else:
        return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    x = datetime.datetime.now()
    if request.method == 'POST':
        try:
            tweet = {
            "title": request.form['title'], 
            "text": request.form['text'], 
            "uid": login_session['user']['localId'],
            "date_time": x}
            db.child("Tweets").push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "Authentication failed"
            return error
    return render_template("add_tweet.html")

@app.route('/signout', methods=['GET', 'POST'])
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets = tweets)


if __name__ == '__main__':
    app.run(debug=True)