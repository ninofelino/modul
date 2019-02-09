select * from
(
select left(name,4)  as store ,to_date(substr(name,5,4)||'2018','MMDDYYYY') AS Date
,"Child" from felino_eodmaster
) t order by 2,1