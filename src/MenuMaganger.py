from GameUI import GameUI

class MenuManager:
    @staticmethod
    def draw_menu(img):
        pastel_green = (153, 255, 153)
        pastel_blue = (255, 102, 102) 
        pastel_red = (178, 80, 255)   
        
        GameUI.draw_fancy_button(img, (400, 200), (880, 300), pastel_green, "Jugar")
        GameUI.draw_fancy_button(img, (400, 350), (880, 450), pastel_blue, "Como jugar?")
        GameUI.draw_fancy_button(img, (400, 500), (880, 600), pastel_red, "Salir")

    @staticmethod
    def check_back_button(hands, img):
        for hand in hands:
            x, y = hand['lmList'][8][:2]
            if 50 < x < 250 and 600 < y < 700:
                return True
        return False

    @staticmethod
    def check_menu_selection(hands, img):
        for hand in hands: 
            x, y = hand['lmList'][8][:2]
            if 400 < x < 880:  
                if 200 < y < 300:  
                    return "play"
                elif 500 < y < 600:
                    return "exit"
                elif 350 < y < 450:
                    return "options"
        return None  
    
    @staticmethod
    def draw_back_button(img):
        pastel_gray = (200, 200, 200)
        GameUI.draw_fancy_button(img, (50, 600), (250, 700), pastel_gray, "Regresar", text_color=(0, 0, 0))
