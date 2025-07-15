import tkinter as tk
from tkinter import messagebox
import pyautogui
import threading
import keyboard

# 主程式類
class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自動按鍵或點擊工具")
        self.root.geometry("400x300")
        
        self.running = False  # 控制自動執行的狀態
        self.mode = None  # 用來存儲目前模式（滑鼠或鍵盤）

        # 建立主UI
        self.create_widgets()

    def create_widgets(self):
        # 模式選擇
        tk.Label(self.root, text="選擇模式:").pack(pady=5)
        self.mode_var = tk.StringVar(value="mouse")  # 預設為滑鼠模式
        self.mouse_mode_button = tk.Radiobutton(self.root, text="滑鼠模式", variable=self.mode_var, value="mouse")
        self.mouse_mode_button.pack(pady=5)
        self.keyboard_mode_button = tk.Radiobutton(self.root, text="鍵盤模式", variable=self.mode_var, value="keyboard")
        self.keyboard_mode_button.pack(pady=5)

        # 鍵盤模式輸入框
        tk.Label(self.root, text="輸入鍵盤符號:").pack(pady=5)
        self.key_entry = tk.Entry(self.root)
        self.key_entry.pack(pady=5)

        # 開始提示
        tk.Label(self.root, text="按 ` 開始，按 ESC 停止").pack(pady=10)

        # 開始執行按鈕
        self.start_button = tk.Button(self.root, text="開始執行", command=self.start_action)
        self.start_button.pack(pady=10)

        # 停止執行按鈕
        self.stop_button = tk.Button(self.root, text="停止執行", command=self.stop_action)
        self.stop_button.pack(pady=10)

    def start_action(self):
        # 根據選擇的模式準備執行操作，但不立即執行，等待按下 ` 開始
        self.mode = self.mode_var.get()
        if self.mode == "mouse":
            threading.Thread(target=self.wait_for_start, args=(self.auto_mouse_click,), daemon=True).start()
        elif self.mode == "keyboard":
            key = self.key_entry.get().strip()
            if key:
                threading.Thread(target=self.wait_for_start, args=(self.auto_key_press, key), daemon=True).start()
            else:
                messagebox.showerror("錯誤", "請輸入鍵盤符號")
        else:
            messagebox.showerror("錯誤", "請選擇模式")

    def stop_action(self):
        # 停止執行
        self.running = False

    def wait_for_start(self, action_function, *args):
        # 等待按下 ` 開始執行
        self.running = False
        while not keyboard.is_pressed("`"):  # 等待按下 `
            pass
        self.running = True
        action_function(*args)

    def auto_mouse_click(self):
        # 自動滑鼠左鍵點擊
        while self.running:
            pyautogui.click()
            if keyboard.is_pressed("esc"):  # 偵測 ESC 按鍵退出
                self.running = False
                break

    def auto_key_press(self, key):
        # 自動按鍵
        while self.running:
            pyautogui.press(key)
            if keyboard.is_pressed("esc"):  # 偵測 ESC 按鍵退出
                self.running = False
                break


# 主程式入口
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
