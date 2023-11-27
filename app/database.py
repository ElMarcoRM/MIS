import psycopg2
import bcrypt
from psycopg2 import IntegrityError

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
            
    def createTables(self):
        self.cur.execute('''
                CREATE TABLE IF NOT EXISTS log (
                    id SERIAL PRIMARY KEY,
                    FIO TEXT,
                    login TEXT UNIQUE,
                    password TEXT UNIQUE,
                    role TEXT DEFAULT 'user'
                ); 
                
                CREATE TABLE IF NOT EXISTS patients_info ( 
                    FIO TEXT,
                    Gender TEXT,
                    Date_birth DATE,
                    Address TEXT
                );
                
                CREATE TABLE IF NOT EXISTS drug_info (
                    title TEXT,
                    active_substances TEXT,
                    effect TEXT,
                    method_of_taking TEXT,
                    side_effects TEXT
                );

                CREATE TABLE IF NOT EXISTS checking (
                    FIO TEXT,
                    Date DATE,
                    Address TEXT,
                    Doc_FIO TEXT,
                    Symptoms TEXT,
                    Drug_title TEXT,
                    diagnosis TEXT
                );
            ''')
        self.connection.commit()
        try:
            self.default_users()
        except IntegrityError as e:
            print(f"Insertion failed: {e}")
        self.connection.commit()

    user = {
        "id": "",
        "FIO": "",
        "login": "",
        "password":"",
        "role":""
    }

    def default_users(self):
        password_word = 'lisafe'
        bytes = password_word.encode('utf-8') 
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        hash1 = hash.decode('utf-8')
        query = "INSERT INTO log(FIO, login, password, role) VALUES ('Lisafeva Tamara Andreevna', 'tamara', '"+hash1+"', 'admin')"
        self.cur.execute(query)
        self.connection.commit()

    def userad(self, data):
        query = "SELECT * FROM log WHERE login =%s"
        self.cur.execute(query, data)
        row = self.cur.fetchall()
        if row[0][4] == 'user':
            self.user["id"] = row[0][0]
            self.user["FIO"] = row[0][1]
            self.user["login"] = row[0][2]
            self.user["password"] = row[0][3]
            self.user["role"] = row[0][4]
        else:
            print('admin')
        return self.user

    def insertData(self,FIO, name, password, role):
        self.cur.execute("INSERT INTO log(FIO, login, password, role) VALUES ('"+FIO+"', '"+name+"', '"+password+"', '"+role+"')")
        self.connection.commit()
    
    def checkData(self, data, inputData): #data - username, inputdata = username, password
        query = "SELECT login, password FROM log WHERE login = %s"
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

    def insertPatientsData(self, FIO, Gender, Date, Address):
        self.cur.execute("INSERT INTO patients_info(FIO, Gender, Date_birth, Address) VALUES ('"+FIO+"', '"+Gender+"', '"+Date+"', '"+Address+"')")
        self.connection.commit()
    
    def insertDrugInfo(self, title, active_substance, effect, meethod_of_taking, side_effects):
        self.cur.execute("INSERT INTO drug_info(title, active_substances, effect, method_of_taking, side_effects) VALUES ('"+title+"', '"+active_substance+"', '"+effect+"', '"+meethod_of_taking+"', '"+side_effects+"')")
        self.connection.commit()

    def insertCheckInfo(self, FIO, Date, Address, Doc_FIO, Symptoms, Drug_title, diagnosis):
        self.cur.execute("INSERT INTO checking(FIO, Date, Address, Doc_FIO, Symptoms, Drug_title, diagnosis) VALUES ('"+FIO+"', '"+Date+"', '"+Address+"', '"+Doc_FIO+"', '"+Symptoms+"', '"+Drug_title+"', '"+diagnosis+"')")
        self.connection.commit()
    
    #Select - выбор пациента, которого внесли до этого
    def selectPatients(self):
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT FIO FROM patients_info")
        self.connection.commit()
        rows = self.cur.fetchall()
        return rows
    def selectAll(self, column_name, searchAsk):
        self.cur = self.connection.cursor()
        query = f"SELECT * FROM checking WHERE {column_name} = %s "
        self.cur.execute(query, searchAsk)
        self.connection.commit()

    def get_user_id(self, data):
        self.cur = self.connection.cursor()
        query = "SELECT id FROM log WHERE login = %s "
        self.cur.execute(query, data)
        self.connection.commit()
        user_id = self.cur.fetchone()
        if user_id:
            return user_id[0]
        else:
            return None
        
    def createActiveSessions(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS active_sessions
                (session_id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES log(id),
                active BOOLEAN); 
                ''')
        self.connection.commit()

    def upd_session(self, data):
        query = "UPDATE active_sessions SET active = CASE WHEN active = true THEN false ELSE true END WHERE user_id = %s"
        self.cur.execute(query, data)
        self.connection.commit()

    def ins_session(self, userID):
        userID = str(userID)
        self.cur.execute("INSERT INTO active_sessions(user_id, active) VALUES ('"+userID+"', true)")
        self.connection.commit()

    def sel_session_id(self):
        query = "SELECT * FROM active_sessions"
        self.cur.execute(query)
        row = self.cur.fetchall()
        if row:
            return row
    def sel_session_id2(self):
        query = "SELECT user_id FROM active_sessions"
        self.cur.execute(query)
        row = self.cur.fetchall()
        if row:
            return row
    def select_drug_title(self):
        self.cur.execute("SELECT title FROM drug_info ")
        self.connection.commit()
        row = self.cur.fetchall()
        return row

    def closing_session(self):
        query = 'DELETE FROM active_sessions WHERE NOT active = TRUE'
        self.cur.execute(query)
        self.connection.commit()

    def sel_role(self, login):
        query = "SELECT role FROM log WHERE login = %s"
        self.cur.execute(query, login)
        row = self.cur.fetchone()
        return row[0]
