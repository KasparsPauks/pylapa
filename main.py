# Lai apstrādātu ziņojumus izmantos masīvus
from collections import namedtuple
import datetime, time
from flask import Flask, render_template, request, url_for, redirect,\
    make_response
# from wtforms import StringField, PasswordField, validators, Form, BooleanField
# from wtforms.validators import InputRequired, Email


app = Flask(__name__)


Message = namedtuple('Message', 'message_name, message_email, message_text, message_time,'
                                'message_time_stamp, message_ErrorMessage')
messages = []


@app.route("/", methods=["GET"])
def index():
    message_name_cookie = request.cookies.get("message_name_cookie")
    response = make_response(render_template("index.html"))
    return response
# render_template()

@app.route("/posts")
def posts():
    return render_template("posts.html")


@app.route("/about",  methods=["POST", "GET"])
def about():
    return render_template("about.html", messages=messages)


@app.route('/getcookie')
def getcookie():
    message_name_cookie = request.cookies.get("message_name_cookie")

    return message_name_cookie

@app.route("/add_message", methods=["POST", "GET"])
def add_message():
    message_name_cookies = request.cookies.get('message_name_cookies')

    message_name = request.form["message_name"]
    message_ErrorMessage = ''
    if message_name == '':
        message_ErrorMessage = 'Jāaizpilda lauki'
    message_email = request.form["message_email"]
    if message_email == '':
        message_ErrorMessage = 'Jāaizpilda lauki'
    message_text = request.form["message_text"]
    if message_text == '':
        message_ErrorMessage = 'Jāaizpilda lauki'
    message_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message_time_stamp = int(time.time())
    messages.append(Message(message_name, message_email, message_text, message_time,
                            message_time_stamp, message_ErrorMessage))
    response = make_response(redirect(url_for('about')))
    response.set_cookie("message_name_cookie", message_name, max_age=60*10)


    return response




# Va fails tiek izpildīts pa tiešo vai kāda cita faila ...
if __name__ == "__main__":
    app.run()  # Palaiž vebservera ...
    # app.run(debug=True) # Palaiž vebservera ...
