import numpy as np
from InfluenceArea import InfluenceArea
"""
Pitch Control = Sigmoid(sum(home_area_influence) - sum(away_area_influence))

Required data:
    player information (from database)
            ===> 
            player_influence_surface = Influence.area_influence_surface(
                                                                xy, 
                                                                vel,
                                                                ang,
                                                                distance
                                                                )
"""


class PitchControl(InfluenceArea):
    def __init__(self):
        super(PitchControl, self).__init__()
        self.player_num = 11
        self.home_dicts = None
        self.away_dicts = None

    def process_frame_data(self, frame_info_home, frame_info_away):
        home_info, away_info = [], []
        for i in range(self.player_num):
            home_player_info = frame_info_home[i][1:].to_dict()
            home_player_info['xy'] = np.flip(np.array(home_player_info['xy']).reshape(2))
            home_info.append(home_player_info)
            away_player_info = frame_info_away[i][1:].to_dict()
            away_player_info['xy'] = np.flip(np.array(away_player_info['xy']).reshape(2))
            away_info.append(away_player_info)
        self.home_dicts = home_info
        self.away_dicts = away_info

    def compute_pitchControl(self):
        home_area_influence, away_area_influence = [], []
        for i, home_player_dict in enumerate(self.home_dicts):
            player_ai_surface = self.area_influence_surface(**home_player_dict)
            home_area_influence.append(player_ai_surface)
        for away_player_dict in self.away_dicts:
            player_ai_surface = self.area_influence_surface(**away_player_dict)
            away_area_influence.append(player_ai_surface)

        home_area_influence = np.array(home_area_influence).reshape(self.player_num, self.length, self.width)
        away_area_influence = np.array(away_area_influence).reshape(self.player_num, self.length, self.width)

        home_pitch_control_surface = np.sum(home_area_influence, axis=0)
        away_pitch_control_surface = np.sum(away_area_influence, axis=0)
        pitch_control_surface = self.sigmoid(home_pitch_control_surface - away_pitch_control_surface)

        return pitch_control_surface


