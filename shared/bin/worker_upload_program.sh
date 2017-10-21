#!/bin/sh

script_dir=$1

ip=$(hostname -I | cut -f1 -d' ')
dt=$(date +%Y%m%d%H%M%S)
fn=investment_platform_crawler_${ip}_${dt}.tar.gz
home=/root/
ffn=$home/$fn
tar -czvf  $ffn  $home/investment_platform_crawler*

dropbox_uploader.sh upload $ffn /${script_dir}/pg/$fn
dropbox_uploader.sh list /${script_dir}/pg
