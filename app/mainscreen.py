from tkinter import *
import psycopg2
from tkinter import ttk   
from database import DatabaseAuth
from tkcalendar import DateEntry
from datetime import date

db = DatabaseAuth()
class mainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title('My App')
        self.root.geometry('1920x1080')

        choose = ttk.Label(self.root, text='Выберите действие:').pack()
        add_patients = ttk.Button(self.root, text='Добавить пациента', command=self.register).pack()
        register_checking = ttk.Button(self.root, text='Зарегистрировать осмотр', command=self.register_osmotr).pack()
        statistics = ttk.Button(self.root, text='Статистика', command=self.viewAllPatients).pack()
        self.root.mainloop()
    
    def register(self):
        self.root.destroy()
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')
        db.createMainTable()

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
            root.destroy()
            mainWindow()
        addPatient = ttk.Button(text = "Добавить пациента", command=add_patients).pack()
        backButton = ttk.Button(text = "Назад", command=back).pack()
        root.mainloop()

    def register_osmotr(self):
        self.root.destroy()
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')
        db.createCheckTable()

        # выбор пациента, которого внесли в бд до этого
        db.cur = db.connection.cursor()
        db.cur.execute("SELECT FIO FROM patients_info")
        db.connection.commit()
        rows = db.cur.fetchall()
        table = [' '.join(inner) for inner in rows]
        # for row in rows:
        #     fio = str(row[0])
        #     fio = fio.replace("{", "").replace("}", "") 
        var = StringVar()
        choosePatient = ttk.Label(text = "Выберите пациента")
        combobox=ttk.Combobox(root, textvariable=var)
        combobox['values'] = table
        combobox['state'] = 'readonly'
        combobox.pack(fill=X)
        print(table)

        # ФИО Врача, который проводит осмотр - автоматически
        # Место текущего осмотра - entry
        # Дата и время - автоматически
        today = date.today()
        dateLabel = ttk.Label(text=today)
        dateLabel.pack()
        # Симптомы - entry
        Symptoms = ttk.Label(text="Симптомы").pack(anchor=NW)
        entry1 = ttk.Entry()
        entry1.pack(fill=X)
        # Диагноз - entry
        Diagnosis = ttk.Label(text="Диагноз").pack(anchor=NW)
        entry2 = ttk.Entry()
        entry2.pack(fill=X)
        # Лекарство - выбор лекарства из бд или добавление нового
        db.cur.execute("SELECT title FROM drug_info ")
        db.connection.commit()
        rows1 = db.cur.fetchall()
        table1 = [' '.join(inner) for inner in rows1]
        var1 = StringVar()
        drugCheck = ttk.Label(text = "Лекарство").pack(anchor=NW)
        combobox1=ttk.Combobox(root, textvariable=var1)
        combobox1['values'] = table1
        combobox1['state'] = 'readonly'
        combobox1.pack(fill=X)
        addDrug = ttk.Button(text= "Добавить новое лекарство", command=self.addNewDrug)
        addDrug.pack()
        def back(): 
            root.destroy()
            mainWindow()   
        def insertCheck():
            FIO = combobox.get()
            Date = date.today()
            date_stringing = str(Date)
            Doc_FIO = "Доктор"
            symptoms = entry1.get()
            drug_title = combobox1.get()
            diagnosis = entry2.get()
            print(FIO, date_stringing, Doc_FIO, symptoms, drug_title, diagnosis)
            db.insertCheckInfo(FIO, date_stringing, Doc_FIO, symptoms, drug_title, diagnosis)
        add_button = ttk.Button(text = "Добавить", command=insertCheck).pack()
        backButton = ttk.Button(text = "Назад", command=back).pack()
        root.mainloop()

    def addNewDrug(self):
        addingDrugWin = Tk()
        addingDrugWin.title('My App')
        addingDrugWin.geometry('1920x1080')
        db.createDrugTable()
        drugDescription = ["Название", "Активные вещества", "Действие", "Способ приема", "Побочные эффекты"]
        drugEntries = []
        for i in drugDescription:
            label = ttk.Label(addingDrugWin, text=i).pack()
            entry = ttk.Entry(addingDrugWin)
            entry.pack()
            drugEntries.append(entry)
        def add_drug():
            drug_info = [entry.get() for entry in drugEntries]
            db.insertDrugInfo(*drug_info)  
        addDrug = ttk.Button(addingDrugWin, text = "Добавить", command=add_drug)
        addDrug.pack()
        backToRegister = ttk.Button(addingDrugWin, text="Назад", command=addingDrugWin.destroy).pack()
        addingDrugWin.mainloop()

    def viewAllPatients(self):
        self.root.destroy()
        selectPatients = Tk()
        selectPatients.title('My App')
        selectPatients.geometry('400x400')
        dentry = DateEntry()
        dentry.pack()
        diagnosisEntry = ttk.Entry(selectPatients)
        diagnosisEntry.pack(fill=X)
        drugEntry = ttk.Entry(selectPatients)
        drugEntry.pack(fill=X)
        columns = ("FIO", "Date", "Doc_FIO", "Symptoms", "Drug_title", "diagnosis")
        tree = ttk.Treeview(columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)
        tree.heading("FIO", text = "ФИО")
        tree.heading("Date", text = "Дата")
        tree.heading("Doc_FIO", text = "Фамилия доктора")
        tree.heading("Symptoms", text = "Симптомы")
        tree.heading("Drug_title", text = "Лекарство")
        tree.heading("diagnosis", text = "Диагноз")
        def checkDate():
            query = "SELECT * FROM checking WHERE Date = %s "
            date =  dentry.get_date()
            date_stringing = str(date)
            db.cur = db.connection.cursor()
            db.cur.execute(query, (date_stringing, ))
            db.connection.commit()
            rows = db.cur.fetchall()
            for item in tree.get_children():
                tree.delete(item)
            for person in rows:
                tree.insert('', END, values=person)
        def checkDiagnosis():
            query = "SELECT * FROM checking WHERE diagnosis = %s "
            diagnosisGet = diagnosisEntry.get()
            db.cur = db.connection.cursor()
            db.cur.execute(query, (diagnosisGet, ))
            db.connection.commit()
            rows = db.cur.fetchall()
            for item in tree.get_children():
                tree.delete(item)
            for person in rows:
                tree.insert('', END, values=person)
        def drugEffect():
            query = "SELECT side_effects FROM drug_info WHERE title = %s "
            drugEntryGet = drugEntry.get()
            db.cur = db.connection.cursor()
            db.cur.execute(query, (drugEntryGet, ))
            db.connection.commit()
            rows = db.cur.fetchall()
            tree.destroy()
            lbl = ttk.Label(text = rows).pack()
        def back():
            selectPatients.destroy()
            mainWindow()
        dateSearch = ttk.Button(text= "Найти по дате", command=checkDate).pack()
        diagnosisSearch = ttk.Button(text= "Найти по диагнозу", command=checkDiagnosis).pack()
        drugEffectSearch = ttk.Button(text= "Найти побочный эффект по лекарству", command=drugEffect).pack()
        
        back1 = ttk.Button(text="Назад", command=back).pack()
        selectPatients.mainloop