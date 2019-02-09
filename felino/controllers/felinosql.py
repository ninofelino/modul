
class Felinosqll(http.Controller):
      def rekapeod(self, parameter_list):
          sql="""
          select concat('<a href="/felino/analisa/',id,'">',name,'<span class="badge badge-secondary"><small>',count,'</small></span></a>') as name,count from
                (
                select substring(name,5,2) as id,TO_CHAR(to_date(substr(name,5,4)||'2018','MMDDYYYY'),'Mon-YYYY')
                as name,count(*) from felino_pivoteod
             GROUP BY 1,2
             ) t
          """
          return sql