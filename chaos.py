# language: Python, file: chaos.py
import tkinter as tk
from PIL import Image, ImageTk
import random
import threading
import time
import os
import sys
import pygame

# ================= НАСТРОЙКИ =================
ERROR_TEXTS = [
    "CRITICAL ERROR: 0x000000FF",
    "SYSTEM32 HALTED",
    "KERNEL PANIC!",
    "MEMORY ACCESS VIOLATION",
    "FATAL EXCEPTION",
    "HARD DRIVE FAILURE IMMINENT",
    "BIOS CORRUPTED",
    "UNKNOWN SOFTWARE EXCEPTION"
]

# ================= ПУТИ =================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================= ЗВУК (ПО ОЧЕРЕДИ) =================
def play_sound():
    try:
        pygame.mixer.init()
        sounds = ["1.wav", "2.wav"]
        
        while True:
            for s in sounds:
                path = resource_path(s)
                if os.path.exists(path):
                    pygame.mixer.music.load(path)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.1)
                else:
                    time.sleep(1)
    except Exception as e:
        print(f"Sound error: {e}")

# ================= ЛОГИКА ХАОСА =================
def spawn_error_window(root):
    win = tk.Toplevel(root)
    win.title("System Error")
    win.configure(bg="red")
    
    x = random.randint(0, root.winfo_screenwidth() - 300)
    y = random.randint(0, root.winfo_screenheight() - 150)
    win.geometry(f"300x150+{x}+{y}")
    
    msg = random.choice(ERROR_TEXTS)
    tk.Label(win, text=msg, bg="red", fg="white", font=("Consolas", 14, "bold")).pack(expand=True)
    win.protocol("WM_DELETE_WINDOW", lambda: None)

def flying_images(root):
    try:
        imgs = []
        assets_path = resource_path("assets")
        
        if not os.path.exists(assets_path):
            print("Assets folder not found.")
            return
            
        for file in os.listdir(assets_path):
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                img = Image.open(os.path.join(assets_path, file))
                img = img.resize((random.randint(150, 300), random.randint(150, 300)))
                imgs.append(ImageTk.PhotoImage(img))
        
        if not imgs: 
            return

        screen_w = root.winfo_screenwidth()
        screen_h = root.winfo_screenheight()
        flying_windows = []
        
        for _ in range(12): # 12 летающих окон
            win = tk.Toplevel(root)
            win.overrideredirect(True)
            win.attributes("-topmost", True)
            
            # Случайная стартовая позиция
            start_x = random.randint(0, screen_w - 200)
            start_y = random.randint(0, screen_h - 200)
            win.geometry(f"+{start_x}+{start_y}")
            
            lbl = tk.Label(win, bg="black") 
            lbl.pack()
            flying_windows.append([win, lbl, random.choice(imgs)])

        # Скорость для каждого окна (от 5 до 15 пикселей за кадр)
        velocities = [[random.choice([-1, 1]) * random.randint(5, 15), 
                       random.choice([-1, 1]) * random.randint(5, 15)] for _ in flying_windows]

        def move():
            for i, data in enumerate(flying_windows):
                win, lbl, img = data
                
                # Случайная смена картинки
                if random.random() < 0.1:
                    lbl.config(image=random.choice(imgs))
                
                x = win.winfo_x()
                y = win.winfo_y()
                
                x += velocities[i][0]
                y += velocities[i][1]
                
                # Отскок от краев
                if x <= 0 or x >= screen_w - 150: 
                    velocities[i][0] *= -1
                if y <= 0 or y >= screen_h - 150: 
                    velocities[i][1] *= -1
                
                win.geometry(f"+{x}+{y}")
            
            root.after(20, move)

        move()
    except Exception as e:
        print(f"Image error: {e}")

def chaos_loop(root):
    while True:
        spawn_error_window(root)
        time.sleep(0.25) # Интервал ошибок

# ================= ЗАПУСК =================
def main():
    root = tk.Tk()
    root.withdraw() # Скрываем основное окно
    
    # Запуск музыки
    threading.Thread(target=play_sound, daemon=True).start()
    
    # Запуск картинок
    root.after(100, lambda: flying_images(root))
    
    # Запуск ошибок
    threading.Thread(target=chaos_loop, args=(root,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
