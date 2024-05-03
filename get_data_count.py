
import pyodbc
import datetime
import connection as c



period = datetime.datetime.now()


def data_count():

    with pyodbc.connect(c.conn) as cnx:
        cursor = cnx.cursor()
        sql = """SELECT
               count(distinct Domain) 
               FROM
                  GetLeads """

        cursor.execute(sql)

        list_result = []

        for row in cursor.fetchall():
            list_result.append(row[0])
        return(list_result)

