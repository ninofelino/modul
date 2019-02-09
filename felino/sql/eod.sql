update felino_eoddetail set loc=left(name,4)
select name,substr(name,5,4) from felino_eoddetail
select name,substr(name,5,4),to_date(substr(name,5,4)||'2018','MMDDYYYY') from felino_eoddetail

select loc,tgl,sum(sales) as sales from
(
select name
,left(name,4) as loc
,substr(name,5,4)
,to_date(substr(name,5,4)||'2018','MMDDYYYY') as tgl,price*qty as sales from felino_eoddetail
) t
group by 1,2 order by 1