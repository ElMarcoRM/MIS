from tkinter import *
import psycopg2
from tkinter import ttk   
from tkcalendar import DateEntry

class mainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title('My App')
        self.root.geometry('1920x1080')

        lbl = ttk.Label(self.root, text='МЯУ')
        lbl.pack()

        lbl1 = ttk.Button(self.root, text='Добавить пациента', command=self.register)
        lbl1.pack()
        lbl2 = ttk.Button(self.root, text='Добавить лекарство', command=self.addNewDrug)
        lbl2.pack()
        lbl3 = ttk.Button(self.root, text='Зарегистрировать осмотр', command=self.register_osmotr)
        lbl3.pack()
        lbl4= ttk.Button(self.root, text='Просмотреть список пациентов', command=self.viewAllPatients)
        lbl4.pack()

        self.root.mainloop()
        
    def register(self):
        self.root.destroy()
        register_window = Tk()
        register_window.title('My App')
        register_window.geometry('400x400')

        lbl = ttk.Label(register_window, text='Регистрация нового пациента')
        lbl.pack()
        frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[8, 10])
        FIO = ["Фамилия", "Имя", "Отчество"]
        for i in FIO:
            address_entry = ttk.Entry(frame)
            address_label = ttk.Label(frame, text=i)
            address_label.pack(anchor=NW)
            address_entry.pack(fill=X)
        frame.pack(anchor=NW, fill=X, padx=5, pady=5)

        selected_gender = StringVar()
        gender_male = ttk.Radiobutton(text="Мужской", value=1, variable=selected_gender)
        gender_male.pack()
        gender_female = ttk.Radiobutton(text="Женский", value=2, variable=selected_gender)
        gender_female.pack()
        
        lbl313 = ttk.Label(register_window, text='Введите дату рождения').pack()
        dentry = DateEntry(register_window)
        dentry.pack()
        
        frame2 = ttk.Frame(borderwidth=1, relief=SOLID,padding=[8, 10])
        address = ["Город", "Улица", "Дом", "Квартира"]
        for i in address:
            address_entry = ttk.Entry(frame2)
            address_label = ttk.Label(frame2, text=i)
            address_label.pack(anchor=NW)
            address_entry.pack(fill=X)
        frame2.pack(anchor=NW, fill=X, padx=5, pady=5)

        add = ttk.Button(text = "Добавить пациента")
        add.pack()

        register_window.mainloop()
    
    def addNewDrug(self):
        self.root.destroy()
        addingDrugs = Tk()
        addingDrugs.title('My App')
        addingDrugs.geometry('400x400')
        
        drugDescription = ["Название", "Активные вещества", "Действие", "Способ приема", "Побочные эффекты"]
        for i in drugDescription:
            entry = ttk.Entry()
            label = ttk.Label(text=i)
            label.pack()
            entry.pack()
        addingDrugs.mainloop()

    def register_osmotr(self):
        self.root.destroy()
        regCheck = Tk()
        regCheck.title('My App')
        regCheck.geometry('400x400')
        # выбор пациента, которого внесли в бд до этого
        patientsNames = ('Ex1', 'Ex2', 'Александр Леонидович Терентьев')
        var = StringVar()
        combobox=ttk.Combobox(regCheck, textvariable=var)
        combobox['values'] = patientsNames
        combobox['state'] = 'readonly'
        combobox.pack()
        # ФИО Врача, который проводит осмотр
        # Дата и время
        # Симптомы - entry
        # Диагноз - entry
        # Лекарство - combobox
        drugs = ('Ex1', 'Ex2', 'Фенибут')
        var1 = StringVar()
        combobox1=ttk.Combobox(regCheck, textvariable=var1)
        combobox1['values'] = drugs
        combobox1['state'] = 'readonly'
        combobox1.pack()
        regCheck.mainloop()

    def viewAllPatients(self):
        self.root.destroy()
        selectPatients = Tk()
        selectPatients.title('My App')
        selectPatients.geometry('400x400')

        connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="qwerty",
            database="postgres"
        )
        cur = connection.cursor()
        cur.execute('''SELECT * FROM testdata 
                ''')
        connection.commit()
        viewTable = cur.fetchall()
        label = ttk.Label(text = viewTable)
        label.pack()
        print(viewTable)
        # Таблица со всеми пациентами
        columns = ("login", "password")
        tree = ttk.Treeview(columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)
        tree.heading("login", text = "Логин")
        tree.heading("password", text = "Пароль")
        for person in viewTable:
            tree.insert('', END, values=person)

        # Поиск нужного пациента
        selectPatients.mainloop


