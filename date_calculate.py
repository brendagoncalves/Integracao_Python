
import datetime




def calculate_date():
  week_day = datetime.date.today().weekday()

  if week_day == 0: #segunda
    return(datetime.date.today() + datetime.timedelta(-3))   

  if week_day == 1: #terça
    return(datetime.date.today() + datetime.timedelta(-1))

  if week_day == 2: #quarta
    return(datetime.date.today() + datetime.timedelta(-1))

  if week_day == 3: #quinta
    return(datetime.date.today() + datetime.timedelta(-1))

  if week_day == 4: #sexta
    return(datetime.date.today() + datetime.timedelta(-1))


dt_start = calculate_date().strftime('%Y-%m-%d')