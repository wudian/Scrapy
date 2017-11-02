
delete from {{from_db}}.project where name in (select name from {{to_db}}.project);
delete from  {{from_db}}.financing_phase where project_id not in (select id from {{from_db}}.project);
delete from  {{from_db}}.company_member where project_id not in (select id from {{from_db}}.project);


insert into {{to_db}}.project(id, logo_url, name, introduction, product_description, industry, city, financing_phase, company_name, start_date, site, investment_platform)
 select id, logo_url, name, introduction, product_description, industry, city, financing_phase, company_name, start_date, site, investment_platform
 from {{from_db}}.project;

insert into {{to_db}}.financing_phase(id, phase,amount,investor,date, project_id, investment_platform)
select id, phase,amount,investor,date, project_id, investment_platform
from {{from_db}}.financing_phase;


insert into {{to_db}}.company_member(id, name, position, experience, project_id, investment_platform)
select id, name, position, experience, project_id, investment_platform
 from {{from_db}}.company_member;

