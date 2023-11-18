"""
Required data:
infer postion -> X,Y ==== pitch_map
player's coordinate -> x,y              (from database)
player's velocity -> vel                (from database)
player's angle -> theta                 (from database)
the distance to the ball -> distance    (from database)
"""

import numpy as np


class InfluenceArea:
    def __init__(self,
                 pitch_length: int,
                 pitch_width: int
                 ):
        self.width = max(pitch_length, pitch_width)
        self.length = min(pitch_width, pitch_length)
        self.pitch_map = (np.array([[i, j] for i in range(self.length) for j in range(self.width)]).
                          reshape(self.length, self.width, 2, 1))
        """
        The standard football pitch size:
            length: 100.58 m
            width:  64.01 m
        """

    def influence_radius(self, ball_dist):
        if ball_dist >= 19:
            radius = 10
        else:
            radius = 6 / 18 ** 2 * ball_dist ** 2 + 4

        return radius

    def speed_coefficient(self, player_vel):
        speed_coef = player_vel ** 2 / 13 ** 2
        return speed_coef

    def scaling_matrix(self, player_vel, ball_dist):
        radius = self.influence_radius(ball_dist)
        speed_coef = self.speed_coefficient(player_vel)
        s_x = (radius + (radius * speed_coef)) * 0.5
        s_y = (radius - (radius * speed_coef)) * 0.5

        return np.array([[s_x, 0],
                         [0, s_y]])

    def rotation_matrix(self, player_ang):
        return np.array([[np.cos(player_ang), -np.sin(player_ang)],
                         [np.sin(player_ang), np.cos(player_ang)]])

    def area_influence_surface(self, player_pos, player_vel, player_ang, ball_dist):
        player_pos = player_pos.reshape(-1, 1)
        r, s = self.rotation_matrix(player_ang), self.scaling_matrix(player_vel, ball_dist)
        center_movement = np.array([0.5 * player_vel, 0.5 * player_vel]).reshape(-1, 1)
        mean = player_pos + center_movement

        cov_matrix = np.dot(np.dot(np.dot(r, s), s), np.linalg.inv(r))
        inverse_cov = np.linalg.inv(cov_matrix)

        assert player_pos.shape == mean.shape, "player position is not compatible with the mean vector."
        print(mean.shape, self.pitch_map.shape)
        coefficient_infer_influence = (-0.5) * np.matmul(
            np.matmul(
                np.transpose((self.pitch_map - mean), axes=(0, 1, 3, 2)), inverse_cov),
            (self.pitch_map - mean)
        )

        coefficient_standardized = (-0.5) * np.matmul(
            np.matmul(
                np.transpose(np.zeros_like(self.pitch_map), axes=(0, 1, 3, 2)), inverse_cov),
            np.zeros_like(self.pitch_map)
        )

        influence = np.exp(coefficient_infer_influence - coefficient_standardized)

        return np.squeeze(influence, axis=(2, 3))

    def check(self):
        influence = self.normalized_influence(
            player_pos=np.array([15, 15]),
            player_vel=6.36,
            player_ang=np.pi / 4,
            ball_dist=15)
        print(influence)
