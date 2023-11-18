import pandas as pd
import numpy as np

"""
TODO:
1. Reformat the position to np.array
2. Compute the distance to the ball
"""


def position():
    player_position_name = ["p1",
                            "p2", "p3", "p4", "p5",
                            "p6", "p7", "p8",
                            "p9", "p10", "p11"
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

    home_player_angle = [0,
                         -40, -10, -20, -30,
                         -45, 30, 0,
                         -5, -45, 5,
                         ]
    for i in range(len(home_player_angle)):
        home_player_angle[i] = home_player_angle[i] * np.pi / 180 + np.pi/2
    away_player_angle = [0,
                         -5, 5, -30, -8,
                         -10, 15, 15,
                         -10, -30, 10
                         ]
    for i in range(len(away_player_angle)):
        away_player_angle[i] = away_player_angle[i] * np.pi / 180 + np.pi/2

    home_player_velocity = [0,
                            5, 3, 2, 2,
                            3, 11, 4,
                            5, 8, 9
                            ]
    away_player_velocity = [0,
                            3, 6, 4, 5,
                            6, 8, 12,
                            3, 1, 5
                            ]

    ball_position = [81, 5]

    home_player_distance = [np.sqrt((pos[0] - ball_position[0]) ** 2 + (pos[1] - ball_position[1]) ** 2)
                            for pos in home_player_position_coordinate]
    away_player_distance = [np.sqrt((pos[0] - ball_position[0]) ** 2 + (pos[1] - ball_position[1]) ** 2)
                            for pos in away_player_position_coordinate]

    home_team = pd.DataFrame({'pos': player_position_name,
                              'xy': home_player_position_coordinate,
                              'ang': home_player_angle,
                              'vel': home_player_velocity,
                              'distance': home_player_distance})

    away_team = pd.DataFrame({'pos': player_position_name,
                              'xy': away_player_position_coordinate,
                              'ang': away_player_angle,
                              'vel': away_player_velocity,
                              'distance': away_player_distance})

    return home_team.T, away_team.T
