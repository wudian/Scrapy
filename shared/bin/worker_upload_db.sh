#!/bin/sh

script_dir=$1

ip=$(hostname -I | cut -f1 -d' ')
db=$(mysql -uroot -proot -e"show databases like 'inv%'"  | tail -n 1)  ;
dt=$(date +%Y%m%d%H%M%S)
mysqldump --no-data  -uroot -proot $db   > $db.mysqldefsql
mysqldump --no-create-info  -uroot -proot $db   > $db.mysqldatasql
sleep 1
dropbox_uploader.sh upload $db.mysqldatasql /${script_dir}/db/${db}_${ip}_${dt}.mysqldatasql
sleep 1
dropbox_uploader.sh upload $db.mysqldefsql /${script_dir}/db/${db}_${ip}_${dt}.mysqldefsql
dropbox_uploader.sh list /${script_dir}/db
