import cv2
import mediapipe as mp
import pyautogui
import numpy as np

class FingertipMouseController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        self.screen_width, self.screen_height = pyautogui.size()
        
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.smoothing_factor = 0.3
        self.prev_x, self.prev_y = 0, 0
        
        self.click_threshold = 30
        self.is_clicking = False
        self.click_cooldown = 0
        
        pyautogui.FAILSAFE = True
        
    def get_fingertip_position(self, landmarks, frame_width, frame_height):
        index_tip = landmarks.landmark[8]
        x = int(index_tip.x * frame_width)
        y = int(index_tip.y * frame_height)
        return x, y
    
    def get_thumb_position(self, landmarks, frame_width, frame_height):
        thumb_tip = landmarks.landmark[4]
        x = int(thumb_tip.x * frame_width)
        y = int(thumb_tip.y * frame_height)
        return x, y
    
    def smooth_movement(self, x, y):
        if self.prev_x == 0 and self.prev_y == 0:
            self.prev_x, self.prev_y = x, y
            return x, y
        
        smooth_x = int(self.prev_x + (x - self.prev_x) * self.smoothing_factor)
        smooth_y = int(self.prev_y + (y - self.prev_y) * self.smoothing_factor)
        
        self.prev_x, self.prev_y = smooth_x, smooth_y
        return smooth_x, smooth_y
    
    def map_to_screen(self, x, y, frame_width, frame_height):
        x = frame_width - x
        screen_x = int(x * self.screen_width / frame_width)
        screen_y = int(y * self.screen_height / frame_height)
        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))
        return screen_x, screen_y
    
    def detect_click_gesture(self, index_pos, thumb_pos):
        if index_pos and thumb_pos:
            distance = np.sqrt((index_pos[0] - thumb_pos[0])**2 + 
                             (index_pos[1] - thumb_pos[1])**2)
            return distance < self.click_threshold
        return False
    
    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            index_pos = None
            thumb_pos = None
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    index_pos = self.get_fingertip_position(
                        hand_landmarks, frame_width, frame_height)
                    thumb_pos = self.get_thumb_position(
                        hand_landmarks, frame_width, frame_height)
                    
                    cv2.circle(frame, index_pos, 10, (0, 255, 0), -1)
                    cv2.circle(frame, thumb_pos, 10, (255, 0, 0), -1)
                    
                    smooth_x, smooth_y = self.smooth_movement(index_pos[0], index_pos[1])
                    screen_x, screen_y = self.map_to_screen(
                        smooth_x, smooth_y, frame_width, frame_height)
                    
                    pyautogui.moveTo(screen_x, screen_y, duration=0)
                    
                    if self.detect_click_gesture(index_pos, thumb_pos):
                        if not self.is_clicking and self.click_cooldown <= 0:
                            pyautogui.click()
                            self.is_clicking = True
                            self.click_cooldown = 10
                            cv2.putText(frame, "CLICK!", (50, 50), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    else:
                        self.is_clicking = False
                    
                    if self.click_cooldown > 0:
                        self.click_cooldown -= 1
            
            cv2.putText(frame, "Point to move, Pinch to click, 'q' to quit", 
                       (10, frame_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            cv2.imshow('Fingertip Mouse Controller', frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
        
        self.cap.release()
        cv2.destroyAllWindows()

def main():
    try:
        controller = FingertipMouseController()
        controller.run()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
