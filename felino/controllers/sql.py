import datetime
import json
from sqlalchemy import *
import psycopg2
import datetime
from sqlalchemy import Table, MetaData, create_engine
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import insert
from dbfread import DBF
#sudo mount.cifs //192.168.1.254/posserver /mnt/poserver share -o user=nuansa,password=nuansa,vers=2.1

# tidak tampil menu
# DELETE FROM ir_attachment WHERE url LIKE '/web/content/%';



def importInv():
    engine = create_engine("postgresql://felino:felino@localhost/databaru")
    con = engine.connect() 
    conn = psycopg2.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    cur.execute("delete from felino_felino;")
    SQ=''
    uk=['ALL','01','2','3','4','5','O','S','M','L','XL','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']
    X=0
    print(type(uk))
    #for u in uk:
        #SQL="insert into product_attribute_value(id,name,attribute_id,create_uid,write_uid) values(%s,'%s',%s,%s,%s) ON CONFLICT ON CONSTRAINT product_attribute_value_pkey DO NOTHING;"
        #cur.execute(SQL %(X,u,1,1,1))
        #print(SQL %(X,u,1,1,1))
        #conn.commit()
        #X=X+1
    err=''    
    current_time = datetime.datetime.now() 
    for item in DBF('/mnt/poserver/ics/DAT/INV.DBF',encoding='iso-8859-1'):
        SQL="insert into felino_felino(id,barcode,article,ukuran,list_price,sale_price,index,ondhand,catagory,description) values(%s,'%s','%s','%s',%s,%s,%s,%s,'%s','%s') ON CONFLICT ON CONSTRAINT felino_felino_pkey DO NOTHING;"
    
        list=item['DESC1'].split(" ")
        article= article=item['DESC1'].replace("'"," ")
        index=0;
        ukuran=''
        for lst in list:
            for u in uk :
                if lst==u:
                   print(item['DESC1'])
                   print(list.index(lst))  
                   ukuran=lst
                #print(ukuran)
                   print("-------------------")
                   print(list)
                   index=uk.index(u)
                   list.pop(list.index(lst))
                   print(list)
            article=''
            for ls in list:
                article=article+' '+ls
                print(article)                        
        article=article.replace("'"," ").lstrip()

        ukuran=ukuran.replace("'"," ")       
        try:
           
           cur.execute(SQL %(item['CODE'],item['CODE'],article,ukuran,item['COSTPRC'],item['SELLPRC'],index,item['LQOH'],item['MCLSCODE'],item['DESC1']))
           conn.commit()
        except :
           print("ERROR")
           conn.rollback()   
           print("--------------------ERR")
           print(article)
    f = open("err.log","a")        
    f.write(err)
    print(SQ)
    return 0  

def importAttr():
    engine = create_engine("postgresql://felino:felino@localhost/databaru")
    con = engine.connect() 
    conn = psycopg2.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    SQ=''
    X=0
    uk=['ALL','01','2','3','4','5','O','S','M','L','XL','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']
    for ukuran in uk:
        X=X+1
        SQ="INSERT INTO public.product_attribute_value(id,name,attribute_id) VALUES(%s,'%s',1) ON CONFLICT ON CONSTRAINT product_attribute_value_pkey DO NOTHING;"
        print(SQ %(X,ukuran))   
        cur.execute(SQ %(X,ukuran))
        conn.commit()  
    return 0

def importCat():
    conn = psycopg2.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    cari = conn.cursor()
    SQ="INSERT INTO public.product_category(id,name,complete_name) VALUES(%s,'%s','%s') ON CONFLICT ON CONSTRAINT product_category_pkey DO NOTHING;"
    print(SQ %(1103,'M1A03','LL'))
    cari.execute("SELECT * FROM felino_product_catagory where id!=''")
    for record in cari:
        print(record[0])
        cur.execute(SQ %(record[0],record[1],record[1]))
    conn.commit()    
    return 0
def importVendor():
    conn = psycopg2.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    cari = conn.cursor()
    #cur.execute("DELETE FROM public.res_partner WHERE id>7")
    conn.commit()
    SQ="INSERT INTO public.res_partner(customer,active,company_id,id, name,invoice_warn,picking_warn,display_name,supplier) \
        VALUES (True,True,1,%s,'%s','no-message','no-message','%s',true) ON CONFLICT ON CONSTRAINT res_partner_pkey DO NOTHING;"
    cari.execute("SELECT * FROM felino_vendor") 
    for record in cari:
        cur.execute(SQ %(record[0],record[0],record[0])) 
    conn.commit()       
    return 0

def importSupplier():
    conn = psycopg2.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    cari = conn.cursor()
    for item in DBF('/mnt/poserver/ics/DAT/SUP.DBF',encoding='iso-8859-1'):
        print(item['DESC'],item['CODE'])
        SQ="UPDATE res_partner SET name='%s',display_name='%s',phone='%s' WHERE ID=%s"
         
        cur.execute(SQ %(item['DESC'].replace("'",""),item['DESC'].replace("'",""),item['TELP'],item['CODE'])) 
        conn.commit()
              
    return 0

def importRcv():
    conn = psycopg2.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    cari = conn.cursor()
    cur.execute('delete from felino_receivedetail') 
    conn.commit()
    for item in DBF('/mnt/poserver/ics/DAT/RCV2.DBF',encoding='iso-8859-1'):
        #print(item['DESC'],item['CODE'])
        SQ="insert into felino_receivedetail(id,ponum,podate,barcode,qty) values(%s,%s,'%s','%s',%s) ON CONFLICT ON CONSTRAINT felino_receivedetail_pkey DO NOTHING"
        qty=item['QTY']
        id=item['INVCODE'][-7:]+item['PONUM'][-2:]

        sql=SQ %(id,item['PONUM'],item['PODATE'],item['INVCODE'],item['QTY'])
        print(item['PONUM'][-2:])     
        cur.execute(sql) 
        conn.commit()
    return 0 

importRcv()
#importSupplier()
#importVendor()
#importCat()
#importAttr()
#importInv()