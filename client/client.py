
import urllib

from flask import Flask


app = Flask(__name__)



@app.route('/search/<word>', methods=['GET'] )
def search_dos(word):	
	return  urllib.request.urlopen("http://127.0.0.1:5001/query_by_subject/" + word).read()

	 
 




if __name__ == '__main__':
    app.run(debug = True,host = "127.0.0.2", port ="5001")    