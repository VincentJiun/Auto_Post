import threading
import queue
import time
import tkinter as tk
from tkinter import ttk

from crawler import Facebook_Crawler


# class Facebook_Crawler:
#     def post(self, url, fb_acc, fb_pwd, status_queue):
#         print(f"開始爬取 {url} 使用帳號: {fb_acc}")
#         for i in range(5):  # 模擬爬蟲任務
#             time.sleep(1)  # 模擬任務耗時
#             status_queue.put(f"進度: {i + 1}/5")  # 傳遞進度到隊列
#         status_queue.put("爬蟲完成")
#         print("爬蟲已完成")


class PsotStatus:
    def __init__(self, root, status_queue):
        self.status_queue = status_queue
        self.toplevel = tk.Toplevel(root)
        self.toplevel.title("爬蟲狀態")
        self.toplevel.geometry("300x200")

        # 設置標籤來顯示狀態
        self.label = ttk.Label(self.toplevel, text="正在等待爬蟲更新...", anchor="center")
        self.label.pack(pady=20, padx=10, expand=True)

        # 設置停止按鈕
        self.stop_button = ttk.Button(self.toplevel, text="關閉", command=self.close)
        self.stop_button.pack(pady=10)

        self.running = True
        self.update_status()  # 開始更新狀態

    def update_status(self):
        """更新視窗中的爬蟲狀態"""
        if self.running:
            try:
                # 從隊列中獲取最新狀態
                status = self.status_queue.get_nowait()
                self.label.config(text=status)  # 更新標籤文字
            except queue.Empty:
                pass
            # 設定一個定時器來重複調用自身
            self.toplevel.after(100, self.update_status)

    def close(self):
        """關閉視窗"""
        self.running = False
        self.toplevel.destroy()


class Controller:
    def __init__(self):
        self.fb_acc = "egg790508@hotmail.com"
        self.fb_pwd = "Eggsy7955168~"
        self.status_queue = queue.Queue()
        self.root = tk.Tk()
        self.root.withdraw()  # 隱藏主視窗

    def fb_post(self):
        """執行爬蟲"""
        URL = 'https://www.facebook.com/'
        fb_crawler = Facebook_Crawler()
        fb_crawler.post(URL, self.fb_acc, self.fb_pwd, self.status_queue)

    def run_post(self):
        """啟動視窗和爬蟲執行緒"""
        # 創建 PsotStatus 視窗
        PsotStatus(self.root, self.status_queue)

        # 啟動爬蟲執行緒
        thread_crawler = threading.Thread(target=self.fb_post)
        thread_crawler.start()

        # 啟動 Tkinter 主迴圈
        self.root.mainloop()


# 執行主程式
if __name__ == "__main__":
    controller = Controller()
    controller.run_post()
