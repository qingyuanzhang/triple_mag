#coding=utf-8
import warnings
from warnings import filterwarnings
#import MySQLdb
from datetime import *
import warnings
from warnings import filterwarnings
import MySQLdb as Database
filterwarnings('ignore', category = Database.Warning)
def main():
    conn=Database.connect(host="localhost",user="rtyk_triple",passwd="winter4coming",db="rtyk_triple",charset="utf8") 
    cur = conn.cursor()
#    cur.callproc('everyday_check')
    cur.execute("delete from `rtyk_triple`.`django_session`") 
    conn.commit()
    cur.close()
    conn.close()
    
    print 'helloworld'
if __name__ == "__main__":
    main()
