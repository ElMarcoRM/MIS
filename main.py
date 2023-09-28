from tkinter import *
import psycopg2

try:
    connection = psycopg2.connect(
        host="localhost",
        user="postgres",
        password="qwerty",
        database="db_name"
    )
    cur = connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS testdata
              (login TEXT,
              password TEXT); 
              ''')
    connection.commit()
    print("Таблицы создана")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)


root = Tk()
root.title('My App')
root.geometry('400x400')
login = Entry(root)
login.place(x=10, y=90) 
passwd = Entry(root)
passwd.place(x=10, y=150)
def clicked():
    name=login.get()
    password=passwd.get()
    print(name, password)
    cur.execute("INSERT INTO testdata(login, password) VALUES ('"+name+"', '"+password+"')")
    connection.commit()
    print('Данные внесены')
lbl1 = Label(root, text='Войти').place(x=10, y=10)
btn1 = Button(root, text='Войти', command=clicked).place(x=10, y=200)

root.mainloop()