select replace( replace(logo_url,'background-image: url("',''), '");', '')   from project where length(logo_url)>0;

update project set logo_url = replace( replace(logo_url,'background-image: url("',''), '");', '')    where length(logo_url)>0;

select * from project where length(logo_url)>0 limit 2;

update project p join investment_platform_db5100000_20171009094105.project pnew on p.name=pnew.name set p.logo_url=pnew.logo_url;
update project p join investment_platform_db5000000_20171009093903.project pnew on p.name=pnew.name set p.logo_url=pnew.logo_url;

