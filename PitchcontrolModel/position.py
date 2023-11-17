import pandas as pd
import numpy as np

"""
TODO:
1. Reformat the position to np.array
2. Compute the distance to the ball
"""


def position():
    player_position_name = ["GK",
                            "RWB", "RB", "LB", "LWB",
                            "CDM", "RM", "LM",
                            "RW", "ST", "LW"
                            ]
    home_player_position_coordinate = [[19, 31],
                                       [61, 10], [43, 20], [43, 33], [52, 50],
                                       [52, 26], [70, 8], [60, 34],
                                       [81, 5], [80, 25], [75, 40]
                                       ]

    away_player_position_coordinate = [[98, 33],
                                       [64, 41], [78, 39], [81, 26], [82, 6],
                                       [64, 31], [77, 20], [78, 8],
                                       [49, 30], [50, 15], [69, 8]
                                       ]

    ball_position = [81, 5]

    home_player_distance = [np.sqrt((pos[0] - ball_position[0]) ** 2 + (pos[1] - ball_position[1]) ** 2)
                            for pos in home_player_position_coordinate]
    away_player_distance = [np.sqrt((pos[0] - ball_position[0]) ** 2 + (pos[1] - ball_position[1]) ** 2)
                            for pos in away_player_position_coordinate]

    home_team = pd.DataFrame({'pos': player_position_name,
                              'home_xy': home_player_position_coordinate,
                              'home_distance': home_player_distance})

    away_team = pd.DataFrame({'pos': player_position_name,
                              'away_xy': away_player_position_coordinate,
                              'away_distance': away_player_distance})

    position_info = pd.merge(home_team, away_team, on=["pos"], how="inner")
    return position_info