import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox

from PIL import Image

from config import accounts_name, account_select_by_name, add_config_account, delete_config_account, modify_config_account
from crawler import Facebook_Crawler

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
        self.main.show_page('settings')

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
        self.btn_facebook = ctk.CTkButton(self.frame_container, text='  Facebook', font=('Times', 20, 'bold'), text_color='#000000', fg_color="#FFCBB3", width=30, image=img_facebook, hover_color="#BEBEBE", corner_radius=0, command=lambda: self.master.main.show_page('facebook'))
        self.btn_facebook.place(relx=0.5, rely=0.2, relwidth=0.8, relheight=0.05, anchor='center')
        # Instagram
        img_instagram = ctk.CTkImage(light_image=Image.open(f'./images/instagram.png'), dark_image=Image.open(f'./images/instagram.png'), size=(32,32))
        self.btn_instagram = ctk.CTkButton(self.frame_container, text='  Instagram', font=('Times', 20, 'bold'), text_color='#000000', fg_color="#FFCBB3", width=30, image=img_instagram, hover_color="#BEBEBE", corner_radius=0, command=lambda: self.master.main.show_page('instagram'))
        self.btn_instagram.place(relx=0.5, rely=0.28, relwidth=0.8, relheight=0.05, anchor='center')
        # Button Settings
        img_setting = ctk.CTkImage(light_image=Image.open(f'./images/settings.png'), dark_image=Image.open(f'./images/settings.png'), size=(32,32))
        self.btn_settings = ctk.CTkButton(self.frame_container, text='  設          定', font=('微軟正黑體', 20, 'bold'), text_color='#000000', fg_color="#FFCBB3", width=30, image=img_setting, hover_color="#BEBEBE", corner_radius=0, command=lambda: self.master.main.show_page('settings'))
        self.btn_settings.place(relx=0.5, rely=0.9, relwidth=0.8, relheight=0.05, anchor='center')
        # Label Version
        self.lab_version = ctk.CTkLabel(self.frame_container, text='v 1.0.0', font=('Times New Roman', 16, 'bold'), text_color='#000000')
        self.lab_version.place(relx=0.5, rely=0.95, relwidth=1, relheight=0.05, anchor='center')
        # Event Configure
        self.label_robot.bind("<Configure>", lambda event: self._image_on_configure(event, self.label_robot, 'chatbot.png', 2, 3))

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
        # TopLevel 初始化
        # self.top_modify =None

    def show_page(self, page_name):
        # 清除当前页面内容
        for widget in self.frame_container.winfo_children():
            widget.destroy()

        # 根据页面标识符显示内容
        if page_name == 'facebook':
            self.create_fb_page()
        elif page_name == 'instagram':
            self.create_ig_page()
        elif page_name == 'settings':
            self.create_settings_page()
    
    def create_fb_page(self):
        # title
        self.lab_fb_title = ctk.CTkLabel(self.frame_container, font=('微軟正黑體', 20, 'bold'), text="Facebook 發文機器人")
        self.lab_fb_title.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.08, anchor='center')
        # FB 帳號選項
        self.lab_select_acc = ctk.CTkLabel(self.frame_container, font=('微軟正黑體', 16, 'bold'), text='請選擇帳號:', anchor='w')
        self.lab_select_acc.place(relx=0.1, rely=0.1, relwidth=0.12, relheight=0.04, anchor='w')
        self.combo_fb_acc = ctk.CTkComboBox(self.frame_container, justify='left', state='readonly', command=self.fb_account_selected_by_name)
        self.combo_fb_acc.place(relx=0.23, rely=0.1, relwidth=0.15, relheight=0.04, anchor='w')
        self.refresh_combo_accounts('FB', self.combo_fb_acc)
        # 帳戶資訊
        self.lab_fb_acc_info = ctk.CTkLabel(self.frame_container, font=('微軟正黑體', 14, 'bold'), text='', anchor='w')
        self.lab_fb_acc_info.place(relx=0.4, rely=0.1, relwidth=0.6, relheight=0.04, anchor='w')
        # 貼文內容
        self.lab_fb_post = ctk.CTkLabel(self.frame_container, font=('微軟正黑體', 18, 'bold'), text="貼文內容:", anchor='w')
        self.lab_fb_post.place(relx=0.1, rely=0.2, relwidth=0.2, relheight=0.08, anchor='w')
        self.txt_fb_post = ctk.CTkTextbox(self.frame_container, font=('微軟正黑體', 16))
        self.txt_fb_post.place(relx=0.1, rely=0.25, relwidth=0.8, relheight=0.3, anchor='nw')

        # 開始發文
        self.btn_post = ctk.CTkButton(self.frame_container, font=('微軟正黑體', 18, 'bold'), text="開始貼文", command=self.fb_post)
        self.btn_post.place(relx=0.5, rely=0.7, relwidth=0.15, relheight=0.05, anchor='nw')

    def fb_account_selected_by_name(self, choice):
        account, index = account_select_by_name('FB', choice)
        self.acc = account[0]['email']
        self.pwd = account[0]['password']
        group = account[0]['group']
        txt = f'帳號:{self.acc}  密碼:{self.pwd}'
        self.lab_fb_acc_info.configure(text=txt)

    def fb_post(self):
        url = 'https://www.facebook.com/'
        fb_crawler = Facebook_Crawler()
        fb_crawler.post(url, self.acc, self.pwd)

    def create_ig_page(self):
        self.fb = ctk.CTkTextbox(self.frame_container, font=('微軟正黑體', 16))
        self.fb.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.3, anchor='center')

    def create_settings_page(self):
        # Facebook 帳號設定
        self.lab_fb_account = ctk.CTkLabel(self.frame_container, text='Facebook帳號設定', font=('微軟正黑體', 22, 'bold'))
        self.lab_fb_account.place(relx=0.15, rely=0.05, relwidth=0.3, relheight=0.08, anchor='center')
        # FB 帳號選項
        self.combo_fb_account = ctk.CTkComboBox(self.frame_container, justify='left', state='readonly', command=self.fb_account_selected)
        self.combo_fb_account.place(relx=0.1, rely=0.1, relwidth=0.15, relheight=0.04, anchor='center')
        self.refresh_combo_accounts('FB', self.combo_fb_account)
        # button 清除/刪除/修改
        self.btn_fb_clear =  ctk.CTkButton(self.frame_container, text='清空', text_color='#000000', font=('微軟正黑體', 16, 'bold'), command=lambda: self.inputs_clear('FB'))
        self.btn_fb_clear.place(relx=0.75, rely=0.1, relwidth=0.07, relheight=0.04, anchor='center')
        self.btn_fb_modify = ctk.CTkButton(self.frame_container, text='修改', text_color='#000000', font=('微軟正黑體', 16, 'bold'), state='disabled', command=lambda: self.modify_account('FB', self.combo_fb_account))
        self.btn_fb_modify.place(relx=0.85, rely=0.1, relwidth=0.07, relheight=0.04, anchor='center')
        self.btn_fb_delete = ctk.CTkButton(self.frame_container, text='刪除', font=('微軟正黑體', 16, 'bold'), state='disabled', fg_color='red', command=lambda: self.delete_account('FB', self.combo_fb_account))
        self.btn_fb_delete.place(relx=0.95, rely=0.1, relwidth=0.07, relheight=0.04, anchor='center')
        # 新增FB帳號/密碼
        self.lab_name_fb = ctk.CTkLabel(self.frame_container, text='名稱:', text_color='#000000', font=('微軟正黑體', 16, 'bold'))
        self.lab_name_fb.place(relx=0.025, rely=0.15, relwidth=0.05, relheight=0.04, anchor='center')
        self.entry_name_fb = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16))
        self.entry_name_fb.place(relx=0.175, rely=0.15, relwidth=0.23, relheight=0.04, anchor='center')
        self.lab_acc_fb = ctk.CTkLabel(self.frame_container, text='帳號:', text_color='#000000', font=('微軟正黑體', 16, 'bold'))
        self.lab_acc_fb.place(relx=0.325, rely=0.15, relwidth=0.05, relheight=0.04, anchor='center')
        self.entry_acc_fb = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16))
        self.entry_acc_fb.place(relx=0.475, rely=0.15, relwidth=0.23, relheight=0.04, anchor='center')
        self.lab_pwd_fb = ctk.CTkLabel(self.frame_container, text='密碼:', text_color='#000000', font=('微軟正黑體', 16, 'bold'))
        self.lab_pwd_fb.place(relx=0.625, rely=0.15, relwidth=0.05, relheight=0.04, anchor='center')
        self.entry_pwd_fb = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16), show="*")
        self.entry_pwd_fb.place(relx=0.775, rely=0.15, relwidth=0.23, relheight=0.04, anchor='center')
        self.btn_fb_add = ctk.CTkButton(self.frame_container, text='新增', text_color='#000000', font=('微軟正黑體', 16, 'bold'), fg_color='green', command=lambda: self.create_account(self.entry_name_fb, 'FB', self.entry_acc_fb, self.entry_pwd_fb, self.combo_fb_account, self.entry_fb_group))
        self.btn_fb_add.place(relx=0.95, rely=0.15, relwidth=0.07, relheight=0.04, anchor='center')
        # FB Group Text
        self.lab_fb_group =  ctk.CTkLabel(self.frame_container, text='社團編號:', font=('微軟正黑體', 18, 'bold'))
        self.lab_fb_group.place(relx=0.08, rely=0.2, relwidth=0.1, relheight=0.04, anchor='center')
        self.entry_fb_group = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16))
        self.entry_fb_group.place(relx=0.55, rely=0.2, relwidth=0.8, relheight=0.04, anchor='center')
        
        # Horizontal Line
        sep = ttk.Separator(self.frame_container, orient='horizontal')
        sep.place(relx=0.5, rely=0.5, relwidth=0.95, anchor='center')
        # Instagram 帳號設定
        self.lab_ig_account = ctk.CTkLabel(self.frame_container, text='Instagram帳號設定', font=('微軟正黑體', 22, 'bold'))
        self.lab_ig_account.place(relx=0.15, rely=0.55, relwidth=0.3, relheight=0.06, anchor='center')
        # IG 帳號選項
        self.combo_ig_account = ctk.CTkComboBox(self.frame_container, justify='left', state='readonly', command=self.ig_account_selected)
        self.combo_ig_account.place(relx=0.1, rely=0.6, relwidth=0.15, relheight=0.04, anchor='center')
        self.refresh_combo_accounts('IG', self.combo_ig_account)
        # button 刪除/修改
        self.btn_ig_clear =  ctk.CTkButton(self.frame_container, text='清空', text_color='#000000', font=('微軟正黑體', 16, 'bold'), command=lambda: self.inputs_clear('IG'))
        self.btn_ig_clear.place(relx=0.75, rely=0.6, relwidth=0.07, relheight=0.04, anchor='center')
        self.btn_ig_modify = ctk.CTkButton(self.frame_container, text='修改', text_color='#000000', font=('微軟正黑體', 16, 'bold'), state='disabled', command=lambda: self.modify_account('IG', self.combo_ig_account))
        self.btn_ig_modify.place(relx=0.85, rely=0.6, relwidth=0.07, relheight=0.04, anchor='center')
        self.btn_ig_delete = ctk.CTkButton(self.frame_container, text='刪除', font=('微軟正黑體', 16, 'bold'), state='disabled', fg_color='red', command=lambda: self.delete_account('IG', self.combo_ig_account))
        self.btn_ig_delete.place(relx=0.95, rely=0.6, relwidth=0.07, relheight=0.04, anchor='center')
        # 新增IG帳號/密碼
        self.lab_name_ig = ctk.CTkLabel(self.frame_container, text='名稱:', text_color='#000000', font=('微軟正黑體', 16, 'bold'))
        self.lab_name_ig.place(relx=0.025, rely=0.65, relwidth=0.05, relheight=0.04, anchor='center')
        self.entry_name_ig = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16))
        self.entry_name_ig.place(relx=0.175, rely=0.65, relwidth=0.23, relheight=0.04, anchor='center')
        self.lab_acc_ig = ctk.CTkLabel(self.frame_container, text='帳號:', text_color='#000000', font=('微軟正黑體', 16, 'bold'))
        self.lab_acc_ig.place(relx=0.325, rely=0.65, relwidth=0.05, relheight=0.04, anchor='center')
        self.entry_acc_ig = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16))
        self.entry_acc_ig.place(relx=0.475, rely=0.65, relwidth=0.23, relheight=0.04, anchor='center')
        self.lab_pwd_ig = ctk.CTkLabel(self.frame_container, text='密碼:', text_color='#000000', font=('微軟正黑體', 16, 'bold'))
        self.lab_pwd_ig.place(relx=0.625, rely=0.65, relwidth=0.05, relheight=0.04, anchor='center')
        self.entry_pwd_ig = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16), show="*")
        self.entry_pwd_ig.place(relx=0.775, rely=0.65, relwidth=0.23, relheight=0.04, anchor='center')
        self.btn_ig_add = ctk.CTkButton(self.frame_container, text='新增', text_color='#000000', font=('微軟正黑體', 16, 'bold'), fg_color='green', command=lambda: self.create_account(self.entry_name_ig, 'IG', self.entry_acc_ig, self.entry_pwd_ig, self.combo_ig_account, self.entry_ig_group))
        self.btn_ig_add.place(relx=0.95, rely=0.65, relwidth=0.07, relheight=0.04, anchor='center')
        # FB Group Text
        self.lab_ig_group =  ctk.CTkLabel(self.frame_container, text='社團編號:', font=('微軟正黑體', 18, 'bold'))
        self.lab_ig_group.place(relx=0.08, rely=0.7, relwidth=0.1, relheight=0.04, anchor='center')
        self.entry_ig_group = ctk.CTkEntry(self.frame_container, font=('微軟正黑體', 16))
        self.entry_ig_group.place(relx=0.55, rely=0.7, relwidth=0.8, relheight=0.04, anchor='center')

    def refresh_combo_accounts(self, acc_type, widget):
        names = accounts_name(acc_type)
        widget.configure(values=names)

    def fb_account_selected(self, choice):
        account, index = account_select_by_name('FB', choice)
        acc = account[0]['email']
        pwd = account[0]['password']
        group = account[0]['group']
        # self.lab_fb_account.configure(text=f'名稱:{choice}  帳號:{acc}    密碼:{pwd}')
        self.entry_name_fb.delete(0, 'end')
        self.entry_name_fb.insert(0, str(choice))
        self.entry_acc_fb.delete(0, 'end')
        self.entry_acc_fb.insert(0, str(acc))
        self.entry_pwd_fb.delete(0, 'end')
        self.entry_pwd_fb.insert(0, str(pwd))  
        self.entry_fb_group.delete(0,'end')
        self.entry_fb_group.insert(0, str(group))
        self.btn_fb_add.configure(state='disabled') 
        self.btn_fb_delete.configure(state='normal')
        self.btn_fb_modify.configure(state='normal')    

    def ig_account_selected(self, choice):
        account, index = account_select_by_name('IG', choice)
        acc = account[0]['email']
        pwd = account[0]['password']
        group = account[0]['group']
        # self.lab_ig_account.configure(text=f'帳號:{acc}    密碼:{pwd}')
        self.entry_name_ig.delete(0, 'end')
        self.entry_name_ig.insert(0, str(choice))
        self.entry_acc_ig.delete(0, 'end')
        self.entry_acc_ig.insert(0, str(acc))
        self.entry_pwd_ig.delete(0, 'end')
        self.entry_pwd_ig.insert(0, str(pwd))  
        self.entry_ig_group.delete(0,'end')
        self.entry_ig_group.insert(0, str(group))
        self.btn_ig_add.configure(state='disabled') 
        self.btn_ig_delete.configure(state='normal') 
        self.btn_ig_modify.configure(state='normal')

    def inputs_clear(self, acc_type):
        if acc_type == 'FB':
            self.entry_name_fb.delete(0, 'end')
            self.entry_acc_fb.delete(0, 'end')
            self.entry_pwd_fb.delete(0, 'end')
            self.entry_fb_group.delete(0, 'end')
            self.btn_fb_add.configure(state='normal') 
            self.btn_fb_delete.configure(state='disabled') 
            self.btn_fb_modify.configure(state='disabled')
        elif acc_type == 'IG':
            self.entry_name_ig.delete(0, 'end')
            self.entry_acc_ig.delete(0, 'end')
            self.entry_pwd_ig.delete(0, 'end')
            self.entry_ig_group.delete(0, 'end')
            self.btn_ig_add.configure(state='normal')  
            self.btn_ig_delete.configure(state='disabled')
            self.btn_ig_modify.configure(state='disabled')
        
    def create_account(self, input_name, acc_type, input_acc, input_pwd, widget, input_group):
        if input_name.get()=='' or input_acc.get()=='' or input_pwd.get()=='':
            messagebox.showwarning(title='資料空白', message='請確認輸入框是否空白!')
        else:
            data = f'name={input_name.get()};type={acc_type};email={input_acc.get()};password={input_pwd.get()};group={input_group.get()}'
            add_config_account(data)
            self.refresh_combo_accounts(acc_type, widget)
            messagebox.showinfo(title='新增資料成功', message='新增資料成功!')
            input_name.delete(0, 'end')
            input_acc.delete(0, 'end')
            input_pwd.delete(0, 'end')
            input_group.delete(0, 'end')

    def delete_account(self, acc_type, widget):
        acc = widget.get()
        msg = messagebox.askyesno(title='刪除帳號?', message=f'確定刪除{acc}的帳號設定嗎?')
        if msg:
            delete_config_account(acc_type, acc)
            self.refresh_combo_accounts(acc_type, widget)
            self.inputs_clear(acc_type)

    def modify_account(self, acc_type, widget):
        acc = widget.get()
        data = ''
        if acc_type == 'FB':
            if self.entry_name_fb.get() == '' or self.entry_acc_fb.get() == '' or self.entry_pwd_fb.get() == '':
                messagebox.showwarning(title='資料空白', message='請確認輸入框是否空白!')
            else:
                data = f'name={self.entry_name_fb.get()};type={acc_type};email={self.entry_acc_fb.get()};password={self.entry_pwd_fb.get()};group={self.entry_fb_group.get()}\n'
        elif acc_type == 'IG':
            if self.entry_name_ig.get() == '' or self.entry_acc_ig.get() == '' or self.entry_pwd_ig.get() == '':
                messagebox.showwarning(title='資料空白', message='請確認輸入框是否空白!')
            else:
                data = f'name={self.entry_name_ig.get()};type={acc_type};email={self.entry_acc_ig.get()};password={self.entry_pwd_ig.get()};group={self.entry_ig_group.get()}\n'

        modify_config_account(acc_type, acc, data)
        self.refresh_combo_accounts(acc_type, widget)
        messagebox.showinfo(title='資料修改成功', message='資料修改成功!')
        self.inputs_clear(acc_type)


# class AccountModify(ctk.CTkToplevel):
#     def __init__(self, master):
#         super().__init__(master)
#         self.attributes("-topmost", True)  # 視窗置頂
#         self.geometry("600x400")
#         self.resizable(False, False)
#         self.title("修改帳號")

#         self.protocol("WM_DELETE_WINDOW", self.on_close)  # 監聽關閉視窗 事件

#     def on_close(self):
#         self.master.top_add = None  # 重置父窗口的引用
#         self.destroy()

#     def create_page(self, acc_type, acc):
#         self.lab_acc = ctk.CTkLabel(self, text=f'type={acc_type}, name={acc}', text_color='#000000', font=('微軟正黑體', 24, 'bold'))
#         self.lab_acc.place(relx=0.5, rely=0.05, relwidth=0.5, relheight=0.1, anchor='center')

if __name__ == '__main__':
    app = App()
    app.index()
    app.mainloop()
