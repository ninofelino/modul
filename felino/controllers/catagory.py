@http.route('/felino/catagory', auth='public')
      def cat(self, **kw):
          http.request.cr.execute('select catagory from felino_felino group by 1  ') 
          data = http.request.cr.fetchall() 
          for record in data:
              str=record[0]
              str1 = ''.join(re.findall('\d+',str.replace('A','5')))
              print(str,str1) 
              SQL="insert into product_category(id,name) values(%s,'%s') ON CONFLICT DO NOTHING"
              try:
                  http.request.cr.execute(SQL %(str1,str))
                  http.request.cr.commit()
              except:
                  http.request.cr.rollback()    
          return "catagory"