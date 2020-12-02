

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






if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port=5002)   



