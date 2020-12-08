
import urllib
import time
from flask import Flask
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

app = Flask(__name__)
cache.init_app(app)

catalog = 1

order_server_first_replica="127.0.0.1:5003"
order_server_second_replica="127.0.0.1:5007"


def round_robin_catalog():
	global catalog
	if catalog==1:
		catalog=2
		return "127.0.0.1:5001"
	else:
		catalog=1
		return "127.0.0.1:5005"


#the result of this function will be in the cache for 120s 
@cache.cached(timeout=120)
def search_cache(word):
	return  urllib.request.urlopen("http://"+round_robin_catalog()+"/query_by_subject/" + word.replace(" ", "")).read() #called the query_by_subject function in catalog server first replica or second replica



@app.route('/search/<word>', methods=['GET'] )
def search(word):
	t1 = time.time()
	w = search_cache(word)
	t2 = time.time()
	print("\ntime_search: "+str(t2-t1)+"\n")
	print("next replica number: "+str(catalog)+"\n")
	return w

	
#the result of this function will be in the cache for 120s 
@cache.cached(timeout=120)
def lookup_cache(number):
	return  urllib.request.urlopen('http://127.0.0.1:5001/query_by_item/' + number).read() #called the query_by_item function in catalog server


	 
@app.route('/lookup/<number>', methods=['GET'] )
def lookup(number):
	t1 = time.time()
	w = lookup_cache(number)
	t2 = time.time()
	print("\ntime_lookup: "+str(t2-t1)+"\n")
	return w	


@app.route('/buy/<number>', methods=['POST'] )
def buy(number):
	return urllib.request.urlopen('http://127.0.0.1:5003/buy/' + number).read() #called the buy function in order server


@app.route('/<any>/<anything>', methods=['GET','POST'] )
def anything(any,anything):
	return "This operation not supported" #when the operation not search,not lookup and not buy


if __name__ == '__main__':
    app.run(debug = True,host = "127.0.0.2", port ="5001")    