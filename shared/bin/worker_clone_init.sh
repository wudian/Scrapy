#!/bin/sh

swapoff -a

branch=$1

echo $0 $1

#clone init:
cd ~; rm -fr investment_platform_crawler
yum install git -y
git config --global credential.helper "cache --timeout=360000000"
git clone https://programdev:pi=3.1415@gitee.com/zaaaaaaaa/investment_platform_crawler.git
cd investment_platform_crawler; git checkout -- .; git checkout ${branch}
git clone https://programdev:pi=3.1415@gitee.com/zaaaaaaaa/investment_platform_crawler_shared.git shared
cd shared; git checkout ${branch}; cd ..
sleep 1

#drop database
db=$(mysql -uroot -proot -e"show databases like 'inv%'"  | tail -n 1)
mysql -uroot -proot -e"drop database ${db}"
#create database def
cd ~/investment_platform_crawler; export PYTHONPATH=`pwd`;    python  itjuzi/worker_init_db.py
db=$(mysql -uroot -proot -e"show databases like 'inv%'"  | tail -n 1)
mysql -uroot -proot -e"show databases; show tables from  ${db}; select count(*) from ${db}.project"
