import numpy as np
from InfluenceArea import InfluenceArea

if __name__ == '__main__':
    IA = InfluenceArea(player_position=np.array([1, 2]), player_velocity=7, player_angle=np.pi/4, ball_distance=10)
    IA.check()

