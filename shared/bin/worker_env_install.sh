#!/usr/bin/env bash

h=~/work_home
bin=$h/bin
mkdir $h ; mkdir $bin; cd $h

rm -fr ./chromedriver_linux64.zip; wget -N https://chromedriver.storage.googleapis.com/2.30/chromedriver_linux64.zip  -O  ./chromedriver_linux64.zip
rm -fr /usr/bin/chromedriver; unzip chromedriver_linux64.zip -d /usr/bin/


python --version
#2.7


yum install -y  python2-pip  xorg-x11-server-Xvfb xorg-x11-server-Xephyr killall htop  google-noto-sans-simplified-chinese-fonts
pip install selenium sqlalchemy pymysql pycurl flask dmidecode bypy pyvirtualdisplay

echo """
[google64]
name=Google - x86_64
baseurl=http://dl.google.com/linux/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
""" > /etc/yum.repos.d/google64.repo
yum install google-chrome-stable -y


echo """
[mariadb]
name = MariaDB
baseurl = http://yum.mariadb.org/10.1/centos7-amd64
gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB
gpgcheck=1
""" > /etc/yum.repos.d/mariadb.repo
yum install -y MariaDB-server MariaDB-client
systemctl enable mariadb ; systemctl start mariadb
mysql -uroot -e"grant all privileges on *.* to root@'localhost' identified by 'root'";

wget -N https://raw.github.com/andreafabrizi/Dropbox-Uploader/master/dropbox_uploader.sh    -O  /usr/bin/dropbox_uploader.sh
chmod +x /usr/bin/dropbox_uploader.sh 



wget -N "https://docs.google.com/uc?id=0B3X9GlR6EmbnQ0FtZmJJUXEyRTA&export=download"  -O /usr/bin/gdrive ; chmod +x /usr/bin/gdrive