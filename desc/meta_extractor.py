#!/usr/bin/python

##########################
# using request:
#   when get html, content decode wrong for some charset.
#	using urllib2 instead of
##########################
from bs4 import BeautifulSoup
#import requests
from thread_pool import ThreadPool
import io
import urllib2


hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def check_valid(protocol, domain):
    url = protocol + domain
    try:
    	req = urllib2.Request(url, headers=hdr)
    	page = urllib2.urlopen(req)
    	html = page.read()
    	status = page.getcode()
    	#r = requests.get(url)
    	#status = r.status_code
    	with open("already.txt", "a") as f:
			f.write(url + " -> " + str(status) + "\r\n")
    	if status == 200:
    		get_meta_data(domain, url, html)
    except Exception, e:
    	#print(url + " -> " + str(e))
    	with open("error.txt", "a") as f:
			f.write(url + " -> " + str(e) + "\r\n")

def get_meta_data(domain, url, html):
	#print(domain + " -> " + url)
	soup = BeautifulSoup(html, "html.parser")
	metas = soup.find_all('meta')
	#print(meta)
	desc = [ meta.attrs['content'] for meta in metas if 'name' in meta.attrs and (meta.attrs['name'] == 'description' or meta.attrs['name'] == 'Description') ]
	if len(desc) > 0:
		#print(desc[0].encode('utf-8'))
		with io.open("desc.data", "a") as f:
			f.write(domain + "\t" +url + "\t" + " ".join(desc[0].splitlines())  + "\r\n")
	else:
		with open("nodesc.txt", "a") as f:
			f.write(url + " -> No Description !" + "\r\n")
			#print('No Description !')

exists = list()
if __name__ == "__main__":
	print("start ---- ")
	domains = list()
	with open("exist.data", "rt") as f:
		exists = [url.strip() for url in f.readlines()]
	with open("domains.data", "rt") as f:
		domains = [url.strip() for url in f.readlines()]
	print("Size Exist: " + str(len(exists)))
	print("Size Domain: " + str(len(domains)))
    # Function to be executed in a thread
	def extract_meta(domain):
		d = domain.split(",")[0].replace("(", "")
		#print("----->" + d.strip())
		if d not in exists:
			with open("exist.data", "a") as f:
				f.write(d + "\r\n")
			check_valid("http://", d)
			check_valid("https://", d)
        #print("sleeping for (%d)sec" % d)
        #sleep(d)

    # Generate random delays
    #delays = [randrange(3, 7) for i in range(50)]

    # Instantiate a thread pool with 5 worker threads
	pool = ThreadPool(100)

    # Add the jobs in bulk to the thread pool. Alternatively you could use
    # `pool.add_task` to add single jobs. The code will block here, which
    # makes it possible to cancel the thread pool with an exception when
    # the currently running batch of workers is finished.
	pool.map(extract_meta, domains)
	pool.wait_completion()

#exists = list()
#domains = list()
#with open("exist.data", "rt") as f:
#    exists = [url.strip() for url in f.readlines()]
#
#with open("domains.data", "rt") as f:
#    domains = [url.strip() for url in f.readlines()]
#
#for domain in domains:
#	d = domain.split(",")[0].replace("(", "")
#	if d not in exists:
#		with open("exist.data", "a") as f:
#			f.write(d + "\r\n")
#		check_valid("http://", d)
#		check_valid("https://", d)
    		#print(d)
            #if domain not in exists:
	
	#soup = BeautifulSoup(open(html_doc), "html.parser")
	#print "--- process: {}".format(html_doc)

#channel_index = []
#for i in soup.find("ul", { "class" : "list-channel" }).findAll("li"):
