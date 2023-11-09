from tkinter import *
from database import DatabaseAuth
import bcrypt
from mainscreen import mainWindow

db = DatabaseAuth()
db.createTable()

def redirect():
    root.destroy()
    mainWindow()

def check():
    nameGet = usernameInput.get() 
    passwordGet = passwordInput.get()
    inputData = (nameGet, passwordGet,)
    if (db.checkData((nameGet, ), (inputData, ))):
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
root = Tk()
root.title('My App')
root.geometry('400x400')

signInTXT = Label(root, text='Войти').pack()
usernameInput = Entry(root)
passwordInput = Entry(root)
usernameInput.pack()
passwordInput.pack()
signUp = Button(root, text='Зарегистрироваться', command=register).pack()
signIn = Button(root, text='Войти', command=check).pack()
root.mainloop()