
import json


with open("config_app.json", "r", encoding='utf-8') as json_config:
  data = json.load(json_config)

  Server          = data["database_login"]['Server']
  User            = data["database_login"]['User']
  Password        = data["database_login"]['Password']
  Driver          = data["database_login"]['Driver']

  Email_sender    = data["Email_config"]['Email_sender']
  Password_sender = data["Email_config"]['Password_sender']
  Email_receiver  = data["Email_config"]['Email_receiver'] 

  conn = f"""Driver={Driver};
             Server={Server};
             Database=Base_01;
             UID={User};
             PWD={Password};unicode_results=True;"""  




         