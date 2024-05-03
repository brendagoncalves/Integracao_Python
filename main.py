
import analytics_connection 
import export_archive as u
import analytics_tst as a

def main():
    a.truncate_table()
    a.get_domain()
    u.export_xlsx()
    
  
if __name__ == '__main__':
    main()
