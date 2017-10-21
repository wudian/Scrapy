#!/bin/sh

file_list=`ls /home/wd/db`
mysql -uroot -proot -e""
for file in $file_list
do
    if [[ $file =~ "def" ]]
    then
	db_name=${file%.*}
	sql_path="/home/wd/db/""${file}"
	#echo $db_name
	#echo $sql_path
	mysql -udev -p'dev.0.o-_->>>' -e"create database ${db_name}; source ${sql_path}"
    fi
done
