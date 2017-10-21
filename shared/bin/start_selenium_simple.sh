#!/bin/sh

script_dir=$1
script_name=$1


ps auxf | grep python | grep $script_name;
if [ $? -e 0 ]  ; then
echo "existed process,exit..."
exit 1
fi

script_dir_full=`pwd`/$script_dir

export PYTHONPATH=`pwd`:$script_dir_full

killall Xvfb chromedriver chrome chrome-sandbox

cd $script_dir
nohup python $script_name  &
echo $! > $script_dir_full/pid.python

