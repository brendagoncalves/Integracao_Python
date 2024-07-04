
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import httplib2
import pandas as pd
import pyodbc
import json
import connection as co
from date_calculate import dt_start, dt_end

import urllib
from sqlalchemy import create_engine


#Create service credentials
#Rename your JSON key to client_secrets.json and save it to your working folder
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', ['https://www.googleapis.com/auth/analytics.readonly'])

#Create a service object

http = credentials.authorize(httplib2.Http())
service = build('analytics', 'v4', http=http, discoveryServiceUrl=('https://analyticsreporting.googleapis.com/$discovery/rest'))
response = service.reports().batchGet(

    body ={
    'reportRequests':  [{'viewId': '***********',
            'dateRanges': [{'startDate': '2023-06-01', 'endDate': 'today'}],
            'dimensions': [{'name': 'ga:pagePath'}],
            'metrics': [{'expression':'ga:pageviews'}],

            "filtersExpression":'ga:pagePath=@upstore'

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

df = pd.DataFrame (dim, columns = ['domain'])

# conexão com o banco
conn = pyodbc.connect(co.conn)
quoted = urllib.parse.quote_plus(co.conn)
engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(quoted))

k_upstore = co.Key_Upstore


def setUpstore(upstore):
  
   with conn as cnx:
    cursor = cnx.cursor()
    update_up = f"update InstallFilterDomain set upstore = '{upstore}' where upstore is null" 
    cursor.execute(update_up)
    


def setDomain():
  
  with conn as cnx:
    cursor = cnx.cursor()
    update_d = f""" update InstallFilterDomain
                    set domain = replace(SUBSTRING(domain, 0, CharIndex('#', domain) ), '.teste.com/', '') """
    cursor.execute(update_d)
    return update_d


def set_main():
    with conn as cnx:
        cursor = cnx.cursor()
        sql = f"delete from InstallFilterDomain"
        cursor.execute(sql)

    for up in k_upstore:    
        words = df[df['domain'].str.contains(up)] 
        words.to_sql('InstallFilterDomain', if_exists='append', con=engine)

        # update InstallFilterDomain upstore is null (=up)
        setUpstore(up)
    #update InstallFilterDomain set domain 
    setDomain()

    





























