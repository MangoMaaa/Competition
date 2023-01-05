import sqlite3

# shows all of the competitors
db = sqlite3.connect("dance_competition.db")

cur = db.cursor()

def view_all_competitors():
    return cur.execute("SELECT * FROM tblCompetitors")

def activities_view_all():
    # shows all of the activities
    return cur.execute("SELECT * FROM tblActivity")

def events_view_all():
    return cur.execute("SELECT * FROM tblEvents INNER JOIN tblCompetitors on tblCompetitors.CompetitorID = tblEvents.CompetitorID;")

def event_search(*array):
    print(array)
    return cur.execute("")
