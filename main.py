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


@app.route("/")
def index():
    response = make_response(render_template("index.html"))
    return response
# render_template()


# @app.route("/posts")
# def posts():
#     return render_template("posts.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    message_k = request.cookies.get("message_k")
    return render_template("about.html", name=message_k, messages=messages)
    # return render_template("about.html", messages=messages)


# @app.route('/getcookie')
# def getcookie():
#     message_name_cookie = request.cookies.get("user_name")
#
#     return message_name_cookie


@app.route("/add_message", methods=["GET", "POST"])
def add_message():
    if request.method == "GET":
        message_k = request.cookies.get("message_k")
        return render_template("about.html", name=message_k)
    elif request.method == "POST":
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
        response.set_cookie("message_k", message_name, max_age=60*10)
        return response


@app.route("/posts", methods=['GET', 'POST'])
def posts():
    """
    Skolas mājas darba šablons
    :return:
    """
    if request.method == "GET":
        user_name = request.cookies.get("user_name")
        return render_template("posts.html", name=user_name)
    elif request.method == "POST":
        contact_name = request.form.get("contact-name")
        contact_email = request.form.get("contact-email")
        contact_message = request.form.get("contact-message")
        user_name = request.cookies.get("user_name")
        response = make_response(render_template("success.html"))
        response.set_cookie("user_name", contact_name)

        return response


# Va fails tiek izpildīts pa tiešo vai kāda cita faila ...
if __name__ == "__main__":
    # app.run()  # Palaiž vebservera ...
    app.run(debug=True) # Palaiž vebservera ...


