from tkinter import *
from database import DatabaseAuth
import bcrypt
from mainscreen import mainWindow

db = DatabaseAuth()
db.createTable()
db.createActiveSessions()

class AdminPanel:
    def __init__(self, Newroot):
        self.Newroot = Newroot
        active_sessions = db.sel_session_id()
        print(active_sessions)
        self.active_sessions = active_sessions

        self.session_listbox = Listbox(self.Newroot)
        self.refresh_button = Button(self.Newroot, text="Refresh", command=self.showda)
        self.terminate_button = Button(self.Newroot, text="Terminate Session", command=self.terminate_session)
        self.terminate_button.pack()
        self.session_listbox.pack()
        self.refresh_button.pack()
        self.show_active_sessions()  # Initial refresh of active sessions
    def showda(self):
       shown = self.session_listbox.get(self.session_listbox.curselection()) 
       print(shown)

    def show_active_sessions(self):
        # Clear the listbox and repopulate with active sessions
        self.session_listbox.delete(0, END)
        self.active_sessions = db.sel_session_id()

        for session in self.active_sessions:
            self.session_listbox.insert(END, session)
    def terminate_session(self):
        # Assuming you have the ability to select a session to terminate
        selected_index = self.session_listbox.curselection()
        if selected_index:
            selected_session = self.session_listbox.get(selected_index)
            # Perform termination logic here for the selected session
            userID = db.user["id"]
            db.upd_session(str(userID))
            db.closing_session()
            print(f"Terminated session: {selected_session}")
            # Remove the terminated session from the active sessions list
            self.active_sessions.remove(selected_session)
             # Update the listbox after terminating the session


def redirect():
    # root.destroy()
    mainWindow()

def check():
    nameGet = usernameInput.get()
    passwordGet = passwordInput.get()
    inputData = (nameGet, passwordGet,)
    if (db.checkData((nameGet, ), (inputData, ))):
        db.userad((nameGet, ))
        print (db.user)
        userID = db.get_user_id((nameGet, ))
        db.ins_session(userID)
        redirect()
    else:   
        print("Wrong Credentials")

def register():
    nameGet = usernameInput.get()
    passwordGet = passwordInput.get()
    bytes = passwordGet.encode('utf-8') 
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    hash1 = hash.decode('utf-8')
    db.insertData(nameGet, hash1)

def admine():
    Newroot = Tk()
    admin_panel = AdminPanel(Newroot)

root = Tk()
root.title('My App')
root.geometry('400x400')
signInTXT = Label(root, text='Войти').pack()
usernameInput = Entry(root)
passwordInput = Entry(root)


usernameInput.pack()
passwordInput.pack()
adm = Button(root, text='admin', command=admine).pack()
signUp = Button(root, text='Зарегистрироваться', command=register).pack()
signIn = Button(root, text='Войти', command=check).pack()
root.mainloop()

