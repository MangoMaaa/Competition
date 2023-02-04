import sqlite3
import shutil
import os


# Connects to the database
def db_connect(sql):
    db = sqlite3.connect("dance_competition.db")
    cur = db.cursor()
    rows = cur.execute(sql)
    db.commit()
    return rows

# view all functions:


def view_all_competitors():
    return db_connect("SELECT * FROM tblCompetitors")


def activity_view_all():
    return db_connect("SELECT * FROM tblActivity")


def events_view_all():
    return db_connect("SELECT * FROM tblEvents INNER JOIN tblCompetitors on tblCompetitors.CompetitorID = tblEvents.CompetitorID;")


def contestant_view_all():
    return db_connect("SELECT * FROM tblEvents INNER JOIN tblCompetitorType on tblCompetitorType.CompetitorTypeID = tblEvents.CompetitorID;")


def view_all_solo():
    return db_connect("SELECT * FROM tblEvents INNER JOIN tblCompetitorType on tblCompetitorType.CompetitorTypeID = tblEvents.CompetitorID WHERE CompetitorTypeID = 1;")


def view_all_teams():
    return db_connect("SELECT * FROM tblEvents Where TeamID;")


def view_all_one_team():
    return db_connect("SELECT * FROM tblEvents Where TeamID = 1;")

# search functions


def competitor_search(CompetitorForename="", CompetitorSurname="", TeamName="", CompetitorID="", CompetitorType="", CompetitorTypeID=""):
    return db_connect(f"SELECT * FROM tblCompetitors WHERE CompetitorForename like {CompetitorForename} OR CompetitorSurname like {CompetitorSurname} OR CompetitorTeamName like {TeamName} OR CompetitorID like {CompetitorID} OR CompetitorTypeID like {CompetitorTypeID} ORDER BY competitorID", (CompetitorForename, CompetitorSurname, TeamName, CompetitorID, CompetitorType))


def event_search(EventID="", ActivityID="", CompetitorID="", Score="", Date="", TeamID=""):
    return db_connect(f"SELECT tblEvents.EventID, tblEvents.ActivityTypeID, tblEvents.CompetitorID, tblEvents.Scores, tblEvents.Date, tblEvents.TeamID, tblCompetitors.CompetitorForename, tblCompetitors.CompetitorSurname, tblCompetitors.CompetitorTeamName, tblActivity.ActivityType, tblActivity.ActivityID FROM tblEvents INNER JOIN tblCompetitors on tblEvents.CompetitorID = tblCompetitors.CompetitorID INNER JOIN tblActivity on tblEvents.ActivityTypeID = tblActivity.ActivityTypeID INNER JOIN tblTeams on tblEvents.TeamID = tblTeams.TeamID Where tblEvents.EventID like {EventID} OR tblActivity.ActivityTypeID like {ActivityID} OR tblEvents.CompetitorID like {CompetitorID} OR tblEvents.Scores like {Score} OR tbl Teams.TeamID like {TeamID} ORDER BY tblEvents.Date", (EventID, ActivityID, CompetitorID, Score, Date, TeamID))


def activity_search(ActivityTypeID="", ActivityType=""):
    return db_connect(f"SELECT * FROM tblActivity WHERE tblActivity.ActivityTypeID like {ActivityTypeID} OR tblActivity.ActivityType like {ActivityType} ORDER BY tblActivity.ActivityTypeID", (ActivityTypeID, ActivityType))


# insert functions


def insert_competitor(CompetitorForename, CompetitorSurname, TeamName, CompetitorID, CompetitorType):
    return db_connect(f"INSERT INTO tblCompetitors VALUES {CompetitorForename, CompetitorSurname, TeamName, CompetitorID, CompetitorType}", (CompetitorID, CompetitorForename, CompetitorSurname, TeamName, CompetitorType))


def insert_events(EventID, ActivityTypeID, CompetitorID, Score, Date, TeamName):
    return db_connect(f"INSERT INTO tblEvents VALUES {EventID,ActivityTypeID,CompetitorID,Score,Date,TeamName}", (EventID, ActivityTypeID, CompetitorID, Score, Date, TeamName))


def insert_activity(ActivityTypeID, ActivityType):
    return db_connect(f"INSERT INTO tblActivities VALUES {ActivityTypeID, ActivityType}", (ActivityTypeID, ActivityType))


# delete functions


def delete_competitor(CompetitorID):
    return db_connect(f"DELETE FROM tblCompetitors WHERE CompetitorID = {CompetitorID} ORDER BY tblCompetitors.CompetitorID", (CompetitorID,))


def delete_event(EventID):
    return db_connect(f"DELETE FROM tblEvents WHERE EventID={EventID}", (EventID,))
    db.close()


def delete_activity(ActivityTypeID):
    return db_connect(f"DELETE FROM tblActivities WHERE ActivityTypeID={ActivityTypeID} ", (ActivityTypeID,))
    db.close()

# update functions


def update_competitor(CompetitorID, CompetitorForename, CompetitorSurname, TeamName, CompetitorType):
    return db_connect(f"UPDATE tblCompetitors SET competitorForename={CompetitorForename}, CompetitorSurname={CompetitorSurname}, competitorTeamName={CompetitorTeamName}, competitorTypeID={CompetitorTypeID}, competitorID={CompetitorID}", (CompetitorForename, CompetitorSurname, TeamName, CompetitorType, CompetitorID))
    db.close()


def update_events(EventID, ActivityID, CompetitorID, Score, Date, TeamID):
    return db_connect(f"UPDATE tblEvents SET ActivityTypeID={ActivityTypeID}, CompetitorID={CompetitorID}, Scores={Scores}, Date={Date}, TeamID={TeamID} WHERE EventID={EventID}", (ActivityID, CompetitorID, Score, Date, EventID, TeamID))
    db.close()

def update_activity(ActivityTypeID, ActivityType):
    return db_connect(f"UPDATE tblActivities SET ActivityTypeID={ActivityTypeID}, ActivityType={ActivityTypeID} WHERE ActivityTypeID={ActivityType}", (ActivityTypeID, ActivityType, ActivityTypeID))
# admin functions

def copy_db():
    shutil.copyfile("dance_competition.db", "dance_competition_copy.db")


def delete_copy_db():
    os.remove("dance_competition_copy.db")

print(db_connect("SELECT * FROM sqlite_master").fetchall())

# DO NOT RUN WITHOUT BACKUP


def drop_tables(self):
    return db_connect("DROP TABLE tblActivity DROP TABLE tblCompetitors DROP TABLE tblEvents DROP TABLE tblTeams DROP TABLE tblCompetitorType")
