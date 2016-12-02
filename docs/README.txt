安装常用软件包
rpm -Uvh http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm
yum install -y epel-release zlib-devel bzip2-devel pcre-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel mysql mysql-server mysql-devel
yum groupinstall -y 'Development tools'
yum install -y nginx

安装SVN客户端
略
注：smops和业务主机都需要安装svn

编辑安装Python3.5
mkdir /root/src/
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz -P /root/src/
cd /root/src/
tar zxvf Python-3.5.2.tgz
cd /root/src/Python-3.5.2
mkdir /usr/local/python3.5.2
./configure --prefix=/usr/local/python3.5.2/
make && make install

安装easy_install(非必须)
wget https://pypi.python.org/packages/5f/ad/1fde06877a8d7d5c9b60eff7de2d452f639916ae1d48f0b8f97bf97e570a/distribute-0.7.3.zip -P /root/src/
unzip distribute-0.7.3.zip
cd distribute-0.7.3
/usr/local/python3.5.2/bin/python3 setup.py install

安装pip(必须)
wget https://pypi.python.org/packages/e7/a8/7556133689add8d1a54c0b14aeff0acb03c64707ce100ecd53934da1aa13/pip-8.1.2.tar.gz -P /root/src/
cd /root/src/
tar zxvf pip-8.1.2.tar.gz
cd pip-8.1.2
/usr/local/python3.5.2/bin/python3 ./setup.py install

安装virtualenv虚拟环境管理工具
/usr/local/python3.5.2/bin/pip install virtualenvwrapper

安装uwsgi
/usr/local/python3.5.2/bin /pip install uwsgi

创建虚拟运行环境并在虚拟环境中安装uwsgi
/usr/local/python3.5.2/bin/virtualenv /data/www/smops_env/
/data/www/smops_env/bin/pip install uwsgi
/data/www/smops_env/bin/pip install virtualenv

创建uwsgi配置文件
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

修改nginx配置文件
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

将smops项目上传到/data/www/目录下并导入数据库
chkconfig mysqld on
service mysqld start
/data/www/smops_env/bin/pip install -r /data/www/smops/requirements.txt
mysql -uroot -p --default-character-set=utf8 smops < /data/www/smopsv7.sql
mkdir /var/log/uwsgi

修改数据库配置
按实际情况修改/data/www/smops/smops/settings.py中以下数据库配置
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

启动配置
iptables -F
echo "nohup /data/www/smops_env/bin/uwsgi --ini /etc/uwsgi9000.ini" >> /etc/rc.local

修改项目配置
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

启动项目
nohup /data/www/smops_env/bin/uwsgi --ini /etc/uwsgi9000.ini
service nginx restart
