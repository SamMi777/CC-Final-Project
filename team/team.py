# flask
from flask import Flask, render_template
import redis

# creating the app
app = Flask(__name__)
database = redis.Redis(host="redis", port=6379)


# renders the addTeam form which is used to hit the add-team endpoint which is how teams get added
@app.route("/addTeam")
def index():
    return render_template("addTeam.html")


# renders a unique team form for the given team name passed in as a parameter to the page
@app.route("/<team_name>")
def displayTeam(team_name):

    team_list_data = database.hget("team_list", "teams")

    if team_list_data:
        team_list = eval(team_list_data.decode("utf-8"))

        for team_id, team_data in team_list.items():
            if team_data["team_name"].replace(" ", "") == team_name:
                return render_template("team.html", team=team_data)

   # return render_template("team.html", team=team)
    return "team not found", 404

# fetchTeams endpoint fetches all of the teams in the database and de-serializes them into a python dictionary
@app.route("/fetchTeams")
def fetchAll():
    return {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in database.hgetall("team_list").items()
    }


# fetchSemis endpoint fetches all of the teams in the semi finals list and de-serializes them into another python dictionary
@app.route("/fetchSemis")
def fetchSemis():
    return {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in database.hgetall("semi_team_list").items()
    }


# fetchFinals endpoint fetches all of the teams in the finals list and de-serializes them into another python dictionary
@app.route("/fetchFinals")
def fetchFinals():
    return {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in database.hgetall("final_team_list").items()
    }


# fetchWinner endpoint fetches the chosen winner team and de-serializes the data
@app.route("/fetchWinner")
def fetchWinner():
    return {
        key.decode("utf-8"): value.decode("utf-8")
        for key, value in database.hgetall("winner_team").items()
    }


# running the application on port 5005
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5005")
