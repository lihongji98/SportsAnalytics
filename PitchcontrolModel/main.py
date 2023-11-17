import numpy as np
import matplotlib.pyplot as plt
from InfluenceArea import InfluenceArea


def draw_heatmap(IA):
    map = []
    for i in range(30):
        for j in range(30):
            map.append(np.array([i, j]))
    map = np.array(map).reshape(30, 30, 2, 1)

    ia_distribution = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            IA = InfluenceArea(infer_position=map[i][j], player_position=np.array([15, 15]),
                               player_velocity=6.36, player_angle=np.pi / 4, ball_distance=15)
            ia = IA.normalized_influence()
            ia_distribution.append(ia)
    ia_distribution = np.array(ia_distribution).reshape(30, 30)

    plt.imshow(ia_distribution, cmap='viridis', interpolation='nearest')
    plt.gca().invert_yaxis()
    plt.colorbar(label='Values')
    plt.show()


if __name__ == '__main__':
    IA = InfluenceArea(infer_position=np.array([20, 20]),
                       player_position=np.array([15, 15]),
                       player_velocity=6.36,
                       player_angle=np.pi/4,
                       ball_distance=15)
    draw_heatmap(IA)


