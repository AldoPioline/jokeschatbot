import sqlite3
from sqlite3 import Error

import uuid

def generateDB(files):
    for file in files:
        with open(file, 'r') as f:
            questionQueue = f.read().splitlines() 
            print(questionQueue)
        try:
            sqliteConnection = sqlite3.connect('jokes.db')
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")
            userID = uuid.uuid1()
            for joke in questionQueue:
                cursor.execute("SELECT * FROM questions WHERE question = ?", [joke])
                data=cursor.fetchall()
                if not data:
                    cursor.execute("""INSERT INTO questions
                                        (question) 
                                        VALUES 
                                        (?)""",[joke])
            sqliteConnection.commit()
            print("Record inserted successfully into SqliteDb_developers table ")
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
                print("The SQLite connection is closed")

if __name__ == '__main__':
    file = 'questions.txt'
    survey = 'survey.txt'
    generateDB([survey, file])
