from math import cos, sin, radians, sqrt, pow

import numpy as np


class Positioner:
    _rotation: (float, float)
    _position: (float, float)


    def __init__(self, initial_rotation=(1, 0), initial_position=(0, 0)):
        self._rotation = initial_rotation
        self._position = initial_position


    def add_rotation(self, deg):
        theta = np.deg2rad(-deg)
        rot_mat = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        rot = np.array(self._rotation)
        rot = np.dot(rot_mat, rot)
        scale = sqrt(pow(rot[0], 2) + pow(rot[1], 2))
        rot[0] /= scale
        rot[1] /= scale
        self._rotation = tuple(rot)


    def add_position(self, distance):
        self._position = (self._rotation[0] * distance + self._position[0],
                          self._rotation[1] * distance + self._position[1])


    def get_position(self):
        return self._position


    def get_rotation(self):
        return self._rotation

#
