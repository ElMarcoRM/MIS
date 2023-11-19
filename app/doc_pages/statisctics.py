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

        var = StringVar()
        search_label = ttk.Label(root, text="Поиск по").pack(anchor=NW)
        combobox = ttk.Combobox(root, textvariable=var, values=list(search_methods.keys()), state='readonly')
        combobox.pack(fill=X)

        searchEntry = ttk.Entry()
        searchEntry.pack(fill=X)

        #Таблица
        columns = ("FIO", "Date", "Doc_FIO", "Symptoms", "Drug_title", "diagnosis")
        drugDescription = ["ФИО", "Дата", "Фамилия врача", "Симптомы", "Лекарство", "Диагноз"]
        tree = ttk.Treeview(root, columns=columns, show="headings")
        tree.pack(fill=BOTH, expand=1)
        for i, description in zip(columns, drugDescription):
            tree.heading(i, text=description)
        
        def searchForAll(): #Разобраться с exception, куда вставлять табличку для лекарств, соединение таблицы лекарств и таблицы проверок
            selected_method_display=combobox.get()
            column_name = search_methods.get(selected_method_display)
            searchAsk = str(searchEntry.get())
            allowed_columns = ["Date", "diagnosis"]

            if column_name in allowed_columns:
                db.selectAll(column_name, (searchAsk, ))
                rows = db.cur.fetchall()
                for item in tree.get_children():
                    tree.delete(item)
                for person in rows:
                    tree.insert('', END, values=person)
            else:
                query = "SELECT side_effects FROM drug_info WHERE title = %s "
                db.cur.execute(query, (searchAsk, ))
                db.connection.commit()
                rows = db.cur.fetchall()
                lbl = ttk.Label(text = rows).pack()

        def back():
            from main import main
            root.destroy()
            main()

        search = ttk.Button(text= "Найти", command=searchForAll).pack()
        back1 = ttk.Button(text="Назад", command=back).pack()
        root.mainloop()
        
def main():
    root = Tk()
    root.title('Doctor Screen')
    Statistics(root)
    root.mainloop()

if __name__ == "__main__":
    main()


