from tkinter import *
from tkinter import ttk   
from database import DatabaseAuth
from tkcalendar import DateEntry
from datetime import date


db = DatabaseAuth()
class RegisterExamination:
    def __init__(self, root):
        self.root = root
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')

        db.createTables()
        # self.check_session()

        # выбор пациента, которого внесли в бд до этого
        rows = db.selectPatients()
        table = [' '.join(inner) for inner in rows]
        choosePatient = ttk.Label(text = "Выберите пациента").pack(anchor=NW)
        var = StringVar()
        combobox=ttk.Combobox(root, textvariable=var)
        combobox['values'] = table
        combobox['state'] = 'readonly'
        combobox.pack(fill=X)

        # ФИО Врача, который проводит осмотр - автоматически
        doc_name = db.user["login"]
        doc_FIO = ttk.Label(root, text = doc_name).pack()
        # Место текущего осмотра - entry
        # Дата и время - автоматически
        today = date.today()
        dateLabel = ttk.Label(text=today)
        dateLabel.pack()
        # Симптомы - entry
        Symptoms = ttk.Label(text="Симптомы").pack(anchor=NW)
        symptomEntry = ttk.Entry()
        symptomEntry.pack(fill=X)
        # Диагноз - entry
        Diagnosis = ttk.Label(text="Диагноз").pack(anchor=NW)
        diagnosEntry = ttk.Entry()
        diagnosEntry.pack(fill=X)

        # Лекарство - выбор лекарства из бд или добавление нового - чекнуть мб добавить в функцию
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

        def back():
            from main import main
            root.destroy()
            main()

        def insertCheck():
            FIO = combobox.get()
            Date = date.today()
            date_stringing = str(Date)
            Doc_FIO = db.user["login"]
            symptoms = symptomEntry.get()
            drug_title = combobox1.get()
            diagnosis = diagnosEntry.get()
            print(FIO, date_stringing, Doc_FIO, symptoms, drug_title, diagnosis)
            db.insertCheckInfo(FIO, date_stringing, Doc_FIO, symptoms, drug_title, diagnosis)

        add_button = ttk.Button(text = "Добавить", command=insertCheck).pack()
        addDrug = ttk.Button(text= "Добавить новое лекарство", command=self.addNewDrug).pack()
        backButton = ttk.Button(text = "Назад", command=back).pack()

        root.mainloop()

    def addNewDrug(self):
        addingDrugWin = Tk()
        addingDrugWin.title('My App')
        addingDrugWin.geometry('1920x1080')
        # self.check_session()

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
        
def main():
    root = Tk()
    root.title('Doctor Screen')
    RegisterExamination(root)
    root.mainloop()

if __name__ == "__main__":
    main()