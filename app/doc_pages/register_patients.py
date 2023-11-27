from tkinter import *
from tkinter import ttk   
from database import DatabaseAuth
from tkcalendar import DateEntry

db = DatabaseAuth()
class Register_patients:
    def __init__(self, root):
        self.root = root
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')

        Frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10,10])
        Frame.place(relx=0.5, rely=0.3, anchor=CENTER)
    
        register_new_patients = ttk.Label(Frame, text='Регистрация нового пациента').pack()
        entry_frame = ttk.Frame(Frame)
        entry_frame.pack()
        fio_frame = ttk.Frame(entry_frame)
        fio_frame.pack(side=LEFT, padx=5)

        FIO = ["Фамилия", "Имя", "Отчество"]
        FIO_entries = []
        for i in FIO:
            FIO_label = ttk.Label(fio_frame, text=i).pack()
            fioEntry = ttk.Entry(fio_frame)
            fioEntry.pack(fill='x')
            FIO_entries.append(fioEntry)
        
        address = ["Город", "Улица", "Дом", "Корпус", "Квартира"]
        address_entries = []
        
        address_frame = ttk.Frame(entry_frame)
        address_frame.pack(side=RIGHT, padx=5)
        for i in address:
            address_label = ttk.Label(address_frame, text=i).pack()
            addressEntry = ttk.Entry(address_frame)
            addressEntry.pack(fill='x')
            address_entries.append(addressEntry)

        radio_frame = ttk.Frame(Frame)
        radio_frame.pack(pady=5)

        selected_gender = StringVar()
        gender_male = ttk.Radiobutton(radio_frame, text="Мужской", value="male", variable=selected_gender)
        gender_male.pack(side=LEFT)
        gender_female = ttk.Radiobutton(radio_frame, text="Женский", value="female", variable=selected_gender)
        gender_female.pack(side=LEFT)
        
        date_frame = ttk.Frame(Frame)
        date_frame.pack(pady=5)

        birth_date = ttk.Label(date_frame, text="Введите дату рождения:").pack(side=LEFT, padx=5)
        dentry = DateEntry(date_frame, date_pattern='dd/mm/yy')
        dentry.pack(side=LEFT)
        
        def add_patients():
            date =  dentry.get_date()
            date_stringing = str(date)
            FIO_info = [fioEntry.get() for fioEntry in FIO_entries]
            FIO_to_string = ', '.join(FIO_info)
            Address_info = [addressEntry.get() for addressEntry in address_entries]
            Address_to_string = ', '.join(Address_info)
            Gender_info = selected_gender.get()
            db.insertPatientsData(FIO_to_string, Gender_info, date_stringing, Address_to_string)

        def back():
            from main import main
            root.destroy()
            main()

        button_frame = ttk.Frame(Frame)
        button_frame.pack(pady=5)

        addPatient = ttk.Button(button_frame, text = "Добавить пациента", command=add_patients).pack(side=LEFT, padx=5)
        backButton = ttk.Button(button_frame, text = "Назад", command=back).pack(side=LEFT)
        root.mainloop()

def main():
    root = Tk()
    root.title('Doctor Screen')
    Register_patients(root)
    root.mainloop()

if __name__ == "__main__":
    main()