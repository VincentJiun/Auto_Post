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
        self.frame_container = ctk.CTkFrame(self, fg_color='#FFF4C1', corner_radius=0, border_color='#FFF4C1')
        self.frame_container.pack(fill='both', expand=True)

    def create_page(self):
        # Image Robot Logo
        self.label_robot = ctk.CTkLabel(self.frame_container, text='Auto Post Robot', compound='top', font=('Times', 24, 'bold'))
        self.label_robot.place(relx=0.5, rely=0.075, relwidth=0.8, relheight=0.15, anchor='center')
        # Facebook
        img_facebook = ctk.CTkImage(light_image=Image.open(f'./images/facebook.png'), dark_image=Image.open(f'./images/facebook.png'), size=(32,32))
        self.btn_facebook = ctk.CTkButton(self.frame_container, text='  Facebook', font=('Times', 20, 'bold'), text_color='#000000', fg_color="#FFCBB3", width=30, image=img_facebook, hover_color="#BEBEBE", corner_radius=0)
        self.btn_facebook.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.05, anchor='center')
        # Instagram
        img_instagram = ctk.CTkImage(light_image=Image.open(f'./images/instagram.png'), dark_image=Image.open(f'./images/instagram.png'), size=(32,32))
        self.btn_instagram = ctk.CTkButton(self.frame_container, text='  Instagram', font=('Times', 20, 'bold'), text_color='#000000', fg_color="#FFCBB3", width=30, image=img_instagram, hover_color="#BEBEBE", corner_radius=0)
        self.btn_instagram.place(relx=0.5, rely=0.28, relwidth=0.8, relheight=0.05, anchor='center')
        # Button Settings
        img_setting = ctk.CTkImage(light_image=Image.open(f'./images/settings.png'), dark_image=Image.open(f'./images/settings.png'), size=(32,32))
        self.btn_settings = ctk.CTkButton(self.frame_container, text='  設          定', font=('微軟正黑體', 20, 'bold'), text_color='#000000', fg_color="#FFCBB3", width=30, image=img_setting, hover_color="#BEBEBE", corner_radius=0)
        self.btn_settings.place(relx=0.5, rely=0.9, relwidth=0.8, relheight=0.05, anchor='center')
        # Label Version
        self.lab_version = ctk.CTkLabel(self.frame_container, text='v 1.0.0', font=('Times New Roman', 16, 'bold'), text_color='#000000')
        self.lab_version.place(relx=0.5, rely=0.95, relwidth=1, relheight=0.05, anchor='center')



        # Event Configure
        self.label_robot.bind("<Configure>", lambda event: self._image_on_configure(event, self.label_robot, 'chatbot.png', 2, 3))
        # self.btn_settings.bind("<Configure>", lambda event: self._image_on_configure(event, self.btn_settings, 'settings.png', 1, 1))

    def _image_on_configure(self, enevt, object, path, resize_width, resize_height):
        width, height = object.winfo_width(), object.winfo_height()
        image = ctk.CTkImage(light_image=Image.open(f'./images/{path}'), dark_image=Image.open(f'./images/{path}'), size=(int(width/resize_width),int(height/resize_height)))
        object.configure(image=image)
        



class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Frame Container
        self.frame_container = ctk.CTkFrame(self, fg_color='#FFC78E', corner_radius=0, border_color='#FFC78E')
        self.frame_container.pack(fill='both', expand=True)

    def create_page(self):
        pass

if __name__ == '__main__':
    app = App()
    app.index()
    app.mainloop()
