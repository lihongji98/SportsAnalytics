from mongoengine.fields import *
import mongoengine as meng


class Team(meng.DynamicDocument):
    team_id = IntField(required=True)

    meta = {
        'indexes': ['team_id'],
        'db_alias': 'default'
    }


class Match(meng.DynamicDocument):
    competition = ObjectIdField()
    home_team = ReferenceField(Team)
    away_team = ReferenceField(Team)
    halves = ListField(DictField())
    match_id = IntField()
    
    meta = {
        'indexes': ['competition'],
        'db_alias': 'default'
    }


class Event(meng.DynamicDocument):
    match_id = ObjectIdField()
    
    event_type = StringField(required=True)
    
    start_frame = IntField(required=True)
    end_frame = IntField()
    duration = FloatField()
    
    origin_pos_x = FloatField()
    origin_pos_y = FloatField()
    
    destination_pos_x = FloatField()
    destination_pos_y = FloatField()

    team = IntField()    
    
    success = StringField()

    origin_player = IntField()
    destination_player = IntField()

    event_subtype = StringField()

    meta = {
        'indexes': ['match_id', 'event_type', 'origin_player', 'team', 'start_frame'],
        'db_alias': 'default'
    }


class Player(meng.DynamicDocument):
    player_id = IntField()
    team = IntField()
    played_match = IntField()

    meta = {
        'indexes': ['player_id'],
        'db_alias': 'default'
    }