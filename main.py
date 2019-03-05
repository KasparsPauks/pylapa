from flask import Flask, render_template

app = Flask(__name__)


# Kur atrodas saknes direktorija caur dekorātora adresi
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')

# Va fails tiek izpildīts pa tiešo vai kāda cita faila ...
if __name__ == '__main__':
    app.run()  # Palaiž vebservera ...
    # app.run(debug=True) # Palaiž vebservera ...