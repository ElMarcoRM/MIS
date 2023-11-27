from tkinter import *
from tkinter import Tk, ttk
from doc_pages import register_examination, register_patients, statisctics
from database import DatabaseAuth

db = DatabaseAuth()

def check_session(root, check_flag):
    if check_flag and db.sel_session_id():
        root.after(5000, check_session, root, check_flag)     
    else:
        if check_flag:
            root.destroy() 

def main():
    root = Tk()
    root.title('Main page')
    root.geometry('400x400')

    def open_screen(screen_class):
        root.destroy()
        screen_class(root)

    def log_out():
        userID = db.user["id"]
        db.upd_session(str(userID))
        db.closing_session()
        root.destroy()
    
    Frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10,5])
    Frame.place(relx=0.5, rely=0.3, anchor=CENTER)

    button_frame = ttk.Frame(Frame)
    button_frame.pack(side='top', pady=5)
    
    fio_lbl = ttk.Label(button_frame, text = "Вы вошли как: " + db.user["FIO"]).pack(fill='x')
    doctor_button = ttk.Button(button_frame, text='Добавить пациента', command=lambda: open_screen(register_patients.Register_patients)).pack(fill='x')
    register_examination_button = ttk.Button(button_frame, text='Зарегистрировать осмотр', command = lambda: open_screen(register_examination.RegisterExamination)).pack(fill='x')
    statistics_button = ttk.Button(button_frame, text='Посмотреть статистику', command = lambda: open_screen(statisctics.Statistics)).pack(fill='x')
    exit = ttk.Button(button_frame, text = 'Выйти', command = log_out).pack(fill='x')

    check_session(root, True)
    root.mainloop()

if __name__ == "__main__":
    main()

