from control import Control

from flask import Flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS

from sqlalchemy.ext.declarative import declarative_base
app = Flask(__name__)
CORS(app)

POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}
import psycopg2

con = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5432")

print("Database opened successfully")

cur = con.cursor()
try:
    cur.execute("SELECT ID,X,Y,MVE from MOUSE")
    rows = cur.fetchall()
except:
    con.commit()
    cur = con.cursor()
    cur.execute('''CREATE TABLE MOUSE
          (ID INT PRIMARY KEY     NOT NULL,
          X           INT    NOT NULL,
          Y            INT     NOT NULL,
          MVE          CHAR(1)     );''')


    print("Table created successfully")
    con.commit()
con.close()

#
# DATABASE_URI = 'postgres+psycopg2://postgres:password@localhost:5432/postgres'
# engine = create_engine(DATABASE_URI)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
# Base.metadata.create_all(engine)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)
#db.init_app(app)

from models import Mouse

@app.route('/')
def hello():
    c = Control()

    c.moveMouse(100, 500)
    c.clickMouse(100, 500)
    c.moveMouse(900, 900)
    c.moveMouse(1920, 1080)
    #
    # try:
    #     books = Mouse.query.all()
    #     return jsonify([e.serialize() for e in books])
    # except Exception as e:
    #     return (str(e))
    #
    # print(Mouse.query.all())
    # s = Session()
    # print(s.query(Mouse).first())
    # s.close()
    con = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5432")
    cur = con.cursor()
    #
    cur.execute(
        "INSERT INTO MOUSE (ID,X,Y,MVE) VALUES (1,0,0,'0')");
    con.commit()
    print("Record inserted successfully")

    cur = con.cursor()
    cur.execute("SELECT ID,X,Y from MOUSE")
    rows = cur.fetchall()

    for row in rows:
        print("id =", row[0])
        print("x =", row[1])
        print("y =", row[2], "\n")

    print("Operation done successfully")
    con.close()
    return "Hello World!"

@app.route('/move', methods=['POST'])
def move():
    print(request.json)
    data = request.get_json();
    x = int(data['x'])
    y = int(data['y'])

    con = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5432")
    cur = con.cursor()

    cur.execute("SELECT MVE, X, Y from MOUSE WHERE ID = '1'");
    row = cur.fetchall()
    if ( row[0][0] == '1'):
        c = Control()
        c.moveMouse(x,y,row[0][1], row[0][2])
        cur.execute(
            "UPDATE MOUSE set x = %s, y=%s where id = 1",(x,y));
        con.commit()
        print("Coordinates updated")
        con.close()
        return ""
    else:
        print("No movement. toggle off")
        return ""

@app.route('/move/toggle', methods=['GET'])
def toggleTracker():
    con = psycopg2.connect(database="postgres", user="postgres", password="password", host="localhost", port="5432")
    cur = con.cursor()
    cur.execute("SELECT MVE from MOUSE WHERE ID = '1'");
    row = cur.fetchall()
    if (row[0][0] == '1'):
        cur.execute("UPDATE MOUSE set MVE = %s where id = 1", ("0"));
    else:
        cur.execute("UPDATE MOUSE set MVE = %s where id = 1", ("1"));
    con.commit()
    print("Record inserted successfully")
    con.close()
    return ""


if __name__ == '__main__':
    app.run()