from tkinter import *
from tkinter import ttk   
from database import DatabaseAuth
from tkcalendar import DateEntry
from datetime import date

db = DatabaseAuth()

class Statistics:
    def __init__(self, root):
        self.root = root
        root = Tk()
        root.title('My App')
        root.geometry('1920x1080')

        search_methods = {
            "Дате": "Date",
            "Диагнозу": "diagnosis",
            "Лекарству": "title"
        }
        Frame = ttk.Frame(borderwidth=1, relief=SOLID)
        Frame.place(relx=0.5, rely=0.3, anchor=CENTER)
        
        search_frame = ttk.Frame(Frame)
        search_frame.pack(fill='x')

        var = StringVar()
        search_label = ttk.Label(search_frame, text="Поиск по:").pack(anchor=NW, side=LEFT, padx=5)
        combobox = ttk.Combobox(search_frame, textvariable=var, values=list(search_methods.keys()), state='readonly')
        combobox.pack(fill=X, side=LEFT, expand=TRUE, padx=5)

        searchEntry = ttk.Entry(search_frame)
        searchEntry.pack(fill=X, side=LEFT, expand=TRUE)

        #Таблица    
        users_columns = ("FIO", "Date", "Doc_FIO", "Symptoms", "Drug_title", "diagnosis")
        users_descriptions = ["ФИО", "Дата", "Фамилия врача", "Симптомы", "Лекарство", "Диагноз"]
        drug_columns = ("title", "side_effects")
        drug_descriptions = ["Название", "Побочные эффекты"]

        tree = ttk.Treeview(Frame, columns=users_columns, show="headings")
        tree.pack(fill=BOTH, expand=1)
        for i, description in zip(users_columns, users_descriptions):
                tree.heading(i, text=description)

        def searchForAll():
            selected_method_display=combobox.get()
            column_name = search_methods.get(selected_method_display)
            searchAsk = str(searchEntry.get())
            allowed_columns = ["Date", "diagnosis"]

            if column_name in allowed_columns:
                db.selectAll(column_name, (searchAsk, ))
                rows = db.cur.fetchall()
                update_table(users_columns, users_descriptions, rows)
            else:
                query = "SELECT title, side_effects FROM drug_info WHERE title = %s "
                db.cur.execute(query, (searchAsk, ))
                db.connection.commit()
                rows = db.cur.fetchall()
                update_table(drug_columns, drug_descriptions, rows)

        def update_table(columns, descriptions, rows):
            for col in tree.get_children():
                tree.delete(col)

            tree["columns"] = columns
            for idx, (col, desc) in enumerate(zip(columns, descriptions)):
                tree.heading(col, text=desc)
                tree.column(col, anchor='center', width=100)
            for person in rows:
                tree.insert('', END, values=person)

        def back():
            from main import main
            root.destroy()
            main()

        button_frame = ttk.Frame(Frame)
        button_frame.pack()

        search = ttk.Button(button_frame, text= "Найти", command=searchForAll).pack(side=LEFT)
        back1 = ttk.Button(button_frame, text="Назад", command=back).pack(side=LEFT)
        root.mainloop()
        
def main():
    root = Tk()
    root.title('Doctor Screen')
    Statistics(root)
    root.mainloop()

if __name__ == "__main__":
    main()