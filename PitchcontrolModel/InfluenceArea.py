"""
Required data:
infer postion -> X,Y
player's coordinate -> x,y
player's velocity -> vel
player's angle -> theta
the distance to the ball -> distance
"""

import numpy as np


class InfluenceArea:
    def __init__(self, infer_position: np.array, player_position: np.ndarray,
                 player_velocity: float, player_angle: float, ball_distance: float):
        self.infer_pos = infer_position.reshape(-1, 1)
        self.player_pos, self.player_vel, self.player_ang = player_position.reshape(-1, 1), player_velocity, player_angle
        self.ball_dist = ball_distance

    def influence_radius(self):
        if self.ball_dist >= 19:
            radius = 10
        else:
            radius = 6 / 18**2 * self.ball_dist**2 + 4

        return radius

    def speed_coefficient(self):
        speed_coef = self.player_vel ** 2 / 13 ** 2
        return speed_coef

    def scaling_matrix(self):
        radius = self.influence_radius()
        speed_coef = self.speed_coefficient()
        s_x = (radius + (radius * speed_coef)) * 0.5
        s_y = (radius - (radius * speed_coef)) * 0.5

        return np.array([[s_x, 0],
                         [0, s_y]])

    def rotation_matrix(self):
        return np.array([[np.cos(self.player_ang), -np.sin(self.player_ang)],
                         [np.sin(self.player_ang), np.cos(self.player_ang)]])

    def normalized_influence(self):
        r, s = self.rotation_matrix(), self.scaling_matrix()

        v_x = self.player_vel
        v_y = self.player_vel
        center_movement = np.array([0.5 * v_x, 0.5 * v_y]).reshape(-1, 1)

        mean = self.player_pos + center_movement

        cov_matrix = np.dot(np.dot(np.dot(r, s), s), np.linalg.inv(r))
        inverse_cov = np.linalg.inv(cov_matrix)

        assert self.player_pos.shape == mean.shape, "player position is not compatible with the mean vector."
        coef_infer_influence = (-0.5) * np.dot(
            np.dot((self.infer_pos - mean).T, inverse_cov),
            (self.infer_pos - mean))
        coef_standarlized = (-0.5) * np.dot(
            np.dot((mean - mean).T, inverse_cov),
            (mean - mean))

        influence = np.exp(coef_infer_influence - coef_standarlized)
        return influence.flatten()

    def check(self):
        influence = self.normalized_influence()
        print(influence)
