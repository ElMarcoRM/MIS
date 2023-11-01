from tkinter import *
from database import DatabaseAuth
import bcrypt
from mainscreen import mainWindow

db = DatabaseAuth()
db.createTable()

# tamara - lisafe
#max - korolev

def redirect():
    root.destroy
    mainWindow()

def check():
    nameGet = usernameInput.get()  # Retrieve the name when the button is clicked
    passwordGet = passwordInput.get()
    inputData = (nameGet, passwordGet,)
    if (db.checkData((nameGet, ), (inputData, ))):
        redirect()
    else:   
        print("Wrong Credentials")

def clicked():
    nameGet = usernameInput.get()  # Retrieve the name when the button is clicked
    passwordGet = passwordInput.get()
    bytes = passwordGet.encode('utf-8') 
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    hash1 = hash.decode('utf-8')
    db.insertData(nameGet, hash1)
    print('Данные внесены')

root = Tk()
root.title('My App')
root.geometry('400x400')

lbl1 = Label(root, text='Войти').pack()
usernameInput = Entry(root)
passwordInput = Entry(root)
usernameInput.pack()
passwordInput.pack()
signIn = Button(root, text='Зарегистрироваться', command=clicked).pack()
signUp = Button(root, text='Войти', command=check).pack()
root.mainloop()

# passwords = 'some'
# bytes = passwords.encode('utf-8') 
# salt = bcrypt.gensalt()
# hash = bcrypt.hashpw(bytes, salt)
# hash1 = hash.decode('utf-8')

# a = 'some'
# a1 = a.encode('utf-8')
# if bcrypt.checkpw(a1, hash):
#     print('да')
# else:
#     print('пошелнахуй')