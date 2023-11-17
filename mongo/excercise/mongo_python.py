import database
import pandas as pd
import mongoengine as mongo


def connect_db():
    return mongo.connect(db="SA", username="lihong", password="1998918!", host="localhost", port=27017)


def training_1():
    # List match_id, start_frame and origin_player of all Remate that end up in Gol
    # ordered by match_id and start_frame both in descending order
    connect_db()
    print("databased connection complete!")
    df_shots = pd.DataFrame(database.Event.objects(event_type="Remate", event_subtype="Gol").
                            order_by("-match_frame", "-start_frame").as_pymongo())
    print(df_shots[["match_id", "start_frame", "origin_player"]])


def training_2():
    # Update all Match documents with each team_id from Team collection named home_team_id and away_team_id
    connect_db()
    for match in database.Match.objects():
        match.home_team_id = match.home_team.team_id
        match.away_team_id = match.away_team.team_id
        match.save()


def training_3():
    # Update all Event documents with the opponent team_id named opponent_team
    connect_db()
    team_dict1 = {(match.id, match.home_team_id): match.away_team_id for match in database.Match.objects()}
    team_dict2 = {(match.id, match.away_team_id): match.home_team_id for match in database.Match.objects()}
    team_dict = {**team_dict1, **team_dict2}
    for event in database.Event.objects():
        event.opponent_team = team_dict[(event.match_id, event.team)]
        event.save()


def training_4():
    # Create a new Event named Defensa that denotes the time when one team is defending.
    connect_db()
    new_event_type = "Defensa"
    for event in database.Event.objects(event_type=new_event_type):
        event.delete()
    for event in database.Event.objects(event_type="Ataque"):
        delattr(event, "id")
        event.event_type = new_event_type
        buffer = event.team
        event.team = event.opponent_team
        event.opponent_team = buffer
        event.save()


def training_5():
    # Create a new Collection named Competition that denotes for every competition
    # his id and the number of matches in that competition.
    connect_db()
    for comp in database.Competition.objects():
        comp.delete()
    df_matches = pd.DataFrame(database.Match.objects().as_pymongo())[["competition"]]
    for comp_id, num in df_matches.groupby("competition"):
        new_competition = database.Competition()
        new_competition.id = comp_id
        new_competition.match_quantity = num.shape[0]
        new_competition.save()

