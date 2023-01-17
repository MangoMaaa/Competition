import sqlite3

# Connects to the database :)
db = sqlite3.connect("dance_competition.db")

cur = db.cursor()

#Competitor Functions:

def view_all_competitors():
    return cur.execute("SELECT * FROM tblCompetitors")

def competitor_search(*array):
    return "Incomplete"

# Activity Functions:

def activities_view_all():
    # shows all of the activities
    return cur.execute("SELECT * FROM tblActivity")

# Event Functions:

def events_view_all():
    return cur.execute("SELECT * FROM tblEvents INNER JOIN tblCompetitors on tblCompetitors.CompetitorID = tblEvents.CompetitorID;")

def event_search(*array):
    return cur.execute("")

def insert_events(*array):
    print(array)
    return cur.execute(f"INSERT INTO tblEvents VALUES ({array})")

#Leaderboard Functions:

#Admin Functions: