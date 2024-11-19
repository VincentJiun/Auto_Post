import customtkinter as ctk

from PIL import Image

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('1024x768')
        self.title('Auto Post Robot For FB/IG')
        self.iconbitmap('./images/icon.ico')
        ctk.set_appearance_mode("light")

    def index(self):
        self.nav = Nav(self)
        self.nav.grid(row=0, column=0, sticky='NSEW')
        self.nav.create_page()
        self.main = MainFrame(self)
        self.main.grid(row=0, column=1, sticky='NSEW')
        self.main.create_page()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=1)

class Nav(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # Frame Container
        self.frame_container = ctk.CTkFrame(self, fg_color='red', corner_radius=0, border_color='red')
        self.frame_container.pack(fill='both', expand=True)

    def create_page(self):
        # Image Robot
        self.label_robot = ctk.CTkLabel(self.frame_container, text='Auto Post Robot', compound='top', font=('Times', 24, 'bold'))
        self.label_robot.place(relx=0.5, rely=0.075, relwidth=0.8, relheight=0.15, anchor='center')
        # Button Settings
        self.btn_settings = ctk.CTkButton(self.frame_container, text='test', corner_radius=0, compound='left', font=('Times', 20, 'bold'))
        self.btn_settings.place(relx=0.5, rely=0.8, relwidth=0.8, relheight=0.05, anchor='center')


        # Event Configure
        self.label_robot.bind("<Configure>", lambda event: self._image_on_configure(event, self.label_robot, 'chatbot.png', 3, 4))

    def _image_on_configure(self, enevt, object, path, resize_width, resize_height):
        width, height = object.winfo_width(), object.winfo_height()
        image = ctk.CTkImage(light_image=Image.open(f'./images/{path}'), dark_image=Image.open(f'./images/{path}'), size=(int(width/resize_width),int(height/resize_height)))
        object.configure(image=image)
        



class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame Container
        self.frame_container = ctk.CTkFrame(self, fg_color='#B8B8DC', corner_radius=0, border_color='#B8B8DC')
        self.frame_container.pack(fill='both', expand=True)

    def create_page(self):
        pass

if __name__ == '__main__':
    app = App()
    app.index()
    app.mainloop()
