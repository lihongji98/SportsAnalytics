"""
Required data:
infer postion -> X,Y ==== pitch_map
player's coordinate -> x,y
player's velocity -> vel
player's angle -> theta
the distance to the ball -> distance
"""

import numpy as np


class InfluenceArea:
    def __init__(self, 
                 pitch_length: int,
                 pitch_width: int
                 ):
        self.width = max(pitch_length, pitch_width)
        self.length = min(pitch_width, pitch_length)
        self.pitch_map = np.array([[i, j] for i in range(self.length) for j in range(self.width)]) \
                                                            .reshape(self.length, self.width, 2, 1)
        """
        The standard football pitch size:
            length: 100.58 m
            width:  64.01 m
        """

    def influence_radius(self, ball_dist):
        if ball_dist >= 19:
            radius = 10
        else:
            radius = 6 / 18**2 * ball_dist**2 + 4

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
                         [np.sin(player_ang),  np.cos(player_ang)]])

    def normalized_influence(self, infer_pos, player_pos, player_vel, player_ang, ball_dist):
        infer_pos = infer_pos.reshape(-1, 1)
        player_pos = player_pos.reshape(-1, 1)

        r, s = self.rotation_matrix(player_ang), self.scaling_matrix(player_vel, ball_dist)

        v_x = player_vel
        v_y = player_vel
        center_movement = np.array([0.5 * v_x, 0.5 * v_y]).reshape(-1, 1)

        mean = player_pos + center_movement

        cov_matrix = np.dot(np.dot(np.dot(r, s), s), np.linalg.inv(r))
        inverse_cov = np.linalg.inv(cov_matrix)

        assert player_pos.shape == mean.shape, "player position is not compatible with the mean vector."
        
        coef_infer_influence = (-0.5) * np.dot(
            np.dot((infer_pos - mean).T, inverse_cov),
            (infer_pos - mean))

        coef_standarlized = (-0.5) * np.dot(
            np.dot((mean - mean).T, inverse_cov),
            (mean - mean))

        influence = np.exp(coef_infer_influence - coef_standarlized)

        return influence.flatten()[0]
    
    def area_influence_surface(self, player_pos, player_vel, player_ang, ball_dist):
        area_influence_surface = []
        for i in range(self.length):
            for j in range(self.width):
                point_ai= self.normalized_influence(self.pitch_map[i][j], player_pos, player_vel, player_ang, ball_dist)
                area_influence_surface.append(point_ai)
        return np.array(area_influence_surface).reshape(self.length, self.width)

    def check(self):
        influence = self.area_influence_surface(
                                              player_pos = np.array([15,15]), 
                                              player_vel = 6.36, 
                                              player_ang = np.pi / 4, 
                                              ball_dist = 15)
        print(influence)
