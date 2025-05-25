# flask
from flask import Flask, render_template
import requests


# creating the app
app = Flask(__name__)


# makes a call to fetchTeams endpoint to get all of the active teams
# then, it iterates through the teams list and adds all the data to the page
# it also displays buttons which are clickable by the user to fetch individual team data pages
@app.route("/")
def index():

    response = requests.get("http://team:5005/fetchTeams")

    if response.text and response.status_code == 200:
        try:
            raw_data = eval(response.text)
            if "teams" in raw_data:
                team_data = eval(raw_data["teams"])
                teams = [
                    {
                        "team_name": team["team_name"].replace(" ", ""),
                        "school_name": team["school_name"],
                        "year_founded": team["year_founded"],
                    }
                    for team in team_data.values()
                ]

            else:
                teams = []

        except ValueError:
            teams = []

    else:
        teams = []

    return render_template("history.html", teams=teams)


# running the application on port 5005
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5005")
