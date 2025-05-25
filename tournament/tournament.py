# flask
from flask import Flask, render_template
import requests
import redis

# creating the app
app = Flask(__name__)
database = redis.Redis(host="redis", port=6379)


# endpoint displays the finals form, taking fetchFinals teams and then passes the data to the finals page
@app.route("/finals")
def fourthRound():
    response1 = requests.get("http://team:5005/fetchFinals")

    if response1.text and response1.status_code == 200:

        try:

            finals_raw_data = eval(response1.text)
            if "teams" in finals_raw_data:
                finals_team_data = eval(finals_raw_data["teams"])
                finals_teams = [team["team_name"] for team in finals_team_data.values()]

            else:
                finals_teams = []

        except ValueError:
            finals_teams = []

    else:
        finals_teams = []

    return render_template("final.html", teams=finals_teams)


# endpoint displays winner form, passing in a winner team which is gets from fetchWinner endpoint
@app.route("/winner")
def lastRound():
    response2 = requests.get("http://team:5005/fetchWinner")

    if response2.text and response2.status_code == 200:

        try:

            winner_raw_data = eval(response2.text)
            if "teams" in winner_raw_data:
                winner_team_data = eval(winner_raw_data["teams"])
                winner_teams = [team["team_name"] for team in winner_team_data.values()]

            else:
                winner_teams = []

        except ValueError:
            winner_teams = []

    else:
        winner_teams = []

    return render_template("winner.html", teams=winner_teams)


# endpoint displays the semi finals, fetching the four teams in the semi finals and then if the tournament is simulated
# it will display the four teams that made it through
@app.route("/semifinals")
def thirdRound():
    response3 = requests.get("http://team:5005/fetchSemis")

    if response3.text and response3.status_code == 200:

        try:

            semi_raw_data = eval(response3.text)
            if "teams" in semi_raw_data:
                semi_team_data = eval(semi_raw_data["teams"])
                semi_teams = [team["team_name"] for team in semi_team_data.values()]

            else:
                semi_teams = []

        except ValueError:
            semi_teams = []

    else:
        semi_teams = []

    return render_template("semifinal.html", teams=semi_teams)


# default endpoint - fetches the teams from the fetchteams endpoint and then if the data exists, it renders
# the tournament page with all of the active teams
@app.route("/")
def firstRound():
    response = requests.get("http://team:5005/fetchTeams")

    if response.text and response.status_code == 200:

        try:

            raw_data = eval(response.text)
            if "teams" in raw_data:
                team_data = eval(raw_data["teams"])
                teams = [team["team_name"] for team in team_data.values()]

            else:
                teams = []

        except ValueError:
            teams = []

    else:
        teams = []
    return render_template("tournament.html", teams=teams)


# running the application on port 5005
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5005")
