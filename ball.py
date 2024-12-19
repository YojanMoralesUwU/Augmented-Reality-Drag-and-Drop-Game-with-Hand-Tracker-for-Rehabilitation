import numpy as np
import cv2

class Ball:
    def __init__(self, pos, radius=20, gravity=0.3*1000, speed=2*100, restitution=0.8):
        self.pos = np.array(pos, dtype=float)
        self.radius = radius
        self.velocity = np.array([0, speed], dtype=float)  
        self.gravity = gravity
        self.restitution = restitution  
        self.friction = 0.98  
        self.gravity = gravity

    def update(self, dt):
        self.velocity[1] += self.gravity * dt
        self.velocity *= self.friction
        self.pos += self.velocity * dt

    def check_collision(self, rects):
        collided = False
        for rect in rects:

            box_center = np.array(rect.posCenter, dtype=float)
            rotation_matrix = cv2.getRotationMatrix2D((0, 0), rect.angle, 1)[:2, :2]

            local_ball_pos = np.dot(self.pos - box_center, rotation_matrix.T)

            local_ball_radius = self.radius + 4

            half_width = rect.size[0] / 2
            half_height = rect.size[1] / 2

            if -half_width - local_ball_radius <= local_ball_pos[0] <= half_width + local_ball_radius and \
            -half_height - local_ball_radius <= local_ball_pos[1] <= half_height + local_ball_radius:
                collided = True

                overlap_x = half_width + local_ball_radius - abs(local_ball_pos[0])
                overlap_y = half_height + local_ball_radius - abs(local_ball_pos[1])

                if overlap_x < overlap_y:
                    correction_dir = np.array([1, 0]) if local_ball_pos[0] > 0 else np.array([-1, 0])
                else:
                    correction_dir = np.array([0, 1]) if local_ball_pos[1] > 0 else np.array([0, -1])

                correction_global = np.dot(correction_dir, rotation_matrix)

                correction_amount = min(overlap_x, overlap_y) * 0.5  
                self.pos += correction_global * correction_amount

                self.velocity -= 2 * np.dot(self.velocity, correction_global) * correction_global

                self.velocity *= 0.9

                break
            
        return collided
    
    def check_collision_with_borders(self, width, height):
        if self.pos[0] - self.radius < 0:
            self.pos[0] = self.radius
            self.velocity[0] *= -self.restitution

        if self.pos[0] + self.radius > width:
            self.pos[0] = width - self.radius
            self.velocity[0] *= -self.restitution

        if self.pos[1] - self.radius < 0:
            self.pos[1] = self.radius
            self.velocity[1] *= -self.restitution

        if self.pos[1] + self.radius > height:
            self.pos[1] = height - self.radius
            self.velocity[1] *= -self.restitution
