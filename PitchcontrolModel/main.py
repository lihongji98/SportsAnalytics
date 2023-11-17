import numpy as np
import matplotlib.pyplot as plt
from InfluenceArea import InfluenceArea


def draw_heatmap(IA):
    influence = IA.area_influence_surface(  
                                        player_pos = np.array([15,15]), 
                                        player_vel = 6.36, 
                                        player_ang = np.pi / 4, 
                                        ball_dist = 15
                                        )
    print(influence.shape)
    plt.imshow(influence, cmap='viridis', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.colorbar(label='Values')
    plt.show()


if __name__ == '__main__':
    IA = InfluenceArea(pitch_length=100, pitch_width=50)
    draw_heatmap(IA)


