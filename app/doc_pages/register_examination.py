from tkinter import *
from tkinter import ttk   
from database import DatabaseAuth
from datetime import date

db = DatabaseAuth()

class RegisterExamination:
    def __init__(self, root):
        self.root = root
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')

        Frame = ttk.Frame(borderwidth=1, relief=SOLID, padding=[10,10])
        Frame.place(relx=0.5, rely=0.3, anchor=CENTER)

        today = date.today().strftime('%d/%m/%y')
        dateLabel = ttk.Label(Frame, text="Дата: " + str(today))
        dateLabel.pack()

        patients_results = db.selectPatients()
        table_patients = [' '.join(inner) for inner in patients_results]
        choose_patient = ttk.Label(Frame, text = "Выберите пациента:").pack(anchor=NW)
        var = StringVar()
        choose_patient_combobox=ttk.Combobox(Frame, textvariable=var)
        choose_patient_combobox['values'] = table_patients
        choose_patient_combobox['state'] = 'readonly'
        choose_patient_combobox.pack(fill=X)

        place_lbl=ttk.Label(Frame, text="Введите место осмотра: Город, улица, дом, корпус, квартира").pack()
        place_input=ttk.Entry(Frame)
        place_input.pack(fill=X)

        symptoms = ttk.Label(Frame, text="Укажите симптомы").pack(anchor=NW)
        symptomEntry = ttk.Entry(Frame)
        symptomEntry.pack(fill=X)

        diagnosis = ttk.Label(Frame,text="Укажите диагноз").pack(anchor=NW)
        diagnosEntry = ttk.Entry(Frame)
        diagnosEntry.pack(fill=X)
        
        drug_frame = ttk.Frame(Frame)
        drug_frame.pack(fill=X)

        drug_results = db.select_drug_title()
        table_drug = [' '.join(inner) for inner in drug_results]
        var1 = StringVar()
        drug_check = ttk.Label(drug_frame, text = "Лекарство").pack(anchor=NW)
        choose_drug=ttk.Combobox(drug_frame, textvariable=var1)
        choose_drug['values'] = table_drug
        choose_drug['state'] = 'readonly'
        choose_drug.pack(fill='x', side=LEFT, expand=TRUE)
        addDrug = ttk.Button(drug_frame, text= "Добавить новое лекарство", command=self.addNewDrug).pack(side=LEFT)

        def back():
            from main import main
            root.destroy()
            main()

        def insertCheck():
            FIO = choose_patient_combobox.get()
            Date = date.today()
            date_stringing = str(Date)
            address = place_input.get()
            doc_FIO = db.user["FIO"]
            symptoms = symptomEntry.get()
            drug_title = choose_drug.get()
            diagnosis = diagnosEntry.get()
            db.insertCheckInfo(FIO, date_stringing, address, doc_FIO, symptoms, drug_title, diagnosis)

        button_frame = ttk.Frame(Frame)
        button_frame.pack()

        add_button = ttk.Button(button_frame, text = "Добавить", command=insertCheck).pack(side=LEFT)
        backButton = ttk.Button(button_frame, text = "Назад", command=back).pack(side=LEFT)

        root.mainloop()

    def addNewDrug(self):
        addingDrugWin = Tk()
        addingDrugWin.title('My App')
        addingDrugWin.geometry('1920x1080')

        drugDescription = ["Название", "Активные вещества", "Действие", "Способ приема", "Побочные эффекты"]
        drugEntries = []

        Frame = ttk.Frame(addingDrugWin, borderwidth=1, relief=SOLID, padding=[10,10])
        Frame.place(relx=0.5, rely=0.3, anchor=CENTER)

        for i in drugDescription:
            label = ttk.Label(Frame, text=i).pack()
            entry = ttk.Entry(Frame)
            entry.pack()
            drugEntries.append(entry)

        def add_drug():
            drug_info = [entry.get() for entry in drugEntries]
            db.insertDrugInfo(*drug_info)  
        button_frame = ttk.Frame(Frame)
        button_frame.pack(pady=5)

        addDrug = ttk.Button(button_frame, text = "Добавить", command=add_drug).pack(side=LEFT)
        backToRegister = ttk.Button(button_frame, text="Назад", command=addingDrugWin.destroy).pack(side=LEFT)
        addingDrugWin.mainloop()
        
def main():
    root = Tk()
    root.title('Doctor Screen')
    RegisterExamination(root)
    root.mainloop()

if __name__ == "__main__":
    main()