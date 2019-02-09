# -*- coding: utf-8 -*-
#import thread6
import base64
import json
import subprocess
import time
import json
from dbfread import DBF
from odoo import http,exceptions
import re
import os
import glob
import csv
import base64
import cgi
import logging
import pandas as pd 
import pandas.io.sql as psql
import psycopg2 as pg
import xml.etree.ElementTree as ET
import locale

#import datetime
# DELETE FROM ir_attachment WHERE url LIKE '/web/content/%';
# UPDATE ir_module_module SET state = 'to remove' WHERE name = 'my_module_to_uninstall' ,
# sudo apt-get install python3-pandas
# 
datalama='/mnt/poserver/ics/DAT/INV.DBF'

def searchbutton():
    htm="""
    <script>
    function showResult(str) {
            $("#result").html(str);
            $.ajax({type:"get",url:"/felino/data/"+str,
            success:function(html){$("#result").html(html).show()}
            })
            }; 
    </script> 
    <input class="form-control" type="text" placeholder="Search" 
    aria-label="Search" onkeyup="showResult(this.value)"/>
       
    <div id="result" style="padding:4px"></div>
        

    """
    return htm

def sql2table(record):
    hasil=''
    hasil='<table id="kiri" class="table">'
    hasil=hasil+'<thead><tr><th>1</th><th>1</th></tr>'
    hasil=hasil+'</thead>'
    hasil=hasil+'<tbody>'
    for rec in record:
        hasil=hasil+'<tr>'
        for fld in rec:
            #print(type(fld),fld)
            #if type(fld)=='str':
            hasil=hasil+'<td>'+str(fld)+'</td>'          
        hasil=hasil+'</tr>'
    hasil=hasil+'</tbody>'    
    return hasil+'</table>'
def sql2datatable(record,headers):
    hasil=''
    hasil='<table id="kiri" class="table">'
    hasil=hasil+'<thead><tr>'
    for headi in headers:
        hasil=hasil+'<th>'+headi+'</th>'
    hasil=hasil+'</thead>'
    hasil=hasil+'<tbody>'
    print("8888888888888888888888888888888888888")
    print(hasil)
    for rec in record:
        hasil=hasil+'<tr>'
        for fld in rec:
            #print(type(fld),fld)
            #if type(fld)=='str':
            hasil=hasil+'<td>'+str(fld)+'</td>'          
        hasil=hasil+'</tr>'
    hasil=hasil+'</tbody>'    
    return hasil+'</table>'
def sidebar(isi):
    hasilnya=''
    for ha in isi:
        hasilnya=hasilnya+'<li>'+ha[0]+'</li>'
    return hasilnya  
def feltree(data):
    isi=''
    isi=isi+'<ul>'
    #isi=isi+'<li>'+data+'</li>'
    for dt in data:
        isi=isi+'<li><a href="/felino/eod">'+dt[0]+'</a></li>'
    isi=isi+'</ul>'
    hasil='<div id="jstree">'+isi+'</div>'
    return hasil  
def sidebar3(isi):
    hasilnya='<div class="btn-group-vertical">'
    for ha in isi:
        hasilnya=hasilnya+'<li width="100px"><a href="'+ha[1]+'" class="dropdown-item" >'+ha[0]+'</a></li>'
    return hasilnya+'</div>'    

def sidemenu():
    menu=[{'<a href="/felino/sales/all">Total Penjualan</a>'},
                {'<a href="/felino/sales/cat">Total Penjualan per Catagory</a>'},
                {'<a href="/felino/sales/all">Total Penjualan per Hari</a>'},
                {'<a href="/felino/sales/all">Total Penjualan per Perbulan</a>'},
          ]
    return menu

def ninofelinosql(semua):
    http.request.cr.execute(semua)
    return http.request.cr.fetchall()




  

def dbf2eod(filepath,obj):
    hasil=[]
    gagal=0
    JML=0
    DQTY=0
    DTTL=0    
    filename=os.path.basename(filepath)
    linking='<a href="/felino/eod/'+filename+'">'+filename+'</a>'
    
    objects= http.request.env['felino.eoddetail'].search([],limit=30)
    for item in DBF(filepath,encoding='iso-8859-1'):
        bisa=['PLU','D%1','RTN','VOD','DS1']
        tampil=False
        if item['FLAG'] in bisa:
           tampil=True
           JML=JML+1
           idx=bisa.index(item['FLAG'])
           if item['FLAG']=='RTN':
              QTY=-1*item['QTY'] 
           elif  item['FLAG']=='D%1':
              QTY=0 
           elif  item['FLAG']=='DS1':
              QTY=0    
           else:
              QTY=item['QTY'] 
           DQTY=DQTY+QTY    
           DTTL=DTTL+(QTY*item['PRICE'])
           product= http.request.env['felino.felino'].search([('barcode','=',item['CODE'])])
           eod={'name':filename,'code':item['CODE'],'barcode':item['CODE'],'desc':item['DESC'],'qty':QTY,'price':item['PRICE'],'norcp':item['NORCP'],'etype':item['ETYPE'],'flag':item['FLAG'],'cprice':item['CPRICE'],'hide':tampil,'category':product['catagory']}
           objects.sudo().create(eod)
           hasil.append(eod)  
    eod={'name':filename,'link':linking,'Child':JML,'Child1':DQTY,'totalsales':DTTL}
    obj.sudo().create(eod)
    return hasil 

def importInv():
    conn = pg.connect("postgresql://felino:felino@localhost/databaru")
    cur = conn.cursor()
    pesanerror=''
    gagal=0
    #cur.execute("delete from felino_felino;")
    SQ=''
    uk=['ALL','01','2','3','4','5','O','S','M','L','XL','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']
    X=0
    print(type(uk))
    err=''    
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
           
           #cur.execute(SQL %(item['CODE'],item['CODE'],article.replace("'"," "),ukuran,item['COSTPRC'],item['SELLPRC'],index,item['LQOH'],item['MCLSCODE'],item['DESC1'].replace("'"," ")))
           #conn.commit()
           http.request.cr.execute((SQL %(item['CODE'],item['CODE'],article.replace("'"," "),ukuran,item['COSTPRC'],item['SELLPRC'],index,item['LQOH'],item['MCLSCODE'],item['DESC1'].replace("'"," "))))
           http.request.cr.commit()       
        except :
           print("ERROR")
           conn.rollback()   
           print("--------------------ERR--------------------------------")
           print(article)
           pesanerror=pesanerror+':'+item['CODE']+':'+item['DESC1']
           gagal=gagal+1
    f = open("err.log","a")        
    f.write(err)
    print(pesanerror)
    return str(gagal)+pesanerror

class Felino(http.Controller):
      
              
      @http.route('/felino/', auth='public',website=True,type='http')
      def index(self, **kw):
          #objects= http.request.env['felino.felino'].search([],limit=30)
          data=[]
          data.append(['<b>Daftar Product</b>','/felino/inv'])
          data.append(['Daftar Product Per Mclass','/felino/inv'])
          data.append(['<b>Data Penjualan</b>','/felino/inv'])
          data.append(['Rekapan EOD PerBulan','/felino/analisa'])
          data.append(['Rekapan EOD/Mclass PerBulan','/felino/analisa/mclass'])
          data.append(['EOD (dari toko)','/felino/eod'])
          data.append(['Log Penjualan','/felino/sales'])
         
          data.append(['<div class="oe_secondary_menu_section">Master Data</div>','/felino'])
          data.append(['Product','/felino'])
          data.append(['Product Per Mclass','/felino/inv/cat/123'])
          data.append(['Vendor ','/felino/vendor'])
          data.append(['Mclass ','/felino/mclass'])
          data.append(['Custumer','/felino/customer'])
          data.append(['Store   ','/felino/store'])
          data.append(['Penerimaan Barang per supplier','/felino/receive'])
          data.append(['Penerimaan Barang per hari','/felino/receive/day'])
          data.append(['ss','/web#id=90400178&view_type=form&model=product.template&menu_id=195&action=293'])
          data.append(['Debug   ','/felino/felino'])
          return http.request.render('felino.gateway',{"kanan":searchbutton(),"kiri":sidebar3(data)})

      @http.route(['/felino/felino','/felino/felino/<imprt>'], auth='public',website=True,type='http')
      def felinotools(self,imprt=None, **kw):
          data=[]
          judul="Debugger"
          data.append(['<b>Import Data Dari Inv Dbf</b>','/felino/felino/invdbf'])
          data.append(['<b>Dbf Ke Odoo</b>','/felino/felino/template']) 
          data.append(['<b>Import Data Vendor</b>','/felino/felino/invdbf'])
          data.append(['<b>Import Data Customer</b>','/felino/felino/invdbf'])
          data.append(['<b>Import Data Category</b>','/felino/felino/invdbf'])
          data.append(['<b>Data Logger</b>','/felino/felino/invdbf'])
          data.append(['<b>Upload EOD</b>','/felino/eod/upload'])     
          #print(feltree(data))    
          if not imprt is None:
             judul=importInv() 
          return http.request.render('felino.gateway',{"kanan":sidebar3(data),"kiri":feltree(data),'judul':judul})

      @http.route('/felino/quick/<search>', auth='public',website=True,type='http')
      def felino(self, **kw):
          data=[]
          data.append(['<b>Import Data Dari Inv Dbf</b>','/felino/felino/invdbf'])
          data.append(['<b>Dbf Ke Odoo</b>','/felino/felino/invdbf']) 
          data.append(['<b>Import Data Vendor</b>','/felino/felino/invdbf'])
          data.append(['<b>Import Data Customer</b>','/felino/felino/invdbf'])
          data.append(['<b>Import Data Category</b>','/felino/felino/invdbf'])
          data.append(['<b>Data Logger</b>','/felino/felino/invdbf'])         
          return http.request.render('felino.gateway',{"kiri":sidebar3(data)})    
  
      @http.route('/felino/analisa', auth='public',website=True,type='http')
      def felino(self, **kw):
          #data = pd.read_csv("/home/master/addons/felino/controllers/sales.csv",sep=';')        
          http.request.cr.execute("select name,store,to_date(substr(name,5,4)||'2018','MMDDYYYY') as date_in,total as ttl from felino_pivoteod ")
          tupleFromCursor = http.request.cr.fetchall()
          sql="""
             select concat('<a href="/felino/analisa/',id,'">',name,'<span class="badge badge-secondary"><small>',count,'</small></span></a>') as name,count from
                (
                select substring(name,5,2) as id,TO_CHAR(to_date(substr(name,5,4)||'2018','MMDDYYYY'),'Mon-YYYY')
                as name,count(*) from felino_pivoteod
             GROUP BY 1,2
             ) t
          """
          http.request.cr.execute(sql)
          kiri=http.request.cr.fetchall()
          my_DF = pd.DataFrame(data=list(tupleFromCursor), columns=('name','store','date_in','ttl')).pivot_table(index='store',columns='date_in')
          return http.request.render('felino.gateway',{'kiri':sidebar(kiri),'kanan':my_DF.to_html(classes='table table-stripped')})

            
      
            
      @http.route('/felino/sales',  website=True,type='http',auth='public')
      def gatew(self, **kw):
          semua="""
             select * from
             (
             select left(name,4)  as store ,to_date(substr(name,5,4)||'2018','MMDDYYYY') AS Date
             ,totalsales from felino_eodmaster
             ) t order by 2,1 
             """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
          menu=[{'<a href="/felino/salesall">Total Penjualan</a>'},
                {'<a>Total Penjualan per Catagory</a>'},
                {'<a>Total Penjualan per Hari</a>'},
                {'<a>Total Penjualan per Perbulan</a>'},
          ]     
          return http.request.render('felino.gateway',{"kiri":sql2table(menu),"kanan":sql2datatable(data,('11','22','23'))})

      @http.route('/felino/sales/all',  website=True,type='http',auth='public')
      def gatewalls(self, **kw):
          semua="""
             select * from
             (
             select left(name,4)  as store ,to_date(substr(name,5,4)||'2018','MMDDYYYY') AS Date
             ,totalsales from felino_eodmaster
             ) t order by 2,1 
             """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
      @http.route('/felino/sales',  website=True,type='http',auth='public')
      def gatew(self, **kw):
          semua="""
             select * from
             (
             select left(name,4)  as store ,to_date(substr(name,5,4)||'2018','MMDDYYYY') AS Date
             ,totalsales from felino_eodmaster
             ) t order by 2,1 
             """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
          menu=[{'<a href="/felino/salesall">Total Penjualan</a>'},
                {'<a>Total Penjualan per Catagory</a>'},
                {'<a>Total Penjualan per Hari</a>'},
                {'<a>Total Penjualan per Perbulan</a>'},
          ]     
          return http.request.render('felino.gateway',{"kiri":sql2table(menu),"kanan":sql2table(data)})

      @http.route(['/felino/vendor'],  website=True,type='http',auth='public')
      def salesvendor(self, **kw):
          judul='data vendor beserta jumlah product'
          semua="""
              select id,name,phone,concat('</a>',product,'</a>') as product from
              (
              select id,left(name,10) as name,phone,(select count(*) from product_template where left(default_code,3)::int=a.id) as product from res_partner a
              where a.supplier=True
              ) t 
                """
          data = ninofelinosql(semua)
          return http.request.render('felino.gateway',{"judul":judul,"kanan":sql2datatable(data,('1.Code','2.Nama','Telp','Product'))})    
   
      @http.route('/felino/store',  website=True,type='http',auth='public')
      def salesstore(self, **kw):
          judul='rekapan data eod perbulan'
          semua="""
                select id,name,code,
                (select count(*) from felino_eoddetail where left(name,4)=t.code and substr(name,5,2)='01') as jan,
                (select count(*) from felino_eoddetail where left(name,4)=t.code and substr(name,5,2)='02') as feb,
                (select count(*) from felino_eoddetail where left(name,4)=t.code and substr(name,5,2)='03') as mar,
                (select count(*) from felino_eoddetail where left(name,4)=t.code and substr(name,5,2)='04') as apr
                
                from 
                (select id,name,code from stock_warehouse) t 
                """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
          return http.request.render('felino.gateway',{"judul":judul,"kanan":sql2datatable(data,('id','Name','code','Jan','feb','mar','appr'))})    
     
      @http.route('/felino/receive',  website=True,type='http',auth='public')
      def salesreceive(self, **kw):
          objects= http.request.env['felino.receive'].search([],limit=30)
          obj= http.request.env['felino.receivedetail'].search([],limit=30)
          judul='Penerimaan Barang'
          semua="""
                select display_name,sum(qty) as terima from
                (select podate,ponum,(select display_name from res_partner where id=left(t.barcode,3)::int),id,barcode,qty,(select name from felino_felino where barcode=t.barcode) from felino_receivedetail t
                ) x group by 1  
                """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
          return http.request.render('felino.gateway',{"judul":judul,"kanan":sql2datatable(data,('Name','Qty'))})
   
      
      @http.route(['/felino/receive/day/<day>','/felino/receive/day'],website=True,type='http',auth='public')
      def salesreceiveday(self,day=None,**kw):
          judul='Penerimaan Barang perhari'
          kiri=sidebar(ninofelinosql("""
          select concat('<a href="/felino/receive/day/',podate,'">',podate,'<span class="badge badge-light">',sum,'</span><a>') from felino_receive_byday
          """))
          para="where podate='"+day+"'"
          sq="select * from felino_receive_byday_detail "
          if not day is None:
             sq=sq+para  
             kanan=sql2datatable(ninofelinosql(sq),('Vendor','Date','1','Barcode','QTY','1','1','1','1'))
          return http.request.render('felino.gateway',{"judul":judul,"kiri":kiri,"kanan":kanan})


      @http.route('/felino/mclass',  website=True,type='http',auth='public')
      def salesmclass(self, **kw):
          semua="""
                select id,name,complete_name,parent_id from product_category
                """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
          return http.request.render('felino.gateway',{"kanan":sql2datatable(data,('id','Code','Name','Parent'))})  

      @http.route('/felino/sales/cat',  website=True,type='http',auth='public')
      def gatewall(self, **kw):
          semua="""
             select * from felino_eoddetail limit 100
             
             """
          http.request.cr.execute(semua)
          data = http.request.cr.fetchall()
              
          return http.request.render('felino.gateway',{"kiri":sql2table(sidemenu()),"kanan":sql2table(data)})
         

      @http.route('/felino/data/<cari>', auth='public')
      def invdbfcari(self,cari=None,**kw):
          products= http.request.env['product.template'].search([('name','like',cari)],limit=30)
          root = ET.Element('table')
          root.attrib['class']="table table-striped"
          for rec in products:
              baris = ET.SubElement(root, "tr")
              id = ET.SubElement(baris, "td")
              id.text=rec.name
              id.attrib['width']="60%"
             # ids = ET.SubElement(baris, "a")
             # ids.attrib['href']="/felino/data/link/"
             # ids.text=rec.name
              id = ET.SubElement(baris, "td")
              #id.attrib['class']="table"
              id.text=str(rec.id)
              id = ET.SubElement(baris, "td")
              id.attrib['align']="right"
              id.text="{0:,.0f}".format(rec.list_price)

          return ET.tostring(root)

      @http.route('/felino/image', auth='public')
      def imgdbfcari(self,cari=None,**kw):
          data=ninofelinosql("select db_datas from ir_attachment where id=760")
          for rec in data:
              print(str(rec[0]))
              open('/var/tmp/gb.jpg','wb').write(str(rec[0]))
          return rec[0]    

      @http.route('/felino/product', auth='public')
      def inv(self, **kw):
          #http.request.cr.execute('delete from product_product;delete from product_template;')
          #http.request.cr.execute('select * from felino_dbinv order by idx ') 
          data = http.request.cr.fetchall() 
          objects= http.request.env['product.template']
          attr_test= http.request.env['product.attribute'].browse([389])
          print(attr_test.value_ids.ids)
          for record in data:
              px=[]
              attx=[]
              print(record[6])
              attx=record[6]
              #attx=record[5]
              for data in record[5]:
                  px.append((0,0,data))
                  #px.append([0,0,data])
              
              print("------------------------------")
              print(attx)
              print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

              productlist = {'id':record[0],'name':record[1],'list_price':record[3],'standard_price':record[2],
              'product_variant_ids':px,          
              #'attribute_line_ids': [(0, 0, {'attribute_id': 1,'value_ids':[(6, 0,attx)],}),
              'attribute_line_ids': [(0, 0, {'attribute_id': 1,'value_ids':[(4,0,attx)],}),
              
              ] ,
              
              #attribute_value_ids,
              #'qty_availab
              } 
              #try:
              objects.sudo().create(productlist)
              http.request.cr.commit()
             
              
          return http.request.render('felino.listing')  


     

      @http.route('/felino/info', auth='public')
      def testifo(self, **kw):
          #objects= http.request.env['felino.inv']
          http.request.cr.execute("select concat('<a href=products/',vendor,'>',vendor,'</a>'),concat('<span class=""badge badge-secondary"">',jml,'</span>'),jml from felino_suppliers order by 3 desc limit 10")    
          #datas = http.request.env['product.template'].sudo().search([],limit=20) 
          #print(datas)
          datas = http.request.cr.fetchall() 
          http.request.cr.execute("select name,list_price from product_template where left(default_code,3)='026'")
          products= http.request.cr.fetchall() 
          print(type(datas))
          print("kkkkkkkkkkkkkkkkkkkkkkkkkkk")
          print(type(datas))
          return http.request.render('felino.inv',{'datas':datas,'products':products})   
                     
    
# ------------------------------------------ EOD -------------
      @http.route('/felino/uploadfile',type='http',auth='public',methods=['GET', 'POST'],website=True, csrf=False)
      def image_handle(self, **post): 
        fname= post.get('attachment').filename
        files = post.get('attachment').stream.read()
        filename='/var/tmp/'+fname
        fp =open(filename,'wb')        
        fp.write(files)        
        fp.close()        
        objeod= http.request.env['felino.eodmaster']
        dbf2eod(filename,objeod)
        return http.request.redirect('/felino/eod/'+fname)       
     
      @http.route(['/felino/eod/<soday>','/felino/eod'],type='http',auth='public',website=True)
      def eodsearch(self,soday=None, **kw): 
          filenames= http.request.env['felino.eodmaster'].sudo().search([]) 
          detail= http.request.env['felino.eoddetail'].sudo().search([("name","=",soday)]) 
          #detail.filtered('hide'==True)
          return http.request.render('felino.byeod',{'fnames':filenames,'detail':detail})  

      @http.route('/felino/eod/upload', auth='public',type='http',website=True)
      def eodupload(self, **kw):
          fnames=glob.glob('/mnt/poserver/SALES/*.DBF')
          http.request.cr.execute("delete from felino_eoddetail;SELECT setval('felino_eoddetail_id_seq', 1, FALSE);")
          http.request.cr.execute("delete from felino_eodmaster;SELECT setval('felino_eodmaster_id_seq', 1, FALSE);")
          http.request.cr.commit()
          objeod= http.request.env['felino.eodmaster']
          for filepath in fnames:
              isi=dbf2eod(filepath,objeod)
              print(isi)       
          return http.request.redirect('/felino/eod')

      @http.route('/felino/pgproduct', auth='public',website=True,type='http')
      def invpro(self, **kw):
          http.request.cr.execute('select * from felino_dbinv')
          data = http.request.cr.fetchall() 
          
          return http.request.render('felino.gateway',{'kanan':data}) 

        
# ****************************************  EOD *******************
# === INV
      @http.route('/felino/inv', auth='public',type='http',website=True)
      def invdbflama(self, **kw):
          filenames= http.request.env['felino.eodmaster'].sudo().search([]) 
          http.request.cr.execute('''
          select concat('<a href="/felino/inv/cat/',t.categ_id,'">',(select name from product_category where id=t.categ_id),'<span class="badge badge-warning">',count,'</span>','</a>')
          from
              (select categ_id,count(*) from product_template group by 1) t
          order by 1
          ''')


          data = http.request.cr.fetchall() 
          detail= http.request.env['felino.felino'].sudo().search([]) 

          return http.request.render('felino.search',{'kiri':data,'detail':detail}) 
    
      @http.route('/felino/inv/cat/<cat>',type='http',auth='public',website=True)
      def invdbfbycat(self,cat=None, **kw):
          http.request.cr.execute('select * from felino_product_template_catagory')
          data = http.request.cr.fetchall() 
          judul="Data Product Per Category"
          #detail= http.request.env['felino.felino'].sudo().search([('catagory','=',cat)]) 
          SQL="""
          select
         (select name  from res_partner where id=left(default_code,3)::int limit 1) as vendor
         ,left(default_code,3)
         ,id,default_code
         ,name
         ,list_price
         ,active from product_template where categ_id=%s
          order by 2,5
          """
          http.request.cr.execute(SQL %(cat))
          product=http.request.cr.fetchall() 
          return http.request.render('felino.gateway',{'judul':judul,'kiri':sidebar(data),'kanan':sql2datatable(product,['Vendor','Vcode','Barcode','Barcode','Article','ListPrice','Active'])}) 
   
      @http.route('/felino/inv/vendor/<cat>',type='http',auth='public',website=True)
      def invdbfbyvendor(self,cat=None, **kw):
          http.request.cr.execute('select txt from felino_product_vendor order by jm desc')
          data = http.request.cr.fetchall() 
          SQL="""
          select name,list_price from product_template where left(default_code,3)='%s'
          order by 1
          """
          http.request.cr.execute(SQL %(cat))
          product=http.request.cr.fetchall() 
          judul="Daftar Product per vendor"
          return http.request.render('felino.gateway',{'kiri':sidebar(data),'kanan':sql2table(product),'judul':judul}) 

      @http.route('/felino/sales/<cat>',type='http',auth='public',website=True)
      def salesbyvendor(self,cat=None, **kw):
          http.request.cr.execute('select concat(name) from felino_sales_top')
          data = http.request.cr.fetchall() 
          #detail= http.request.env['felino.felino'].sudo().search([('catagory','=',cat)]) 
          SQL="""
          select * from felino_eoddetail where left(barcode,3)='%s'
          """
          http.request.cr.execute(SQL %(cat))
          product=http.request.cr.fetchall() 
         
          return http.request.render('felino.gateway',{'kiri':data,'kanan':sql2table(product)})     
         
# === INV

      @http.route('/felino/template', auth='public')
      def invsupload(self, **kw):
          #http.request.cr.execute('delete from product_product;delete from product_template;DELETE FROM product_attribute_line')
          #http.request.cr.execute('select * from felino_dbinv order by idx ') 
          print("-startrrrrrrrrrrrrrrrrrrrrrrrrrr") 
          data = http.request.cr.fetchall() 
          objects= http.request.env['product.template']
          attr_test= http.request.env['product.attribute'].browse([1])
          # INSERT INTO public.product_attribute(
          # id, name, sequence, create_variant, create_uid, create_date, 
          # write_uid, write_date)
          print(attr_test.value_ids.ids)
          for record in data:
              catid=record[9]
              if record[9] is None:
                 catid=0
                 
              print("------------------------------")
              print(record[9],record[1])
              print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
              if record[9] is None:
                 nilai=1
              else:
                 nilai=record[9]  
              SQL="insert into product_template(tracking,responsible_id,id,name,sequence,type,rental,list_price,sale_ok,purchase_ok,uom_id,uom_po_id,company_id,active,default_code,create_uid,write_uid,available_in_pos,create_date,categ_id)\
               values('none',1,%s,'%s',1,'consu',FALSE,%s,TRUE,TRUE,1,1,1,TRUE,'%s',1,1,TRUE,now(),%s) ON CONFLICT ON CONSTRAINT product_template_pkey DO NOTHING"
              print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
              print(SQL %(record[0],record[1],record[3],record[0],nilai))
              http.request.cr.execute(SQL %(record[0],record[1],record[3],record[0],nilai))
              http.request.cr.commit()
              SQL="insert into product_attribute_line(product_tmpl_id,attribute_id) values(\
                  %s,%s) ON CONFLICT DO NOTHING"
              http.request.cr.execute(SQL %(record[0],1) )
              http.request.cr.commit() 
              ls=record[5]
              print(type(ls))
              for isi in ls:
                  print(isi['default_code'])
                  SQL="insert into product_product(id,product_tmpl_id,default_code,active,create_uid,write_uid)\
                  values(%s,%s,'%s',TRUE,1,1) ON CONFLICT DO NOTHING"
                  print(SQL %(int(isi['default_code']),record[0],isi['default_code']))
                  http.request.cr.execute(SQL %(isi['default_code'],record[0],isi['default_code']) )
                  print("----------------kkkk")
                  print(id)
                  http.request.cr.commit()
                  SQL="insert into product_attribute_value_product_product_rel(product_product_id, product_attribute_value_id)\
                  values(%s,%s)"
                  try:
                      http.request.cr.execute(SQL %(isi['default_code'],isi['attribute_value_ids']) )
                  
                      http.request.cr.commit()
                  except:
                      http.request.cr.rollback() 
                  
              
              
          return http.request.render('felino.listing')  
      

def threaded_print(objects):
    product=http.request.env['product.template']
    print("mulai") 
    for item in DBF('/mnt/poserver/ics/DAT/INV.DBF',encoding='iso-8859-1'):
              list=item['DESC1'].split(" ")
              print("start")
              SQL='INSERT INTO felino_felino (barcode,article,name) VALUES (%s,%s,%s) ON CONFLICT ON CONSTRAINT felino_felino_pkey DO NOTHING; '
              #,{"barcode":item['CODE'],"article":article,"ukuran":ukuran}))
              if len(list)>2:
                 ukuran=list[len(list)-1][-2:]
                 article=list[0]+' '+list[1]
                 name=article
                 id=barcode
                 cost=item['COSTPRC']
                 saleprice=item['SELLPRC']
                 barcode=item['CODE']
                 #product.sudo().write({'product_id':item['CODE'],'name':article,'default_code':barcode,'list_price':cost,'lst_price':saleprice,'attribute_line_ids':[{'id':3}]})
                 print(SQL,(barcode,article,name,))
                 http.request.cr.execute(SQL,(barcode,article,name,))
                 http.request.cr.commit()
    return 1
    


def threaded_inv(objects):
    #mulai=time()
    #objects= http.request.env['felino.felino'].search([],limit=30)
    for item in DBF(datalama,encoding='iso-8859-1'):
              list=item['DESC1'].split(" ")
              print(item['DESC1'])
              
              try:
                 ukuran=list[len(list)-1][-2:]
                 article=list[0]+' '+list[1]
                 barcode=item['CODE']
                 cost=item['COSTPRC']
                 saleprice=item['SELLPRC']
                 objects.sudo().create({'id':barcode,'name':article,'article':article,'barcode':barcode,'ukuran':ukuran,'sale_price':saleprice,'list_price':cost})
                 http.request.cr.commit()
              except:
                 print("error")     
   
    return 1  


