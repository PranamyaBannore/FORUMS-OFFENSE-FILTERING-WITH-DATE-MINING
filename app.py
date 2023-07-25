from flask import Flask, render_template, url_for
from bs4 import BeautifulSoup
import requests
import tldextract # The module looks up TLDs in the Public Suffix List, mantained by Mozilla volunteers
import sqlite3
import urllib.parse as urp 

forumUrl = ""
filterWords = ""
isRecursive = False
preDefDict = ["Encryption","ddos","Malware","Ransomware","virus","Android","layout","MVP","Tagger","contextual","capture","intense","refresh","populate","phishing","keylogging","MITM","CNN","VPN","wireshark","botnet","bat","script","hijack","exe","rar","payload","Trojans","intrusion","wap","wep","wpa","wps","password","dickhead","composer","candemoniun","braga","fucker","brevis","curvature","splenic"]
maxlinks = 500

sqliteConnection = sqlite3.connect('SQLite_Python.db')
cursor = sqliteConnection.cursor()
print("Connected to SQLite")

sql_fetch_blob_query = """SELECT * from tb_config"""
cursor.execute(sql_fetch_blob_query)
record = cursor.fetchall()
for row in record:
		forumUrl = row[0]
		print("Fetched Url : "+row[0])
		if len(row[1])>0:
			filterWords = row[1].replace(" "," ").split(" ")
		else:
			filterWords = preDefDict
		print("Fetched Keywords : "+row[1])
		if row[2] == 'True':
			isRecursive = True
			print("Recursion : True")
		recursionLevel = row[3]
		print("recursionLevel  : ",row[3])

cursor.close()
sqliteConnection.close()
flag = 0


# url = 'https://www.geeksforgeeks.org/multithreading-python-set-1/'
forumUrl = forumUrl.strip("www")
url_info = tldextract.extract(forumUrl)
url_domain = "{}.{}".format(url_info.subdomain,url_info.registered_domain)
erLinks = []
nLinks = []
mLinks = dict()
sLinks=[]
gLinks = []

def getRecursiveUrl(url,level=0):
	global flag
	try:
		page = requests.get(url)
		# print(page.text)

		# nLinks.append(url)
	except:
		print(url + " : Failed to load")
		erLinks.append(url)	
		return

	soup = BeautifulSoup(page.text, 'html.parser')
	links = soup.find_all('a')
	if links is None or len(links) == 0:
		nLinks.append(url)
		# print(level+" : "+url)
		return 1;
	else:
		for x in links:
			try:
				href = urp.urljoin(forumUrl, x['href'])
			except Exception as e:
				print("Error : ",x)
			else:
				
				# if (href and url_domain in href and href not in nLinks and "#" not in href and forumUrl in href and flag < maxlinks):
				# if (href and href not in nLinks and "#" not in href  ):
				if (href and url_info.registered_domain in href and href not in nLinks and "#" not in href and len(href)>len(forumUrl) and flag < maxlinks):
					flag = flag+1
					if (level <= recursionLevel):
						nLinks.append(href)
						print("    "*level,href)

					elif(recursionLevel == -1):
						nLinks.append(href)
						print("    "*level,href)
						if isRecursive:
							getRecursiveUrl(href,level+1)
						else:
							print("Stuck")
					else:
						print("Stuck2")
				else :
					print("OUT",href[:])
					gLinks.append(href)

			finally:
				pass



def parsePages(links):
	for link in links:
		flags  = False
		try:
			page = requests.get(link)
			print("Filtering : ",link)
		except:
			print(link + " : Failed to load")
			erLinks.append(link)
			continue
		pageText = page.text
		soup = BeautifulSoup(page.text, 'html.parser')
		if soup.find('title') != None :
			title = soup.find('title').text
		else : title = link
		#print(pageText)	
		for word in filterWords:
			if " "+word.lower()+" " in pageText.lower():	
				if link in mLinks:
					mLinks[link][1].append(word)
				else:
					mLinks[link] = [title,[word,]]
				flags = True
				# mLinks.append(link)
		if not flags:
			sLinks.append([title,link])
			# sLinks.append([soup.find('title').text,link])
			



def filter():
	print(forumUrl)
	print(filterWords)
	print("{},{},{}".format(url_info.subdomain,url_info.registered_domain,url_info.domain))
	if isRecursive:
		getRecursiveUrl(forumUrl)
	else:
		nLinks.append(forumUrl)
	print("{} sub-links found".format(len(nLinks)))
	parsePages(nLinks)
	print(nLinks)
	print("\n\n\n Matched Links : ",len(mLinks))
	for match in mLinks:
		print(match)

def getFilterData():
	tsite= forumUrl.replace("https://","").replace("https://","")
	fData = {
				"site":tsite,
				"totalLinks":len(nLinks)+len(gLinks),
				"externalLinks":len(gLinks),
				"filteredLinks":[len(nLinks),len(erLinks)],
				"safeLinks":len(sLinks),
				"harmfulLinks":len(mLinks),
				"filteredWords":filterWords,
				"safeLinksArr":sLinks,
				"harmfulLinksArr":mLinks
			}

	return fData



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('intro.html')
   
@app.route('/dashboard')
def dashboard():
    return render_template('index.html',data=getFilterData())
   
if __name__ == "__main__":
	filter()
	# app.run(debug=True ,port="80", host ='0.0.0.0')
	app.run(port="80", host ='0.0.0.0' ,use_reloader=False)
	# webbrowser.open_new_tab(forumUrl)
	# webbrowser.open_new_tab("localhost")