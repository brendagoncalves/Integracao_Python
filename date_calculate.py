
import datetime



def calculate_date():
    week_day = datetime.date.today().weekday()

    if week_day == 0: #segunda
        return(datetime.date.today() + datetime.timedelta(-3)), (datetime.date.today() + datetime.timedelta(-1))
    else:
        return(datetime.date.today() + datetime.timedelta(-1)), (datetime.date.today() + datetime.timedelta(-1))


dt_start,dt_end = calculate_date()

dt_today = datetime.date.today().strftime('%d/%m/%Y')


