import cv2
from GameUI import GameUI
from MenuMaganger import MenuManager

class InstructionsScreen:
    @staticmethod
    def draw(img, hands):
        images = [
            ("docs\\1.png", "Juntar para mover"), 
            ("docs\\2.png", "Rotar a la derecha"),
            ("docs\\5.png", "Rotar a la izquierda"),
            ("docs\\3.png", "Iniciar juego"),
            ("docs\\4.png", "Reiniciar pelota")
        ]

        x_offset, y_offset = 50, 50

        for i, (img_path, text) in enumerate(images):
            img_option = cv2.imread(img_path)
            if img_option is None:
                continue

            img_option_resized = cv2.resize(img_option, (150, 150))
            current_x = x_offset + (i % 3) * 220 
            current_y = y_offset + (i // 3) * 220  

            img[current_y:current_y + 150, current_x:current_x + 150] = img_option_resized

            cv2.putText(img, text, 
                        (current_x, current_y + 170),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 1)

        GameUI.draw_fancy_button(img, (50, 600), (250, 700), (200, 200, 200), 
                                 "Regresar", text_color=(0, 0, 0))

        if hands and MenuManager.check_back_button(hands, img):
            return "back"
        return None
