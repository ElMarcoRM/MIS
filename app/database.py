import psycopg2
import bcrypt

class DatabaseAuth():
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="qwerty",
                database="postgres"
        )
            self.cur = self.connection.cursor()
            print("Подключение создано")
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
            
    def createTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS testdata
                (login TEXT,
                password TEXT); 
                ''')
        print("Таблица создана или нет но функция сработала")
        self.connection.commit()

    def insertData(self, name, password):
        # Pass = password.encode('utf-8')
        self.cur.execute("INSERT INTO testdata(login, password) VALUES ('"+name+"', '"+password+"')")
        self.connection.commit()
    
    def checkData(self, data, inputData): #data - username, inputdata = username, password
        query = "SELECT * FROM testdata WHERE login = %s"
        self.cur.execute(query, data)
        row = self.cur.fetchall() # login - password
        try:
            if row[0][0] == inputData[0][0]: #возможно лишний кусок кода
                bytes = row[0][1].encode('utf-8') 
                bytes1 = inputData[0][1].encode('utf-8') 
                return bcrypt.checkpw(bytes1, bytes)
        except:
            print("Э БЛЯТЬ")
        self.connection.commit()