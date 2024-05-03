
from ast import parse
from itertools import count
import string
from time import strptime
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2
import pandas as pd
import pyodbc
import json 
import connection as co
from date_calculate import dt_start


#Create service credentials
#Rename your JSON key to client_secrets.json and save it to your working folder
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', ['https://www.googleapis.com/auth/analytics.readonly'])

#Create a service object

http = credentials.authorize(httplib2.Http())
service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))
response = service.reports().batchGet(

    body ={
    'reportRequests':  [{'viewId': '77788874',
            'dateRanges': [{'startDate': dt_start, 'endDate': 'yesterday'}],
            'dimensions': [{'name': 'ga:pagePath'}],                                   
            'metrics': [{'expression':'ga:pageviews'}],

            "filtersExpression":'ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx,ga:pagePath=@signature/xxxxxxx'
    
            }]                                    
        }

         ).execute()



#create two empty lists that will hold our dimentions and sessions data

dim = []


 #Extract Data
for report in response.get('reports', []):

    columnHeader = report.get('columnHeader', {})
    dimensionHeaders = columnHeader.get('dimensions', [])

    rows = report.get('data', {}).get('rows', [])

    for row in rows:

        dimensions = row.get('dimensions', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
                  dim.append(dimension)
 


 #Sort Data
dim.reverse()

df = pd.DataFrame()
df["pagePath"] = dim


def truncate_table():
  with pyodbc.connect(co.conn) as cnx:
      cursor = cnx.cursor()
      sql = f"""truncate table GetLeads"""  

      cursor.execute(sql)


def get_domain():   
  with pyodbc.connect(co.conn) as cnx:
    for count_str in dim:
      if '.teste.com' in count_str:
        find_str = str.rfind(count_str, '.teste.com')
        value_str = count_str[:find_str] 

        cursor = cnx.cursor()
        sql = f""" 
        insert into GetLeads (domain)
        VALUES('{value_str}')"""  
        cursor.execute(sql)
        cursor.close()

















