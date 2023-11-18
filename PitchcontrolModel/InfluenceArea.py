"""
Required data:
infer postion -> X,Y ==== pitch_map
player's coordinate -> x,y              (from database)
player's velocity -> vel                (from database)
player's angle -> theta                 (from database)
the distance to the ball -> distance    (from database)
"""

import numpy as np


def influence_radius(ball_dist):
    if ball_dist >= 19:
        radius = 10
    else:
        radius = 6 / 18 ** 2 * ball_dist ** 2 + 4

    return radius


def speed_coefficient(player_vel):
    speed_coef = player_vel ** 2 / 13 ** 2
    return speed_coef


def rotation_matrix(player_ang):
    return np.array([[np.cos(player_ang), -np.sin(player_ang)],
                     [np.sin(player_ang), np.cos(player_ang)]])


def scaling_matrix(player_vel, ball_dist):
    radius = influence_radius(ball_dist)
    speed_coef = speed_coefficient(player_vel)
    s_x = (radius + (radius * speed_coef)) * 0.5
    s_y = (radius - (radius * speed_coef)) * 0.5

    return np.array([[s_x, 0],
                     [0, s_y]])


class InfluenceArea:
    def __init__(self,
                 pitch_length=100,
                 pitch_width=65
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

    def sigmoid(self, x):
        return (np.exp(-x) + 1) ** (-1)

    def area_influence_surface(self, xy, ang, vel, distance):
        xy = xy.reshape(-1, 1)
        r, s = rotation_matrix(ang), scaling_matrix(vel, distance)
        center_movement = np.array([0.5 * vel, 0.5 * vel]).reshape(-1, 1)
        mean = xy + center_movement

        cov_matrix = np.dot(np.dot(np.dot(r, s), s), np.linalg.inv(r))
        inverse_cov = np.linalg.inv(cov_matrix)

        assert xy.shape == mean.shape, "player position is not compatible with the mean vector."

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
        influence = self.area_influence_surface(
            xy=np.array([8, 70]),
            vel=13,
            ang=2.09,
            distance=11.4
        )
        return influence
