��װ���������
rpm -Uvh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y epel-release zlib-devel bzip2-devel pcre-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel mysql mysql-server mysql-devel
yum groupinstall -y 'Development tools'
yum install -y nginx

��װSVN�ͻ���
��
ע��smops��ҵ����������Ҫ��װsvn

�༭��װPython3.5
mkdir /root/src/
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz -P /root/src/
cd /root/src/
tar zxvf Python-3.5.2.tgz
cd /root/src/Python-3.5.2
mkdir /usr/local/python3.5.2
./configure --prefix=/usr/local/python3.5.2/
make && make install

��װeasy_install(�Ǳ���)
wget https://pypi.python.org/packages/5f/ad/1fde06877a8d7d5c9b60eff7de2d452f639916ae1d48f0b8f97bf97e570a/distribute-0.7.3.zip -P /root/src/
unzip distribute-0.7.3.zip
cd distribute-0.7.3
/usr/local/python3.5.2/bin/python3 setup.py install

��װpip(����)
wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz -P /root/src/
cd /root/src/
tar zxvf pip-8.1.2.tar.gz
cd pip-8.1.2
/usr/local/python3.5.2/bin/python3 ./setup.py install

��װvirtualenv���⻷��������
/usr/local/python3.5.2/bin/pip install virtualenvwrapper

��װuwsgi
/usr/local/python3.5.2/bin /pip install uwsgi

�����������л����������⻷���а�װuwsgi
/usr/local/python3.5.2/bin/virtualenv /data/www/smops_env/
/data/www/smops_env/bin/pip install uwsgi
/data/www/smops_env/bin/pip install virtualenv

����uwsgi�����ļ�
cat <<\EOF > /etc/uwsgi9000.ini
[uwsgi]
socket = 127.0.0.1:9000
master = true
vhost = true
workers = 2
reload-mercy = 10
vacuum = true
max-requests = 1000
limit-as = 512
buffer-size = 30000
profiler = true
logdate=true
pythonpath = /data/www/smops/
chdir = /data/www/smops/
virtualenv =  /data/www/smops_env/
pidfile = /var/run/uwsgi9000.pid
daemonize = /var/log/uwsgi/uwsgi9000.log
EOF

mkdir /var/log/uwsgi/

�޸�nginx�����ļ�
cat /etc/nginx/conf.d/default.conf
server {
        listen       80;
        server_name  localhost;
        access_log /var/log/nginx/smops_access.log main;
        error_log /var/log/nginx/smops_error.log;

        location /static {
            #root /data/www/smops/templates/themes/AdminLTE;
            alias /data/www/smops/templates/themes/AdminLTE;
        }

        location / {
            include  uwsgi_params;
            uwsgi_pass  127.0.0.1:9000;
            uwsgi_param UWSGI_SCRIPT smops.wsgi;
            uwsgi_param UWSGI_CHDIR /data/www/smops/;
            index  index.html index.htm;
            client_max_body_size 35m;
        }
}

��smops��Ŀ�ϴ���/data/www/Ŀ¼�²��������ݿ�
chkconfig mysqld on
service mysqld start
/data/www/smops_env/bin/pip install -r /data/www/smops/requirements.txt
mysql -uroot -p --default-character-set=utf8 smops < /data/www/smopsv7.sql
mkdir /var/log/uwsgi

�޸����ݿ�����
��ʵ������޸�/data/www/smops/smops/settings.py���������ݿ�����
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smops',
        'USER': 'root',
        'PASSWORD': 'abc.123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

��������
iptables -F
echo "nohup /data/www/smops_env/bin/uwsgi --ini /etc/uwsgi9000.ini" >> /etc/rc.local

�޸���Ŀ����
vim /data/www/smops/smops/settings.py
DEBUG = False
ALLOWED_HOSTS = ['*']
STATIC_ROOT = '/data/www/smops/templates/themes/AdminLTE/'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': smops,
        'USER': 'root',
        'PASSWORD': 'abc.123',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

������Ŀ
nohup /data/www/smops_env/bin/uwsgi --ini /etc/uwsgi9000.ini
service nginx restart
