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
        except Exception as _ex:
            print("[INFO] Error while working with PostgreSQL", _ex)
            
    def createTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS testdata
                (login TEXT,
                password TEXT); 
                ''')
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
            print("Something went wrong")
        self.connection.commit()
    def createMainTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS patients_info
                (FIO TEXT,
                Gender TEXT,
                Date_birth DATE,
                Address TEXT); 
                ''')
        self.connection.commit()
    def insertPatientsData(self, FIO, Gender, Date, Address):
        self.cur.execute("INSERT INTO patients_info(FIO, Gender, Date_birth, Address) VALUES ('"+FIO+"', '"+Gender+"', '"+Date+"', '"+Address+"')")
        self.connection.commit()
    def createDrugTable(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS drug_info
                (title TEXT,
                active_substances TEXT,
                effect TEXT,
                method_of_taking TEXT,
                side_effects TEXT); 
                ''')
        self.connection.commit()
    def insertDrugInfo(self, title, active_substance, effect, meethod_of_taking, side_effects):
        self.cur.execute("INSERT INTO drug_info(title, active_substances, effect, method_of_taking, side_effects) VALUES ('"+title+"', '"+active_substance+"', '"+effect+"', '"+meethod_of_taking+"', '"+side_effects+"')")
        self.connection.commit()

    def createCheckTable(self): #Таблица осмотров
        self.cur.execute('''CREATE TABLE IF NOT EXISTS checking
                (FIO TEXT,
                Date DATE,
                Doc_FIO TEXT,
                Symptoms TEXT,
                Drug_title TEXT,
                diagnosis TEXT); 
                ''')
        self.connection.commit()
    def insertCheckInfo(self, FIO, Date, Doc_FIO, Symptoms, Drug_title, diagnosis):
        self.cur.execute("INSERT INTO checking(FIO, Date, Doc_FIO, Symptoms, Drug_title, diagnosis) VALUES ('"+FIO+"', '"+Date+"', '"+Doc_FIO+"', '"+Symptoms+"', '"+Drug_title+"', '"+diagnosis+"')")
        self.connection.commit()