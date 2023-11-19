from tkinter import *
from database import DatabaseAuth
db = DatabaseAuth()
import bcrypt



class AdminPanel:
    def __init__(self):
        self.root = Tk()
        self.root.title('My App')
        self.root.geometry('1920x1080')
        active_sessions = db.sel_session_id()
        self.active_sessions = active_sessions

        self.session_listbox = Listbox(self.root)
        self.refresh_button = Button(self.root, text="Refresh", command=self.show_active_sessions)
        self.terminate_button = Button(self.root, text="Terminate Session", command=self.terminate_session)
        self.register_new_user = Button(self.root, text = "Регистрация нового пользователя", command = self.register_new_users).pack()
        self.terminate_button.pack()
        self.session_listbox.pack()
        self.refresh_button.pack()

    def register_new_users(self):
        self.root.destroy()
        root = Tk()
        root.title('My App')
        root.geometry('400x400')

        def register():
            nameGet = usernameInput.get()
            passwordGet = passwordInput.get()
            role = selected_role.get()
            bytes = passwordGet.encode('utf-8') 
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)
            hash1 = hash.decode('utf-8')
            db.insertData(nameGet, hash1, role)
        def back():
            root.destroy()
            AdminPanel()
            

        signInTXT = Label(root, text='Зарегистрировать нового пользователя').pack()
        usernameInput = Entry(root)
        passwordInput = Entry(root)
        usernameInput.pack()
        passwordInput.pack()
        selected_role = StringVar()
        admin_role = Radiobutton(root, text="Админ", value="admin", variable=selected_role)
        admin_role.pack()
        user_role = Radiobutton(root, text="Юзер", value="user", variable=selected_role)
        user_role.pack()
        register_but = Button(root, text = 'Зарегистрировать', command=register).pack()
        backB = Button(root, text = "Назад", command=back).pack()

    def show_active_sessions(self):
        self.session_listbox.delete(0, END)
        self.active_sessions = db.sel_session_id2()
        for session in self.active_sessions:
            self.session_listbox.insert(END, session)

    def terminate_session(self):
        selected_index = self.session_listbox.curselection()
        if selected_index:
            selected_session = self.session_listbox.get(selected_index)
            # userID = db.user["id"]
            print(db.user)
            sel_ses = str(selected_session)
            print(selected_session)
            db.upd_session((selected_session, ))
            db.closing_session()
            print(f"Terminated session: {selected_session}")
            self.active_sessions.remove(selected_session)