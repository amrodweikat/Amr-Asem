
import urllib
import time
import random
from flask import Flask,jsonify
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

#cache contains 8 items => 4 items represent request and 4 items represent results of requests
index = 0


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


#@cache.cached(timeout=120)
def search_cache():
	for x in range(10000):
		s = random.randint(1,10)
	return str(random.randint(1,100))	

	#return  urllib.request.urlopen("http://"+round_robin_catalog()+"/query_by_subject/" + word.replace(" ", "")).read() #called the query_by_subject function in catalog server first replica or second replica


def check_cache(request):
	global index
	if index > 3:
		index = 0
	for i in range(4):
		if  cache.get(i)== request:
			return "true",cache.get(i+10)
	return "false",None


@app.route('/<number>',methods=['GET'])
def hello(number):
	#cache.set(str(number)+"lookup/")
	#return "Hi from windows"
	books={"id":2,"lab":2}
	w = jsonify(books).text + "Hi"
	return w



@app.route('/search/<word>', methods=['GET'] )
def search(word):
	global index
	result = None
	t1 = time.time()
	w = list(check_cache("search/"+str(word)))
	if w[0] == "false":
		result = search_cache()
		cache.set(index,"search/"+str(word),10000)
		cache.set(index+10,result,10000)
		index=index+1
	else:
		result=w[1]	
	t2 = time.time()
	print("\ntime_search: "+str(t2-t1))
	print("index: "+str(index))
	#print("next replica number: "+str(catalog)+"\n")
	return result

	
#the result of this function will be in the cache for 120s 
@cache.cached(timeout=120)
def lookup_cache(number):
	return  urllib.request.urlopen("http://"+round_robin_catalog()+"/query_by_item/" + number).read() #called the query_by_item function in catalog server first replica or second replica


	 
@app.route('/lookup/<number>', methods=['GET'] )
def lookup(number):
	t1 = time.time()
	w = lookup_cache(number)
	t2 = time.time()
	print("\ntime_lookup: "+str(t2-t1)+"\n")
	print("next replica number: "+str(catalog)+"\n")
	return w	


@app.route('/buy/<number>', methods=['POST'] )
def buy(number):
	return urllib.request.urlopen("http://"+round_robin_order()+"/buy/" + number).read() #called the buy function in order server first replica or second replica


@app.route('/<any>/<anything>', methods=['GET','POST'] )
def anything(any,anything):
	return "This operation not supported" #when the operation not search,not lookup and not buy


if __name__ == '__main__':
    app.run(debug = True,host = "127.0.0.1", port ="4502")    