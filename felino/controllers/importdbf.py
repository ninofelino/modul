from sqlalchemy import *
from dbfread import DBF
import psycopg2
import datetime
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert

conn = psycopg2.connect("host='localhost' dbname='developper' user='felino' password='felino'")
cursor=conn.cursor()

listOfUkuran=['O','S','M','L','XL','2','3','4','5','6','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']
engine = create_engine("postgresql://felino:felino@localhost/developper")
con = engine.connect() 
con.execute("delete from felino_felino;")
for item in DBF('/mnt/poserver/ics/DAT/INV.DBF',encoding='iso-8859-1'):
    list=item['DESC1'].split(" ")
    try:
       ukuran=list[len(list)-1][-2:]
       article=list[0]+' '+list[1]
       print item['CODE']
       print list.count
       con.execute(text('INSERT INTO felino_felino (id,article,ukuran) VALUES (:barcode,:article,:ukuran) '),\
       {"barcode":item['CODE'],"article":article,"ukuran":ukuran})
    except:
        print "error"  