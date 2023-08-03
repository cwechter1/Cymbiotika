# from apiclient.discovery import build
# from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime, timedelta, date
import json
import requests

today = date.today()
start_date = date(2023, 1, 1)
y = today - timedelta(days = 1)

page = 0

l = 250

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '/Users/cymbiotika/Desktop/CymbiotikaCody/GA/client_secrets.json'
VIEW_ID = '240793260'

credentials = service_account.Credentials.from_service_account_file(KEY_FILE_LOCATION)

analytics = build('analyticsreporting', 'v4', credentials=credentials)
while start_date <= date.today():
	minim = start_date.strftime('%Y-%m-%d')
	maxim = start_date.strftime('%Y-%m-%d')
	response = analytics.reports().batchGet(body={
	'reportRequests': [{
		"viewId": VIEW_ID,
		"dateRanges": [{'startDate': minim, 'endDate': maxim}],
		"metrics": [
			{"expression": "ga:sessions"},
		],
			"dimensions": [
				{"name": "ga:date"},
			],
			"pageSize": 10000	
			
	}]
	}). execute()
	total_sessions = 0
	reports = response.get('reports', [])
	if reports:
		rows = reports[0].get('data', {}).get('rows', [])
		if rows:
			total_sessions = int(rows[0]['metrics'] [0]['values'][0])
		else:
			print('No Rows Found')
	else:
		print('No Reports Found')
	print("Date: {}".format(start_date))
	print("Total Sessions: {}".format(total_sessions))
	start_date += timedelta(days=1)
# count = 0 

# reports = response['reports']

# events = []

# for i in reports :

# 	data = i['data']

# 	info = data['rows']

# 	for d in info :

# 		url = d['dimensions'][0]

# 		if_cx = url.split('/')[5]

# 		pg = if_cx.split('?')[0]

# 		if '&cxcancel' in if_cx :
			
# 			cx = True

# 		elif '&cxcancel' not in if_cx :

# 			cx = False	

# 		hash_ = url.split('/')[4]

# 		time = d['dimensions'][1]
# 		metrics = d['metrics']

# 		for m in metrics :
				
# 			u_v = m['values'][0]

# 			t_p = m['values'][1]

# 			for i in u_v :

# 				count = count + 1

# 				events.append({'date': time,
# 				'hash': hash_, 
# 				'unique_visit': u_v,
# 				'time_on_page': t_p,
# 				'page': pg,
# 				'cx_cancel': cx})

# for e in events :

# 	for c in i_c :

# 		if e['hash'] == c['hash'] :

# 			print(True)

# 			e['status'] = c['status']
# 			e['created_at'] = c['created_at']

# print(events)			

# events = pd.DataFrame(events)

# events.to_csv('Events.csv', index=False)




