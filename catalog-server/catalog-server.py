

from flask import Flask,jsonify
import sqlite3

app = Flask(__name__)


def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn



@app.route('/query_by_subject/<word>',methods=['GET'])
def query_by_subject(word):
	if (word == "distributedsystems") or (word == "graduateschool"):
		conn   = db_connection()
		cursor = conn.cursor()
		cursor = conn.execute("SELECT id,title FROM book WHERE topic='"+word+"'")
		books = [
			dict(id=row[0],title=row[1])
			for row in cursor.fetchall()
		]
		if books is not None:
			return jsonify(books)

	else:
		return "This operation not supported"



@app.route('/query_by_item/<number>',methods=['GET'])
def query_by_item(number):
	if (number.isnumeric()) and (int(number) <= 7) and (int(number) >= 1):
		conn   = db_connection()
		cursor = conn.cursor()
		cursor = conn.execute("SELECT title,quantity,price FROM book WHERE id="+number)
		books = [
			dict(title=row[0],quantity=row[1],price=row[2])
			for row in cursor.fetchall()
		]
		if books is not None:
			return jsonify(books)

	else:
		return "This operation not supported"




@app.route('/query/<number>',methods=['GET'])
def query(number):
	conn   = db_connection()
	cursor = conn.cursor()
	cursor = conn.execute("SELECT quantity FROM book WHERE id="+number)
	rows   = cursor.fetchall()
	return str(rows).strip('[]').strip('()').strip(',')

	



@app.route('/update/<number>',methods=['GET'])
def update(number):
	conn   = db_connection()
	cursor = conn.cursor()
	cursor = conn.execute("SELECT * FROM book WHERE id="+number)
	data = cursor.fetchone()
	if data[1] > 0:
		num = data[1]-1
		query = conn.execute("UPDATE book SET quantity = ? WHERE id="+number,(num,))
		conn.commit()
		return "Done"
	else:
		return "The buy request failed because the item is out ot stock"





if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port=5002)   



