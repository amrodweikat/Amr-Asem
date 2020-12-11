
import urllib
import time
import random
from flask import Flask
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

#cache contains 8 items => 4 items represent request and 4 items represent results of requests
index = 0

catalog = 1
order = 1

def round_robin_catalog():
	global catalog
	if catalog==1:
		catalog=2
		return "127.0.0.1:5001"
	else:
		catalog=1
		return "127.0.0.1:5005"


def round_robin_order():
	global order
	if order==1:
		order=2
		return "127.0.0.1:5003"
	else:
		order=1
		return "127.0.0.1:5007"



def check_cache(request):
	global index
	if index > 3:
		index = 0
	for i in range(4):
		if  cache.get(i)== request:
			return "true",cache.get(i+10)
	return "false",None


@app.route('/<number>',methods=['GET'])
def invalid_request_cache(number):
	for i in range(4):
		if  cache.get(i)== "lookup/"+str(number):
			cache.set(i,None,10000)
			return ""
	return ""


@app.route('/search/<word>', methods=['GET'] )
def search(word):
	global index
	result = None
	t1 = time.time()
	w = list(check_cache("search/"+str(word)))
	if w[0] == "false":
		result = urllib.request.urlopen("http://"+round_robin_catalog()+"/query_by_subject/" + word.replace(" ", "")).read() #called the query_by_subject function in catalog server first replica or second replica
		cache.set(index,"search/"+str(word),10000)
		cache.set(index+10,result,10000)
		index=index+1
	else:
		result=w[1]	
	t2 = time.time()
	print("\ntime_search: "+str(t2-t1))
	print("index: "+str(index))
	print("next catalog replica number: "+str(catalog))
	return result

	
 
@app.route('/lookup/<number>', methods=['GET'] )
def lookup(number):
	global index
	result = None
	t1 = time.time()
	w = list(check_cache("lookup/"+str(number)))
	if w[0] == "false":
		result = urllib.request.urlopen("http://"+round_robin_catalog()+"/query_by_item/" + number).read() #called the query_by_item function in catalog server first replica or second replica
		cache.set(index,"lookup/"+str(number),10000)
		cache.set(index+10,result,10000)
		index=index+1
	else:
		result=w[1]	
	t2 = time.time()
	print("\ntime_search: "+str(t2-t1))
	print("index: "+str(index))
	print("next order replica number: "+str(order))
	return result	


@app.route('/buy/<number>', methods=['POST'] )
def buy(number):
	return urllib.request.urlopen("http://"+round_robin_order()+"/buy/" + number).read() #called the buy function in order server first replica or second replica


@app.route('/<any>/<anything>', methods=['GET','POST'] )
def anything(any,anything):
	return "This operation not supported" #when the operation not search,not lookup and not buy


if __name__ == '__main__':
    app.run(debug = True,host = "127.0.0.1", port ="4502")    