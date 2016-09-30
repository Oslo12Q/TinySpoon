# TinySpoon  

### 菜谱项目安装指南 

准备一个新的环境  

更新源  

	mysql -uroot -p123456  
	apt-get update  

安装 pip  

	apt-get install python-pip python-dev -y  

安装 django  

	pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple  

更新源  

 	apt-get update  

安装 mysql  

	apt-get install mysql-server mysql-client -y  

> 弹窗输入密码：123456  

安装 mysqldb  

	apt-get install python-mysqldb  

安装 djangorestframework  

	pip install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple  

安装 django-filter  

	pip install django-filter  

安装 git  

	apt-get install git -y  

安装 libmysqlclient-dev  

	apt-get install libmysqlclient-dev -y  

安装 Pillow  

	apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \  
        	libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk -y
	pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple

从github 上下载最新源代码  

	git clone https://github.com/lzq941129/TinySpoon.git  

创建数据库  

进入mysql  

	mysql -uroot -p123456  

创建数据库名字为TinySpoon  

	create database TinySpoon default charset=utf8;  

更改编码问题:  

	cd /etc/mysql/  

打开目录下的`my.cnf`文件, 在[client]下边加上`default-character-set=utf8`  

保存退出  

重启mysql服务  

	service mysql restart  

导入TinySpoon的环境变量  

	export DBHOST=0.0.0.0 && export DBPASSWD=123456  

在项目的根目录做数据库迁移  

	python manage.py migrate  

创建管理员用户  

	python manage.py createsuperuser  

启动项目  

	python manage.py runserver 0.0.0.0:8080  

### 解决MySQL远程连接拒绝访问问题  

	mysql -uroot -p123456  
	
	USE mysql;  
	GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;  
	FLUSH PRIVILEGES;  
	EXIT  
