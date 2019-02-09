# -*- coding: utf-8 -*-
import os
from odoo import models, fields, api
class felino(models.Model):
     _name = 'felino.felino'
     name = fields.Char()
     locasi  = fields.Char()
     tanggal = fields.Char()
     barcode = fields.Char()
     catagory = fields.Char()
     article = fields.Char()
     ukuran  = fields.Char()
     index  = fields.Integer()
     ondhand  = fields.Integer()
     sale_price = fields.Char()
     list_price = fields.Char()
     description = fields.Text()

class eod(models.Model):
      _name ='felino.eoddetail'
      name =fields.Char()
      flag =fields.Char()
      loc  =fields.Char()
      barcode =fields.Char()
      code =fields.Char()
      desc =fields.Char()
      qty =fields.Integer()
      price =fields.Integer()
      cprice =fields.Integer()
      norcp =fields.Char()
      etype =fields.Char()
      ddate =fields.Char()
      dept =fields.Char()
      group =fields.Char() 
      sales =fields.Char()
      point =fields.Char() 
      path =fields.Char() 
      category =fields.Char() 
      hide =fields.Boolean() 
      catagory=fields.Many2one('felino.felino',string="barcode",store=False)
 
class eod(models.Model):
      _name ='felino.eoday'
      name =fields.Char()
      flag =fields.Char()
      code =fields.Char()
      desc =fields.Char()
      qty =fields.Integer()
      price =fields.Integer()
      cprice =fields.Integer()
      norcp =fields.Char()
      etype =fields.Char()
      ddate =fields.Char()
      dept =fields.Char()
      group =fields.Char() 
      sales =fields.Char()
      point =fields.Char() 

class eod(models.Model):
      _name ='felino.eod'
      name =fields.Char()
      flag =fields.Char()
      code =fields.Char()
      desc =fields.Char()
      qty =fields.Integer()
      price =fields.Integer()
      cprice =fields.Integer()
      norcp =fields.Char()
      etype =fields.Char()
      ddate =fields.Char()
      dept =fields.Char()
      group =fields.Char() 
      sales =fields.Char()
      point =fields.Char() 

class rcv(models.Model):
      _name ='felino.receive'
      name =fields.Char()
      ponum =fields.Char()
      podate =fields.Date()
      total =fields.Integer()
      receive =fields.Integer()
      supplier =fields.Integer()

class rcvdetail(models.Model):
      _name ='felino.receivedetail'
      name =fields.Char()
      ponum =fields.Char()
      barcode =fields.Char()
      podate =fields.Date()
      qty =fields.Integer()
      price =fields.Integer()
      supplier =fields.Integer()      
          

class eoderror(models.Model):
      _name ='felino.error'
      desc =fields.Char() 


#class productentry(models.Model):
      #_name ='felino.productentry'
      #_inherit =['product.template']
      #vendor =fields.Integer()


class catagoryeod(models.Model):
      _name ='felino.catagory'
      @api.model_cr
      def init(self):
          self._cr.execute("""
          CREATE OR REPLACE VIEW public.felinocatagory AS 
 SELECT concat('<a href="/felino/inv/cat/',felino_felino.catagory,'">', felino_felino.catagory, '<span class="badge badge-secondary">', count(*), '</span></a>') AS dt
   FROM felino_felino
  GROUP BY felino_felino.catagory;

ALTER TABLE public.felinocatagory
  OWNER TO postgres;


          """)


class eodmaster(models.Model):
      _name ='felino.eodmaster'
      name   =fields.Char()
      #detail =fields.One2many('felino.eoddetail','name','Detail Eod')
      path   =fields.Char()
      link   =fields.Char()
      linkexport   =fields.Char()
      Child  =fields.Integer()
      Child1 =fields.Integer()
      Child2 =fields.Integer()
      totalsales=fields.Integer()
      totalcost=fields.Integer()
      datas  =fields.Binary() 
      
      totali =fields.Char(string='totali',compute='_compute_total',store=False)
      #filename =fields.Char()
      @api.one
      def _compute_total(self):
          i=0 
          filename=os.path.basename(self.name) 
          for x in self.detail:
              print(x.flag)
              i=i+1
          print(i)    
          self.totali='<a href="/felino/eod/'+filename+'">'+filename+'</a>'
      @api.multi
      def generate_printer(self):
          tpl = self.env['mail.template'].search(['name','=','dotmatrix'])
          data = tpl.render_template(tpl.body_html,'felino.felino',self.id,post_process=False)
          self.printer_data=data

#@api.depends()
#def _compute_total():
#    record.total = 0
              