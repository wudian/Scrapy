#!/bin/sh

script_dir=$1
script_name=$2
displayId=$3

script_dir_full=`pwd`/$script_dir

export PYTHONPATH=`pwd`:$script_dir_full

killall Xvfb chromedriver chrome chrome-sandbox
Xvfb :$displayId -ac &
echo $! > $script_dir_full/pid.Xvfb

export DISPLAY=:$displayId

cd $script_dir
echo $displayId>$script_dir_full/displayId
nohup python $script_name  &
echo $! > $script_dir_full/pid.python

