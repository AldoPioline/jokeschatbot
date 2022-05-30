from flask import Flask, render_template, jsonify, request, session
import sqlite3
from sqlite3 import Error
import uuid

app = Flask(__name__)

app.config['SECRET_KEY'] = 'enter-a-very-secretive-key-3479373'


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html', **locals())

# @app.route('/newUser', methods=["GET", "POST"])
# def userreg():
#     if request.method == 'POST':
#         sqliteConnection = sqlite3.connect('jokes.db')
#         sqliteConnection.row_factory = lambda cursor, row: row[0]
#         cursor = sqliteConnection.cursor()
#         cursor.execute("SELECT name FROM users ")
#         data=cursor.fetchall()
#         username = request.form['name']
#         session['username'] = username

#         file = 'survey.txt'
#         if username not in data:
#             with open(file, 'r') as f:
#                 questionQueue = f.read().splitlines() 
#             for question in questionQueue:
#                 userID = str(uuid.uuid1())
#                 print('??????????? ', userID, username, question)
#                 cursor.execute("""INSERT INTO users
#                                         (id, name, question, type) 
#                                         VALUES 
#                                         (?,?,?,?)""",[userID, username, question, 'survey'])
#         file = 'questions.txt'
#         if username not in data:
#             with open(file, 'r') as f:
#                 questionQueue = f.read().splitlines() 
#             for question in questionQueue:
#                 userID = str(uuid.uuid1())
#                 print('??????????? ', userID, username, question)
#                 cursor.execute("""INSERT INTO users
#                                         (id, name, question, type) 
#                                         VALUES 
#                                         (?,?,?,?)""",[userID, username, question, 'joke'])
        
#         sqliteConnection.commit()
#         print("Record inserted successfully into users table ")
#         cursor.close()
#     return jsonify({"response": 'yes' })

def register(username):
    sqliteConnection = sqlite3.connect('jokes.db')
    sqliteConnection.row_factory = lambda cursor, row: row[0]
    cursor = sqliteConnection.cursor()
    cursor.execute("SELECT name FROM users ")
    data=cursor.fetchall()
    session['username'] = username

    file = 'survey.txt'
    if username not in data:
        with open(file, 'r') as f:
            questionQueue = f.read().splitlines() 
        for question in questionQueue:
            userID = str(uuid.uuid1())
            cursor.execute("""INSERT INTO users
                                    (id, name, question, type) 
                                    VALUES 
                                    (?,?,?,?)""",[userID, username, question, 'survey'])
    file = 'questions.txt'
    if username not in data:
        with open(file, 'r') as f:
            questionQueue = f.read().splitlines() 
        for question in questionQueue:
            userID = str(uuid.uuid1())
            cursor.execute("""INSERT INTO users
                                    (id, name, question, type) 
                                    VALUES 
                                    (?,?,?,?)""",[userID, username, question, 'joke'])
    
    sqliteConnection.commit()
    print("Record inserted successfully into users table ")
    cursor.close()

@app.route('/chatbot', methods=["GET", "POST"])
def chatbotResponse():
    if request.method == 'POST':
        userScore = request.form['question']
        userName = session.get('username')
        curJoke = session.get('joke')
        type = session.get('type')
        if not userName:
            if userScore:
                userName = userScore
                register(userName)    
            else:
                return jsonify({"response": "What's your Name?" })

        sqliteConnection = sqlite3.connect('jokes.db')
        cursor = sqliteConnection.cursor()
        if userScore and curJoke:
            if type == 'joke':
                if userScore.isdigit():
                    updateQuery = """UPDATE users  set  response =\"""" + userScore + "\"" + """ where name=\"""" + userName + "\"" + """ and question=\"""" + curJoke  +"\";"
                    cursor.execute(updateQuery)
                    sqliteConnection.commit()
            else:
                updateQuery = """UPDATE users  set response =\"""" + userScore + "\"" + """ where name=\"""" + userName + "\"" + """ and question=\"""" + curJoke  +"\";"
                print(updateQuery)
                cursor.execute(updateQuery)
                sqliteConnection.commit()
        query = """SELECT question,type FROM users where response = "" and name= \"""" + userName + "\""
        cursor.execute(query)
        data=cursor.fetchall()

        if data:
            session['joke'] = data[0][0]
            session['type'] = data[0][1]
            response = session['joke']
        else:
            response = "Thanks for taking the survey"

    return jsonify({"response": response })


if __name__ == '__main__':
    app.run( port='5000', debug=True)
