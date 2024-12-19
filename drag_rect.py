import numpy as np
import math

class DragRect():

    def __init__(self, posCenter, size=[200, 200], angle=0):
        self.posCenter = posCenter
        self.size = size
        self.angle = angle

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        if cx - w // 2 < cursor[0] < cx + w // 2 and \
           cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor

    def rotate(self, angle_step):
        self.angle = (self.angle + angle_step) % 360

    def get_corners(self):
        cx, cy = self.posCenter
        w, h = self.size
        angle_rad = math.radians(self.angle)

        corners = [
            [-w // 2, -h // 2],
            [w // 2, -h // 2],
            [w // 2, h // 2],
            [-w // 2, h // 2],
        ]

        rotated_corners = []
        for corner in corners:
            x, y = corner
            x_rot = cx + int(x * math.cos(angle_rad) - y * math.sin(angle_rad))
            y_rot = cy + int(x * math.sin(angle_rad) + y * math.cos(angle_rad))
            rotated_corners.append([x_rot, y_rot])
        return np.array(rotated_corners, np.int32)
