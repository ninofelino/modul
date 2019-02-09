select min(barcode) as ID,name,list_price,sale_price,count(*),json_agg(json_build_object('barcode',barcode,'attr',ukuran)) as barcode_size
from
(select name,list_price,sale_price,barcode,ukuran

from felino_felino order by barcode) t
group by 2,3,4