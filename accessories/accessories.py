# flask
from flask import Flask, render_template

# creating the app
app = Flask(__name__)


# renders the credits page
@app.route("/credits")
def credits():
    return render_template("credits.html")


# renders the homepage and the static image for the frozen four logo
@app.route("/")
def homepage():
    return render_template("homepage.html")


# running the application on port 5005
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5005")
