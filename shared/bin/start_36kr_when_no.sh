#!/bin/sh

ps auxf | grep python | grep 36kr ;
if [ $? -ne 0 ]  ; then
cd /root/investment_platform_crawler/ ; source shared/bin/set_env.sh ; sh -x start_selenium.sh rong.36kr.com 36kr.py 50
fi