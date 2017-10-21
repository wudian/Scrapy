#!/bin/sh

ps auxf | grep python | grep itjuzi_company ;
if [ $? -ne 0 ]  ; then
cd /root/investment_platform_crawler/ ; source shared/bin/set_env.sh ; sh -x start_selenium.sh itjuzi itjuzi_company.py 50
fi