import cv2
import numpy as np
import time
import random
import cvzone
from cvzone.HandTrackingModule import HandDetector
from MenuMaganger import MenuManager
from InstructionsScreen import InstructionsScreen
from drag_rect import DragRect
from ball import Ball

class GameManager:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        self.detector = HandDetector(detectionCon=0.5)
        
        self.menu_active = True
        self.play_selected = False
        self.how_to_play_active = False
        
        self.last_action_time = time.time()
        self.cooldown_time = 5
        self.attempts = 0

        self.pastel_green = (153, 255, 153)
        self.pastel_blue = (255, 102, 102)
        self.pastel_red = (178, 80, 255)

    def run_menu(self):
        while self.menu_active: 
            success, img = self.cap.read()
            
            img = cv2.flip(img, 1)

            if not success:
                print("Error: No se pudo acceder a la cámara.")
                break

            hands, img = self.detector.findHands(img)

            MenuManager.draw_menu(img)

            if hands:
                choice = MenuManager.check_menu_selection(hands, img)

                if choice == "play":
                    self.play_selected = True
                    self.menu_active = False

                    if cv2.getWindowProperty("Menu", cv2.WND_PROP_VISIBLE) >= 0:
                        cv2.destroyWindow("Menu")
                    
                    self.run_game()

                elif choice == "exit": 
                    self.menu_active = False  
                    self.play_selected = False

                    self.cap.release()
                    cv2.destroyAllWindows()
                    return False

                elif choice == "options":
                    self.show_how_to_play(img)

            cv2.imshow("Menu", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        if cv2.getWindowProperty("Menu", cv2.WND_PROP_VISIBLE) >= 0:
            cv2.destroyWindow("Menu")

    def show_how_to_play(self, img):
        while True:

            success, img = self.cap.read()

            img = cv2.flip(img, 1)

            if not success:
                print("Error: No se pudo acceder a la cámara.")
                break

            hands, img = self.detector.findHands(img)

            InstructionsScreen.draw(img, hands)

            MenuManager.draw_back_button(img)

            if hands and MenuManager.check_back_button(hands, img): 
                if cv2.getWindowProperty("HowToPlay", cv2.WND_PROP_VISIBLE) >= 0:
                    cv2.destroyWindow("HowToPlay")
                break

            cv2.imshow("HowToPlay", img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def run_game(self):
        rectList = [DragRect([x * 250 + 150, 150]) for x in range(3)]
        balls = []
        start_time = time.time()
        ball_spawned = False

        static_ball_pos = (random.randint(100, 1180), random.randint(100, 620))
        static_ball_radius = 25
        game_over = False  

        while True:
            current_time = time.time()
            dt = current_time - start_time
            start_time = current_time

            success, img = self.cap.read()
            if not success:
                print("No se pudo acceder a la cámara.")
                break

            img = cv2.flip(img, 1)

            hands, img = self.detector.findHands(img)

            cv2.putText(img, f"Intentos: {self.attempts}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            if hands:
                lmList = hands[0]['lmList']
                index_tip = (lmList[8][0], lmList[8][1])

                result = self.detector.findDistance(index_tip, (lmList[4][0], lmList[4][1]), img)
                l, _ = result if len(result) == 2 else (result[0], None)

                if l < 30:
                    cursor = index_tip
                    for rect in rectList:
                        rect.update(cursor)
                
                fingers = self.detector.fingersUp(hands[0])

                if fingers == [0, 1, 1, 0, 0]:  
                    for rect in rectList:
                        rect.rotate(5)
                elif fingers == [0, 0, 1, 1, 0]: 
                    for rect in rectList:
                        rect.rotate(-5)
                elif fingers == [0, 0, 1, 1, 1] and not ball_spawned: 
                    balls.append(Ball([640, 0]))
                    ball_spawned = True
                elif fingers == [0, 0, 0, 1, 1] and ball_spawned: 
                    current_time = time.time()
                    if current_time - self.last_action_time >= self.cooldown_time:
                        balls.clear()
                        balls.append(Ball([640, 0]))
                        self.attempts += 1
                        self.last_action_time = current_time

            imgNew = np.zeros_like(img, np.uint8)

            for rect in rectList:
                corners = rect.get_corners()
                cv2.fillPoly(imgNew, [corners], (255, 0, 255))
                cvzone.cornerRect(imgNew, 
                    (rect.posCenter[0] - rect.size[0] // 2, 
                     rect.posCenter[1] - rect.size[1] // 2, 
                     rect.size[0], rect.size[1]), 20, rt=0)

            cv2.circle(imgNew, static_ball_pos, static_ball_radius, (0, 0, 255), cv2.FILLED)

            for ball in balls:
                ball.update(dt)
                ball.check_collision_with_borders(img.shape[1], img.shape[0])
                ball.check_collision(rectList)
                cv2.circle(imgNew, tuple(ball.pos.astype(int)), ball.radius, (0, 255, 0), cv2.FILLED)

                dist = np.linalg.norm(np.array(static_ball_pos) - ball.pos)
                if dist < static_ball_radius + ball.radius:
                    game_over = True

            if game_over:
                cv2.putText(imgNew, "GANASTE!", (500, 360), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (self.pastel_blue), 5)
                cv2.imshow("Image", imgNew)
                cv2.waitKey(3000)
                break

            out = img.copy()
            alpha = 0.5
            mask = imgNew.astype(bool)
            out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

            cv2.imshow("Image", out)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
        self.cap.release()
        cv2.destroyAllWindows()