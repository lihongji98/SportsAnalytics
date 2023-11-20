import database
import pandas as pd
import mongoengine as mongo


def connect_db():
    return mongo.connect(db="football", username="lihong", password="1998918!", host="localhost", port=27017)


def exercise_1():
    # List all Pase Exitoso with a duration greater than 4 seconds
    connect_db()
    print("succeed in connecting the database.")
    df = pd.DataFrame(database.Event.objects(event_type="Pase", success="Exitoso", duration__gt=4).as_pymongo())
    print(df)


def exercise_2():
    # List all different players who have shot ordered by origin_player
    connect_db()
    print("succeed in connecting the database.")
    shot_player = pd.DataFrame(database.Event.objects(event_type="Remate",
                                                      event_subtype__in=["Gol", "No Gol"])
                               .as_pymongo())["origin_player"]
    print(sorted(set(shot_player.values)))


def exercise_3():
    # Number of attacks from teams 1 and 11
    connect_db()
    print("succeed in connecting to the database.")
    df = pd.DataFrame(database.Event.objects(event_type="Ataque").order_by("team").as_pymongo()).groupby("team")
    for k, v in df:
        if k <= 11:
            print("The number of attacks: team ", k, " ->", v.shape[0])


def exercise_4():
    # Remove all Matches which hasn’t any Event
    connect_db()
    print("succeed in connecting the database.")
    matches_with_event = pd.DataFrame(database.Event.objects.only("match_id").as_pymongo())["match_id"].values
    matches_with_event = set(matches_with_event)
    for match in database.Match.objects():
        if match.id not in matches_with_event:
            match.delete()


def exercise_5():
    # For each Pase, Remate and Balon al Pie set the id of the containing attack named attack_id.
    connect_db()
    print("succeed in connecting the database.")

    for event in database.Event.objects(attack_id=208):
        event.delete()

    attack_dict = {}
    attack_id = 0
    for event in database.Event.objects(event_type="Ataque"):
        attack_info = (event.end_frame, attack_id)
        if event.match_id not in attack_dict.keys():
            attack_dict[event.match_id] = [attack_info]
        else:
            attack_dict[event.match_id].append(attack_info)
        attack_id += 1

    for event in database.Event.objects():
        if event.event_type == "Pase" or "Remate" or "Balon al Pie":
            attack_candidates = attack_dict[event.match_id]
            for attack in attack_candidates:
                if event.end_frame <= attack[0]:
                    event.attack_id = attack[1]
        else:
            event.attack_id = 0
        event.save()


def exercise_6():
    # Create a new Event named Cambio de Posesion that denotes when the possession team has changed.
    connect_db()
    for event in database.Event.objects(event_type="Cambio de Posesion"):
        event.delete()

    new_event_type = "Cambio de Posesion"
    for event in database.Event.objects():
        delattr(event, "id")
        if event.event_type == "Pase" and event.success == "Fallido":
            event.event_type = new_event_type
        elif event.event_type == "Remate":
            event.event_type = new_event_type
        else:
            pass
        event.save()


def exercise_7():
    # Create a new Collection named Player that denotes for every player his id,
    # the team which he belongs to and the number of matches he has played.
    connect_db()
    for player in database.Player.objects():
        player.delete()

    origin_player_df = pd.DataFrame(database.Event.objects(event_type__in=["Balon al Pie", "Pase", "Remate"],
                                                           origin_player__nin=[None]).
                                    only("match_id", "team", "origin_player").as_pymongo())[['match_id', 'team', 'origin_player']]
    origin_player_df.rename(columns={'origin_player': 'player'}, inplace=True)

    destination_player_df = pd.DataFrame(database.Event.objects(event_type="Pase",
                                                                destination_player__nin=[None]).
                                         only("match_id", "team", "destination_player").as_pymongo())[['match_id', 'team', 'destination_player']]
    destination_player_df.rename(columns={'destination_player': 'player'}, inplace=True)

    player_df = pd.concat([origin_player_df, destination_player_df], axis=0, ignore_index=True).drop_duplicates()

    player_df = player_df.groupby("player")

    for _, player_info in player_df:
        player = database.Player()
        player.player_id = player_info["player"].values[0]
        player.team = player_info["team"].values[0]
        player.played_match = len(set(player_info["match_id"].values))
        player.save()
