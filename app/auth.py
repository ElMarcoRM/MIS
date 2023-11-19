from tkinter import *
from tkinter import ttk
from database import DatabaseAuth
from main import main
from admin import AdminPanel

db = DatabaseAuth()
db.createTables()
db.createActiveSessions()

def redirect():
    nameGet = usernameInput.get()
    select = db.sel_role((nameGet, ))
    root.destroy()
    if select == 'user':
        main()
    elif select == 'admin':
        AdminPanel()

def check():
    nameGet = usernameInput.get()
    passwordGet = passwordInput.get()
    inputData = (nameGet, passwordGet,)
    if (db.checkData((nameGet, ), (inputData, ))):
        db.userad((nameGet, ))
        select = db.sel_role((nameGet, ))
        if select == 'user':
            userID = db.get_user_id((nameGet, ))
            db.ins_session(userID)
            print(userID)
        elif select == 'admin':
            print ("admin")
        redirect()
    else:   
        print("Wrong Credentials")

root = Tk()
root.title('Authorization')
root.geometry('400x400')

logFrame = ttk.Frame(borderwidth=1, relief=SOLID)
logFrame.place(relx=0.5, rely=0.3, anchor=CENTER)

signIntxt = ttk.Label(logFrame, text='Введите логин и пароль:')
signIntxt.pack()

usernameInput = Entry(logFrame)
passwordInput = Entry(logFrame)
usernameInput.pack(pady = 10, padx= 10)
passwordInput.pack(pady = 10)

signIn = Button(logFrame, text='Войти', command=check)
signIn.pack()

root.mainloop()

