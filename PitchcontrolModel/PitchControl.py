import pandas as pd
import numpy as np
from InfluenceArea import InfluenceArea

"""
Pitch Control = Sigmoid(sum(home_area_influence) - sum(away_area_influence)) ===> point-wise
Required data:
    player information (from database)
            ===> 
            player_influence_surface = Influence.area_influence_surface(
                                                                player_pos, 
                                                                player_vel,
                                                                player_ang,
                                                                ball_dist
                                                                )


TODO:
1. Regularize the dataflow format
2. Complete the pitch control computation
3. Figure out the default attribute the PitchControl attributes
    need read_data function or not
"""


class PitchControl(InfluenceArea):
    def __init__(self):
        super(PitchControl, self).__init__()

    def read_data(self):
        pass

    def compute_pitchControl(self):
        pass
