#!/bin/sh


db=$(mysql -uroot -proot -e"show databases like 'inv%'"  | tail -n 1)
mysqldump  -uroot -proot $db   > $db.sql
