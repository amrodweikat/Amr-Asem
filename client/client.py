
import urllib

from flask import Flask


app = Flask(__name__)



@app.route('/search/<word>', methods=['GET'] )
def search(word):
	return  urllib.request.urlopen("http://127.0.0.1:5001/query_by_subject/" + word.replace(" ", "")).read() #called the query_by_subject function in catalog server

	 
@app.route('/lookup/<number>', methods=['GET'] )
def lookup(number):	
	return  urllib.request.urlopen('http://127.0.0.1:5001/query_by_item/' + number).read() #called the query_by_item function in catalog server


@app.route('/buy/<number>', methods=['POST'] )
def buy(number):
	return urllib.request.urlopen('http://127.0.0.1:5003/buy/' + number).read() #called the buy function in order server


@app.route('/<any>/<anything>', methods=['GET','POST'] )
def anything(any,anything):
	return "This operation not supported" #when the operation not search,not lookup and not buy


if __name__ == '__main__':
    app.run(debug = True,host = "127.0.0.2", port ="5001")    