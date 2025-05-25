# flask
from flask import Flask, render_template, request
import redis
import random

# creating the app
app = Flask(__name__)
database = redis.Redis(host="redis", port=6379)


# endpoint to add a team to the db post request
# hits the add team endpoint from the add-team service and uses that data to add a team to the db
# basically, it takes the data from the form found in templates and puts it into a dictionary
# then from there it checks if there are already 8 teams and if there are then it won't let the user add any more
# otherwise, on the first input, it will create all 8 teams iteratively and then update them as the user adds more
# finally, it renders a team-added page that has all of the data being passed and allows the user to add more teams if they wish.
@app.route("/insertTeam", methods=["POST"])
def index():

    team_name = request.form["team_name"].strip()
    school_name = request.form["school_name"]
    year_founded = request.form["year_founded"]

    team_data = {
        "team_name": team_name,
        "school_name": school_name,
        "year_founded": year_founded,
    }

    team_list = database.hget("team_list", "teams")
    if team_list:
        team_list = eval(team_list.decode())
    else:
        team_list = {}

    # Check if there are already 8 teams, if so, we return the toomanyteams page which informs the user that the tournament is full
    # and prompts them to go back and play the tournament
    if len(team_list) >= 8:
        return render_template("toomanyteams.html")

    # Find the next available team key
    team_key = f"team{len(team_list) + 1}"
    team_list[team_key] = team_data

    # Save the updated team list back to the database
    database.hset("team_list", "teams", str(team_list))

    return render_template("team-added.html", team_data=team_data)


# this endpoint handles all of the logic to simulate the tournament.
# it randomly selects 4/8 teams for semi finals, 2/4 for finals, and then 1 winner
# then, it adds them all to the database
@app.route("/simulateTournament")
def simulateTournament():

    semi_numbers = random.sample(range(8), 4)
    final_numbers = random.sample(range(4), 2)
    winner_number = random.choice(range(2))

    # Fetch the teams from the team_list dictionary in the database
    teams = database.hget("team_list", "teams")

    if teams:
        teams = eval(teams.decode())
    else:
        teams = {}

    if teams and (len(teams) == 8):
        # Create a dictionary for the semi-final teams
        semi_team_list = {
            f"semi_team{i+1}": teams[f"team{num+1}"]
            for i, num in enumerate(semi_numbers)
        }

        # Save the semi_team_list dictionary to the database
        database.hset("semi_team_list", "teams", str(semi_team_list))

        semi_team_keys = list(semi_team_list.keys())

        final_team_list = {
            f"final_team{i+1}": semi_team_list[semi_team_keys[num]]
            for i, num in enumerate(final_numbers)
        }

        database.hset("final_team_list", "teams", str(final_team_list))

        final_team_keys = list(final_team_list.keys())

        winner = {"winner": final_team_list[final_team_keys[winner_number]]}

        database.hset("winner_team", "teams", str(winner))

        winner = [team["team_name"] for team in winner.values()]

        return '<a href="/tournament">Tournament Simulated! Click to see who won</a>'
    else:
        return '<a href="/tournament">Not enough teams entered! Go back and add some more!</a>'


# running the application on port 5005
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5005")
