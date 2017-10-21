#!/bin/sh

script_dir=$1
script_name=$2

script_dir_full=`pwd`/$script_dir

kill -s TERM `cat $script_dir_full/pid.Xvfb`
kill -s TERM `cat $script_dir_full/pid.python`
