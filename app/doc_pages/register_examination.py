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

        def check(root):
            from main import check_session
            check_session(root)
        root.after(5000, check, root)

        # выбор пациента, которого внесли в бд до этого
        patients_results = db.selectPatients()
        table_patients = [' '.join(inner) for inner in patients_results]
        choose_patient = ttk.Label(text = "Выберите пациента:").pack(anchor=NW)
        var = StringVar()
        choose_patient_combobox=ttk.Combobox(root, textvariable=var)
        choose_patient_combobox['values'] = table_patients
        choose_patient_combobox['state'] = 'readonly'
        choose_patient_combobox.pack(fill=X)

        # ФИО Врача, который проводит осмотр - автоматически
        doc_name = db.user["FIO"]
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
        drug_results = db.select_drug_title()
        table_drug = [' '.join(inner) for inner in drug_results]
        var1 = StringVar()
        drug_check = ttk.Label(text = "Лекарство").pack(anchor=NW)
        choose_drug=ttk.Combobox(root, textvariable=var1)
        choose_drug['values'] = table_drug
        choose_drug['state'] = 'readonly'
        choose_drug.pack(fill='x')

        def back():
            from main import main
            root.destroy()
            main()

        def insertCheck():
            FIO = choose_patient_combobox.get()
            Date = date.today()
            date_stringing = str(Date)
            Doc_FIO = db.user["FIO"]
            symptoms = symptomEntry.get()
            drug_title = choose_drug.get()
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