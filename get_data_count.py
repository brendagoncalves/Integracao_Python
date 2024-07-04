
import pyodbc
import datetime
import connection as c




def data_count():

    with pyodbc.connect(c.conn) as cnx:
        cursor = cnx.cursor()
        sql = """SELECT
               count(domain) 
               FROM
                  InstallFilterDomain """

        cursor.execute(sql)

        list_result = []

        for row in cursor.fetchall():
            list_result.append(row[0])
        return(list_result)

count_dt = data_count()
