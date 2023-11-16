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
        self.cur.execute('''CREATE TABLE IF NOT EXISTS log
                (id SERIAL PRIMARY KEY,
                login TEXT,
                password TEXT); 
                ''')
        self.connection.commit()
    
    user = {
        "id": "",
        "login": "",
        "password":""
    }

    def userad(self, data):
        query = "SELECT * FROM log WHERE login =%s"
        self.cur.execute(query, data)
        row = self.cur.fetchall()
        # print(row)
        self.user["id"] = row[0][0] # Assuming the ID is the first column in the result
        self.user["login"] = row[0][1] # Assuming login is the second column
        self.user["password"] = row[0][2]
        return self.user

    def insertData(self, name, password):
        # Pass = password.encode('utf-8')
        self.cur.execute("INSERT INTO log(login, password) VALUES ('"+name+"', '"+password+"')")
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
    
    #Select - выбор пациента, которого внесли до этого
    def selectPatients(self):
        self.cur = self.connection.cursor()
        self.cur.execute("SELECT FIO FROM patients_info")
        self.connection.commit()
    def selectAll(self, column_name, searchAsk):
        self.cur = self.connection.cursor()
        query = f"SELECT * FROM checking WHERE {column_name} = %s "
        self.cur.execute(query, searchAsk)
        self.connection.commit()

    #____________


    def get_user_id(self, data):
        self.cur = self.connection.cursor()
        query = "SELECT id FROM log WHERE login = %s "
        self.cur.execute(query, data)
        self.connection.commit()
        user_id = self.cur.fetchone()
        if user_id:
            return user_id[0]  # Return the user ID if found
        else:
            return None  # Return None if user ID is not found
        
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

    def closing_session(self):
        query = 'DELETE FROM active_sessions WHERE NOT active = TRUE'
        self.cur.execute(query)
        self.connection.commit()

