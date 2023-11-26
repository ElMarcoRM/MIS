from tkinter import *
from tkinter import ttk   
from database import DatabaseAuth
import bcrypt

db = DatabaseAuth()

class AdminPanel:
    def __init__(self):
        self.root = Tk()
        self.root.title('My App')
        self.root.geometry('1920x1080')
        active_sessions = db.sel_session_id()
        self.active_sessions = active_sessions

        Frame = ttk.Frame(borderwidth=1, relief=SOLID)
        Frame.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.session_listbox = Listbox(Frame)
        self.session_listbox.pack(side="top", fill="x")
        self.refresh_button = ttk.Button(Frame, text="Обновить", command=self.show_active_sessions).pack(side="top", fill="x", padx=10, pady=5)
        self.terminate_button = ttk.Button(Frame, text="Остановить сессию", command=self.terminate_session).pack(side="top", fill="x", padx=10, pady=5)
        self.register_new_user = ttk.Button(Frame, text = "Регистрация нового пользователя", command = self.register_new_users).pack(side="top", fill="x", padx=10, pady=5)
        self.back_button = ttk.Button(Frame, text = "Назад", command=self.back).pack(side="top", fill="x", padx=10, pady=5)
        
    def register_new_users(self):
        self.root.destroy()
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')

        Frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10,5])
        Frame.place(relx=0.5, rely=0.3, anchor=CENTER)
 
        signInTXT = Label(Frame, text='Регистрация нового пользователя').pack(pady=5)

        FIO = ["Фамилия", "Имя", "Отчество"]
        FIO_entries = []
        for i in FIO:
            FIO_label = Label(Frame,text=i).pack(anchor=NW)
            fioEntry = Entry(Frame)
            fioEntry.pack(fill="x")
            FIO_entries.append(fioEntry)

        login_lbl = Label(Frame, text="Логин").pack(anchor=NW)
        usernameInput = Entry(Frame)
        usernameInput.pack(fill="x", pady=3)
        password_lbl = Label(Frame, text="Пароль").pack(anchor=NW)
        passwordInput = Entry(Frame)
        passwordInput.pack(fill="x", pady=3)

        radio_frame = ttk.Frame(Frame)
        radio_frame.pack(side='top', pady=5)

        selected_role = StringVar()
        admin_role = ttk.Radiobutton(radio_frame, text="Администратор", value="admin", variable=selected_role)
        admin_role.pack(side=LEFT)
        user_role = ttk.Radiobutton(radio_frame, text="Пользователь", value="user", variable=selected_role)
        user_role.pack(side=LEFT)

        def register():
            FIO_info = [fioEntry.get() for fioEntry in FIO_entries]
            FIO_to_string = ' '.join(FIO_info)
            nameGet = usernameInput.get()
            passwordGet = passwordInput.get()
            role = selected_role.get()
            bytes = passwordGet.encode('utf-8') 
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)
            hash1 = hash.decode('utf-8')
            db.insertData(FIO_to_string, nameGet, hash1, role)

        def back():
            root.destroy()
            AdminPanel()
        button_frame = ttk.Frame(Frame)
        button_frame.pack(side='top')

        register_but = ttk.Button(button_frame, text = 'Зарегистрировать', command=register).pack(side=LEFT)
        backB = ttk.Button(button_frame, text = "Назад", command=back).pack(side=LEFT)

    def show_active_sessions(self):
        self.session_listbox.delete(0, END)
        self.active_sessions = db.sel_session_id2()
        for session in self.active_sessions:
            self.session_listbox.insert(END, session)

    def terminate_session(self):
        selected_index = self.session_listbox.curselection()
        if selected_index:
            selected_session = self.session_listbox.get(selected_index)
            db.upd_session((selected_session, ))
            db.closing_session()
            self.active_sessions.remove(selected_session)
    
    def back(self):
        from auth import main
        self.root.destroy()
        main()
        