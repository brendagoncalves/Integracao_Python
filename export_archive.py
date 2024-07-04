import pyodbc
import pandas as pd
import io

import smtplib

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from get_data_count import count_dt
import connection as c

from date_calculate import dt_start, dt_end, dt_today

def export_xlsx():

      conn_sql = pyodbc.connect (c.conn)

      with pd.ExcelWriter("planilha_leads_semanal.xlsx", engine='xlsxwriter', options = {'strings_to_numbers': True, 'strings_to_formulas': False}) as writer:              
            df= pd.read_sql(""" select
                                    distinct
                                          ii.UserID, ii.Cnpj, b.Domain, Company, ii.Name, seg.Name [Segment], Phone, ii.Email
                                         from
                                             Base_01..InstallFilterDomain b
                                         inner join
                                           Base_01..UserTable (nolock) ii on ii.Domain = b.Domain
                                         inner join
                                            Base_01..Segment (nolock) seg on seg.SegmentID = ii.SegmentID """, conn_sql)



            output = io.BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1')
            writer.save()
            output.seek(0)


            send_from = c.Email_sender
            gmail_pwd = c.Email_password
            send_to = c.Email_receiver
            subject = f"Analytics - Lead Semanal: {dt_today} "
            periodo = f"{dt_start} a {dt_end}"
            body = f"""
                    <p><b>Período&nbsp;..........................:</b> { dt_end if dt_start == dt_end else periodo } </p>
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







