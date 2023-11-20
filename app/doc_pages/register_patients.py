from tkinter import *
from tkinter import ttk   
from database import DatabaseAuth
from tkcalendar import DateEntry
from datetime import date


db = DatabaseAuth()
class Register_patients:
    def __init__(self, root):
        self.root = root
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')

        register_new_patients = ttk.Label(root, text='Регистрация нового пациента').pack()
        fioFrame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10]).pack(anchor=NW, fill=X, padx=5, pady=5)
        FIO = ["Фамилия", "Имя", "Отчество"]
        FIO_entries = []

        for i in FIO:
            FIO_label = ttk.Label(fioFrame, text=i).pack(anchor=NW)
            fioEntry = ttk.Entry(fioFrame)
            fioEntry.pack(fill=X)
            FIO_entries.append(fioEntry)

        selected_gender = StringVar()
        gender_male = ttk.Radiobutton(text="Мужской", value="male", variable=selected_gender)
        gender_male.pack()
        gender_female = ttk.Radiobutton(text="Женский", value="female", variable=selected_gender)
        gender_female.pack()
        
        birth_date = ttk.Label(root, text="Введите дату рождения").pack()
        dentry = DateEntry(root)
        dentry.pack()
        
        addressFrame = ttk.Frame(borderwidth=1, relief=SOLID,padding=[8, 10]).pack(anchor=NW, fill=X, padx=5, pady=5)
        address = ["Город", "Улица", "Дом", "Корпус", "Квартира"]
        address_entries = []
        
        for i in address:
            address_label = ttk.Label(addressFrame, text=i).pack(anchor=NW)
            addressEntry = ttk.Entry(addressFrame)
            addressEntry.pack(fill=X)
            address_entries.append(addressEntry)

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

        addPatient = ttk.Button(text = "Добавить пациента", command=add_patients).pack()
        backButton = ttk.Button(text = "Назад", command=back).pack()
        root.mainloop()

def main():
    root = Tk()
    root.title('Doctor Screen')
    Register_patients(root)
    root.mainloop()

if __name__ == "__main__":
    main()


