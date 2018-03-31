import requests
import json

"""
For the examples we are using 'requests' which is a popular minimalistic python library for making HTTP requests.
Please use 'pip install requests' to add it to your python libraries.
"""

#portfolioAnalysisRequest = requests.get("https://www.blackrock.com/tools/hackathon/performance", params= {'identifiers':"IXN"})
#portfolioAnalysisRequest.text # get in text string format
#portfolioAnalysisRequest.json # get as json object


# company string, start date, end date

def getData(company, start, end): 
	request = requests.get("https://www.blackrock.com/tools/hackathon/performance", params= {'identifiers': company, 'startDate': start, 'endDate': end})
	obj = json.loads(request.text)
	returns = obj["resultMap"]["RETURNS"]
	performance = []
	for i in range(len(returns)):
		performance = performance + returns[i]["performanceChart"]
	if len(performance) > 30:
		return performance[-30:]
	else:
		return performance

print(getData("IDX", '', 20161231))

