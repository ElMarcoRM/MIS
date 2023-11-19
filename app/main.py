from tkinter import Tk, ttk
from doc_pages import register_examination, register_patients, statisctics
from database import DatabaseAuth
db = DatabaseAuth()

def main():
    root = Tk()
    root.title('My App')

    def open_screen(screen_class):
        root.destroy()
        screen_class(root)

    def log_out(self):
        userID = db.user["id"]
        db.upd_session(str(userID))
        db.closing_session()
        self.root.destroy()   

    doctor_button = ttk.Button(root, text='Добавить пациента', command=lambda: open_screen(register_patients.Register_patients))
    doctor_button.pack()
    register_examination_button = ttk.Button(root, text = 'Зарегистрировать осмотр', command = lambda: open_screen(register_examination.RegisterExamination))
    register_examination_button.pack()
    statistics_button = ttk.Button(root, text = 'Посмотреть статистику', command = lambda: open_screen(statisctics.Statistics))
    statistics_button.pack()
    exit = ttk.Button(root, text = 'Выйти', command = log_out).pack()

    root.mainloop()

if __name__ == "__main__":
    main()

# def check_session(self):
#     if db.sel_session_id():
#         self.root.after(1000, self.check_session)  
#     else:
#         print('root destroyed')
#         self.root.destroy()  