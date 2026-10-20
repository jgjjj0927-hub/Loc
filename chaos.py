# language: Python, file: chaos.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import threading
import time
import os
import sys
import winsound

# ================= НАСТРОЙКИ =================
SCREEN_W = 1920  # Можно не менять, скрипт сам подстроится под экран
SCREEN_H = 1080
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

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================= ЛОГИКА ХАОСА =================
def spawn_error_window():
    """Создает окно с ошибкой в случайном месте."""
    win = tk.Toplevel()
    win.title("System Error")
    win.configure(bg="red")
    
    # Рандомная позиция
    x = random.randint(0, 1000)
    y = random.randint(0, 800)
    win.geometry(f"300x150+{x}+{y}")
    
    # Текст ошибки
    msg = random.choice(ERROR_TEXTS)
    tk.Label(win, text=msg, bg="red", fg="white", font=("Consolas", 14, "bold")).pack(expand=True)
    
    # Чтобы окна не закрывались сразу
    win.protocol("WM_DELETE_WINDOW", lambda: None)

def flying_images(root):
    """Создает прозрачные окна с картинками, которые летают."""
    try:
        # Загружаем картинки из папки assets
        imgs = []
        for file in os.listdir(resource_path("assets")):
            if file.endswith((".png", ".jpg", ".jpeg")):
                img = Image.open(resource_path(f"assets/{file}"))
                img = img.resize((random.randint(100, 300), random.randint(100, 300)))
                imgs.append(ImageTk.PhotoImage(img))
        
        if not imgs:
            return

        # Создаем окна для картинок
        flying_windows = []
        for _ in range(15): # 15 летающих окон
            win = tk.Toplevel(root)
            win.overrideredirect(True) # Убираем рамки и заголовок
            win.attributes("-topmost", True) # Поверх всех окон
            
            lbl = tk.Label(win, bg="black") # Фон окна (можно сделать прозрачным через -transparentcolor)
            lbl.pack()
            flying_windows.append((win, lbl, random.choice(imgs)))

        # Анимация полета
        velocities = [ [random.choice([-15, 15]), random.choice([-15, 15])] for _ in flying_windows ]

        def move():
            for i, (win, lbl, img) in enumerate(flying_windows):
                # Меняем картинку (мигание)
                if random.random() < 0.3:
                    lbl.config(image=random.choice(imgs))
                
                # Получаем текущую позицию
                x = win.winfo_x()
                y = win.winfo_y()
                
                # Обновляем скорость
                x += velocities[i][0]
                y += velocities[i][1]
                
                # Отбиваемся от краев экрана
                if x < 0 or x > SCREEN_W - 100:
                    velocities[i][0] *= -1
                if y < 0 or y > SCREEN_H - 100:
                    velocities[i][1] *= -1
                
                win.geometry(f"+{x}+{y}")
            
            root.after(20, move) # Рекурсивный вызов для анимации

        move()
    except Exception as e:
        print(f"Image error: {e}")

def chaos_loop(root):
    """Бесконечно создает окна с ошибками."""
    while True:
        spawn_error_window()
        time.sleep(0.5) # Интервал между окнами

def play_sound():
    """Играет звук в цикле."""
    try:
        sound_path = resource_path("scream.mp3")
        if os.path.exists(sound_path):
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    except Exception as e:
        print(f"Sound error: {e}")

# ================= ЗАПУСК =================
def main():
    root = tk.Tk()
    root.withdraw() # Скрываем главное окно
    
    # Получаем реальные размеры экрана
    global SCREEN_W, SCREEN_H
    SCREEN_W = root.winfo_screenwidth()
    SCREEN_H = root.winfo_screenheight()

    # Поток для музыки
    threading.Thread(target=play_sound, daemon=True).start()
    
    # Запуск летающих картинок
    root.after(100, lambda: flying_images(root))
    
    # Поток для спавна ошибок (или через root.after)
    threading.Thread(target=chaos_loop, args=(root,), daemon=True).start()

    root.mainloop()

if __name__ == "__main__":
    main()
