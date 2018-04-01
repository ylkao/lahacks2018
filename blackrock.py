import requests
import json
import csv

"""
For the examples we are using 'requests' which is a popular minimalistic python library for making HTTP requests.
Please use 'pip install requests' to add it to your python libraries.
"""

#portfolioAnalysisRequest = requests.get("https://www.blackrock.com/tools/hackathon/performance", params= {'identifiers':"IXN"})
#portfolioAnalysisRequest.text # get in text string format
#portfolioAnalysisRequest.json # get as json object


# company string, start date, end date
# use Blackrock API to retrieve data about a company
def getData(company, start, end): 
	request = requests.get("https://www.blackrock.com/tools/hackathon/performance", params= {'identifiers': company, 'startDate': start, 'endDate': end})
	obj = json.loads(request.text) #convert response to JSON object
	if 'RETURNS' not in obj["resultMap"]:
		print(company, "does not have RETURNS")
		return []
	returns = obj["resultMap"]["RETURNS"]
	performance = []

	#get performance charts points and return last 30
	for i in range(len(returns)):
		performance = performance + returns[i]["performanceChart"]
	if len(performance) > 30:
		performance = performance[-30:]
	end = end + 10000

	request = requests.get("https://www.blackrock.com/tools/hackathon/performance", params= {'identifiers': company, 'startDate': end})
	obj = json.loads(request.text) #convert response to JSON object

	if 'RETURNS' in obj["resultMap"]:
		performance = performance + [obj["resultMap"]["RETURNS"][0]["performanceChart"][0]]
	else:
		print(company, "does not have RETURNS")

	return performance

# data will look like [[1,2],[3,4]]
# clean to >>> [2, 4]
def cleanData(data): 
	cleaned = []
	for i in range(len(data)):
		cleaned += [data[i][1]]
	return cleaned

def writeData(rows):
	with open('performance.csv', 'a') as f:
	    writer = csv.writer(f)
	    for r in rows:
	    	writer.writerow(r)

#get company names from csv file
def getCompanies():
	with open('all_sentiment.csv') as f:
		firstColumn = [line.split(',')[0] for line in f if line.split(',')[0] != "Ticker"]
	return firstColumn

def main():
	endDates = [20090101,20090401,20090701,20091001,20100101,20100401,20100701,20101001,20110101,
20110401,20110701,20111001,	20120101,20120401,20120701,	20121001,20130101,20130401,20130701,20131001,20140101,	20140401,20140701,20141001,	20150101,20150401,20150701,
20151001,20160101, 20160401,20160701,20161001,20170101,	20170401,20170701,20171001]
	companies = getCompanies()
	rows = []
	for comp in companies:
		print(comp, "starting")
		data = [comp]
		for date in endDates:
			points = cleanData(getData(comp, '', date))
			data += [points]
		rows += [data]
		print(comp, "ended")
		if len(rows) % 2 == 0:
			writeData(rows)
			rows = []
	if len(rows) != 0:
		writeData(rows)

main()



####### NOTE TO SELF SKIPPED MAXY, GLCH, VOLC, GNCMA
