"""
Required data:
player's coordinate -> x,y
player's velocity -> vel
player's angle -> theta
the distance to the ball -> distance
"""

import numpy as np


class InfluenceArea:
    def __init__(self, player_position: np.ndarray, player_velocity: float, player_angle: float,
                 ball_distance: float):
        self.player_pos, self.player_vel, self.player_ang = player_position, player_velocity, player_angle
        self.ball_dist = ball_distance

    def influence_radius(self):
        if self.ball_dist >= 19:
            radius = 10
        else:
            radius = 6 / (19 * 19) * self.ball_dist**2 + 4
        return radius

    def speed_coefficient(self):
        speed_coef = self.player_vel**2 / 13**2
        return speed_coef

    def scaling_matrix(self):
        radius = self.influence_radius()
        speed_coef = self.speed_coefficient()
        s_x = radius + (radius * speed_coef)
        s_y = radius - (radius * speed_coef)

        return np.array([[s_x, 0],
                         [0, s_y]])

    def rotation_matrix(self):
        return np.array([[np.cos(self.player_ang), -np.sin(self.player_ang)],
                         [np.sin(self.player_ang), np.cos(self.player_ang)]])

    def normalized_influence(self):
        r, s = self.rotation_matrix(), self.scaling_matrix()

        v_x = self.player_vel * np.cos(self.player_vel)
        v_y = self.player_vel * np.sin(self.player_vel)

        mean = self.player_pos + np.array([0.5 * v_x, 0.5 * v_y])
        cov_matrix = np.dot(np.dot(np.dot(r, s), s), np.linalg.inv(r))
        inverse_cov = np.linalg.inv(cov_matrix)





    def check(self):
        r = self.rotation_matrix()
        s = self.scaling_matrix()
        print(s)
        print(r)
