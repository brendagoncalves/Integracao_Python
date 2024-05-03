import pyodbc
import pandas as pd
import io

import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import get_data_count as cd
import connection as c


def dimension_formated_update():
      with pyodbc.connect(c.conn) as cnx:
            cursor = cnx.cursor()
            sql = f"""
            UPDATE planilha_leads_semanal
            SET domain = SUBSTRING(domain , 0, CharIndex('#', domain) )
            UPDATE planilha_leads_semanal
            SET domain = replace(domain , '.teste.com/', '')
            """
            cursor.execute(sql)

            print('Dados formatados')

def export_xlsx():

      conn_sql = pyodbc.connect (c.conn)

      with pd.ExcelWriter("planilha_leads_semanal.xlsx", engine='xlsxwriter', options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:              
            df= pd.read_sql(""" select
                                    distinct
                                          ii.UserID, ii.Cnpj, b.Domain, Company, ii.Name, seg.Name [Segment], Phone, ii.Email
                                         from
                                             Base_01..planilha_leads_semanal b
                                         inner join
                                           Base_01..UserTable (nolock) ii on ii.Domain = b.Domain
                                         inner join
                                            Base_01..Segment (nolock) seg on seg.SegmentID = ii.SegmentID """, conn_sql)


            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            output.seek(0)

            count_dt = cd.data_count()

            send_from = c.Email_sender
            gmail_pwd = c.Password_sender
            send_to = c.Email_receiver
            subject = 'Base Lead Diário'
            body = f"""
                    <p><b>Data Extração&nbsp;................:</b> {cd.period} </p>
                    <p><b>Quantidade Instalações:</b>   {count_dt} </p> """

            report_name = "planilha_leads_semanal.xlsx"


            msg = MIMEMultipart()
            msg['Subject'] = subject  # add in the subject
            msg['From'] = send_from
            msg['To'] = send_to
            msg.attach(MIMEText(body, 'html'))  # add text contents
            file = MIMEApplication(output.read(), name=report_name)
            file['Content-Disposition'] = f'attachment; filename="{report_name}"'
            msg.attach(file)


            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.ehlo()
                smtp.login(send_from, gmail_pwd)
                smtp.send_message(msg)
                smtp.quit()


                print('Enviado por email')







