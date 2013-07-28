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
    cur.callproc('everyday_check')
    cur.close()
    conn.close()
    print '%s进行了A网结算'%(str(datetime.now()))

if __name__ == "__main__":
    main()
