

from flask import Flask
import urllib

app = Flask(__name__)



@app.route('/buy/<number>',methods=['GET'])
def buy(number):
	if (number.isnumeric()) and (int(number) <= 7) and (int(number) >= 1):
		quantity = urllib.request.urlopen('http://0.0.0.0:5006/query/' + number).read()
		if int(quantity) > 0:
			return urllib.request.urlopen('http://0.0.0.0:5006/update/' + number).read()
		else:
			return "The buy request failed because the item is out ot stock"	

	else:
		return "This operation not supported"	




if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True,port=5008)   



