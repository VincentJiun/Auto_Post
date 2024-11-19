import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('1024x600')
        self.title('Auto Post FB/IG')
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        ctk.set_appearance_mode("light")






if __name__ == '__main__':
    app = App()
