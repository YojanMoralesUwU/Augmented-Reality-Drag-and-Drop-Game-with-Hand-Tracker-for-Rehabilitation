import cv2

class GameUI:
    @staticmethod

    def draw_fancy_button(img, top_left, bottom_right, color, text, text_color=(0, 0, 0), font_scale=1.5, thickness=2):
        x1, y1 = top_left
        x2, y2 = bottom_right
        corner_radius = 20

        cv2.rectangle(img, (x1 + corner_radius, y1), (x2 - corner_radius, y2), color, -1)
        cv2.rectangle(img, (x1, y1 + corner_radius), (x2, y2 - corner_radius), color, -1)
        cv2.circle(img, (x1 + corner_radius, y1 + corner_radius), corner_radius, color, -1)
        cv2.circle(img, (x2 - corner_radius, y1 + corner_radius), corner_radius, color, -1)
        cv2.circle(img, (x1 + corner_radius, y2 - corner_radius), corner_radius, color, -1)
        cv2.circle(img, (x2 - corner_radius, y2 - corner_radius), corner_radius, color, -1)

        font_face = cv2.FONT_HERSHEY_PLAIN
        text_size = cv2.getTextSize(text, font_face, font_scale, thickness)[0]
        text_x = x1 + (x2 - x1 - text_size[0]) // 2
        text_y = y1 + (y2 - y1 + text_size[1]) // 2
        cv2.putText(img, text, (text_x, text_y), font_face, font_scale, text_color, thickness)