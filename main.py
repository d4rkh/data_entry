from flask import Flask, render_template, request
import flask
import mysql.connector as mysql

app = Flask(__name__)

mydb = mysql.connect(
    host="localhost",
    user="root",
    password="creAdent@1998",
    database="stnames"
)

mycursor = mydb.cursor()

print(mydb)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/update_data', methods=["POST"])
def update_data():
    data = eval(request.data)
    sql_query = 'UPDATE data SET std_name=%s, f_name=%s, age=%s WHERE no=%s'
    val = (data['std_name'], data['f_name'], data['age'], data['id'])
    mycursor.execute(sql_query, val)
    mydb.commit()

    return "", 200

@app.route('/delete_data', methods=["DELETE"])
def delete_data():
    id = int(str(request.data).replace('b', '').replace("'", ''))
    sql_query = f"DELETE FROM data WHERE no={id}"
    mycursor.execute(sql_query)
    mydb.commit()

    return "", 200

@app.route('/get_ids')
def get_ids():
    sql_query = "SELECT * FROM data"
    mycursor.execute(sql_query)
    data = mycursor.fetchall()
    s_data = []

    for x in range(len(data)):
        s_data.append(data[x][0])

    print(s_data)

    resp = flask.Response(f"{s_data}")
    resp.headers["Access-Control-Allow-Origin"] = "*"

    return resp

@app.route('/data_lookup', methods=['POST'])
def data_lookup():
    id = request.form['id']
    sql_query = f"SELECT * FROM data WHERE no={id}"
    mycursor.execute(sql_query)

    data = mycursor.fetchall()

    return f'{list(data[0])}'

@app.route('/data-lookup')
def lookup_data():
    return render_template('data-lookup.html')

@app.route('/data', methods=['POST'])
def data():
    data = dict(request.form)
    sql_query = "INSERT INTO data (std_name, f_name, age) VALUES (%s, %s, %s)"
    val = ( data['std_name'], data['f_name'], data['age'] )
    mycursor.execute(sql_query, val)
    mydb.commit()
    mycursor.execute(f"SELECT * FROM data WHERE std_name='{data['std_name']}'")

    id = mycursor.fetchall()[0][0]

    return f"<pre>Data Entry Created In Database</pre>\n<pre>ID: {id}</pre>", 200

app.run('0.0.0.0')