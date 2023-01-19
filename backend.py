import sqlite3, shutil, os


# Connects to the database :)
def db_connect(sql):
    db = sqlite3.connect("dance_competition.db")
    cur = db.cursor()
    rows = cur.execute(sql)
    return rows


# view all functions:

def view_all_competitors():
    return db_connect("SELECT * FROM tblCompetitors")


def activities_view_all():
    return db_connect("SELECT * FROM tblActivity")


def events_view_all():
    return db_connect("SELECT * FROM tblEvents INNER JOIN tblCompetitors on tblCompetitors.CompetitorID = tblEvents.CompetitorID;")


def individual_single():
    return db_connect("SELECT * FROM tblEvents INNER JOIN tblCompetitorType on tblCompetitorType.CompetitorTypeID = tblEvents.CompetitorID WHERE competitorTypeID = 1;")


def individual_multiple():
    results = db_connect("")
    print("Individual_multi_leaderboard")
    return results


def team_single():
    return db_connect()
    print("Team_single_leaderboard")


def team_multiple():
    return db_connect()
    print("team_multi_leaderboard")


# search functions

def competitor_search(*array):
    print(array)
    results = db_connect("")
    return results


def event_search(*array):
    results = db_connect("")
    return results


# insert functions


def insert_events(*array):
    print(array)
    return db_connect(f"INSERT INTO tblEvents VALUES ({array})")


# admin functions

def copy_db():
    shutil.copyfile("dance_competition.db", "dance_competition_copy.db")


def delete_copy_db():
    os.remove("dance_competition_copy.db")

print(db_connect("SELECT * FROM sqlite_master").fetchall())
