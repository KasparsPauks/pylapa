# -*- coding: utf-8 -*-
# Lai apstrādātu ziņojumus izmantos masīvus
from collections import namedtuple
import datetime, time
from flask import Flask, render_template, request, url_for, redirect,\
    make_response, flash
from flask import session







from tinydb import TinyDB, Query
# No jaunizveidotā modeļa importējam jauno lietotāja klasi
from models import User
from models import LoginForm
from config import Config  # Vieta konfigurācijām
app = Flask(__name__)


app.config.from_object(Config)




Message = namedtuple('Message', 'message_name, message_email, message_text, message_time,'
                                'message_time_stamp, message_error')
messages = []

# Flask WFT autorizēšanās metode, kas prasa definēt slepeno atslēgu
@app.route('/logins', methods=["GET", "POST"])
def logins():
    # session.clear()
    form = LoginForm()



    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))

        return render_template('index.html')
    return render_template('logins.html', title='Sign In', form=form)


@app.route("/", methods=["GET", "POST"])
def index():
    # loginname = request.cookies.get("loginname")
    # userdata = User.fetch_one(query=["name", "==", loginname])
    return render_template("index.html")


@app.route("/about", methods=["GET", "POST"])
def about():
    message_k = request.cookies.get("message_k")
    return render_template("about.html", name=message_k, messages=messages)


@app.route("/add_message", methods=["GET", "POST"])
def add_message():
    if request.method == "GET":
        message_k = request.cookies.get("message_k")
        return render_template("about.html", name=message_k)
    elif request.method == "POST":
        message_name = request.form["message_name"]
        message_error = ''
        if message_name == '':
            message_error = 'Jāaizpilda lauki'
        message_email = request.form["message_email"]
        if message_email == '':
            message_error = 'Jāaizpilda lauki'
        message_text = request.form["message_text"]
        if message_text == '':
            message_error = 'Jāaizpilda lauki'
        message_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_time_stamp = int(time.time())
        messages.append(Message(message_name, message_email, message_text, message_time,
                                message_time_stamp, message_error))
        response = make_response(redirect(url_for('about')))
        response.set_cookie("message_k", message_name, max_age=60*10)
        return response


@app.route("/posts", methods=['GET', 'POST'])
def posts():
    """
    Funkcija, kas skatā pievieno klāt lietotāja atstāto ziņu.
    :return: response #  ir atsaucīga lapas daļa, kurai tiek nodoti mainīgie contact_name un uzstādītas "kūkas"
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
        flash('Your post is now live!')

        return response


@app.route("/loginform", methods=['POST'])
def loginform():
    # Iegūstam datus no reģistrācijas fomas
    email = request.form.get("InputEmail_login").lower()
    username = request.form.get("InputUserName_login").lower()
    # if username != '':
    #     session['username'] = request.form.get("InputUserName_login").lower()
    name = request.form.get("InputName_login").title()
    surname = request.form.get("InputSurName_login").title()
    date_created = datetime.datetime.now().strftime("%d.%m.%Y | %H:%M:%S")
    date_created_by_unix = int(time.time())
    # Tiek izveidots objekts user, kurš satur sevī mainīgos lietotājvārdu un paroli
    # Saglabā lietotāju datubāzē
    user = User(name=name, email=email, user_name=username, date_created=date_created,
                date_created_by_unix=date_created_by_unix, surname=surname, user_rights=None)
    user.create()
    response = make_response(redirect(url_for("login")))
    response.set_cookie("loginname", username)
    return response


@app.route("/userlist")
def userlist():
    loginname = request.cookies.get("loginname")
    if loginname == 'trakaisaziskaspars':
        userdata = User.fetch_one(query=["name", "==", loginname])
        totalList = User.fetch()
        return render_template("userlist.html", loginname=loginname, userdata=userdata, totalList=totalList)
    return render_template('index.html')


@app.route("/userlist2")
def userlist2():


    totalList = User.fetch()
    for users in totalList:
        print(users.name)
        print(users.email)
        print(users.surname)
        print(users.user_name)
        print(users.date_created)
        print(str(users.date_created_by_unix))



    return render_template("userlist.html")


@app.route("/login")
def login():
    response = make_response(render_template("login.html"))
    return response


@app.route('/logout')
def logout():
    # remove the username from the session if its there
    session.pop('username', None)
    session.clear()
    response = make_response(render_template("index.html"))

    response.set_cookie('loginname', '', expires=0)
    return response


# @app.route('/set/')
# def set():
#     session['key'] = 'value'
#     return 'ok'
# Va fails tiek izpildīts pa tiešo vai kāda cita faila ...
if __name__ == "__main__":
    app.run()  # Palaiž webservera ...
    # app.run(debug=True)  # Palaiž vebservera ...


