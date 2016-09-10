# FreeSpoon_
菜谱项目安装指南 
1.准备一个新的环境 
2.更新源  apt-get update
	安装 pip         
			apt-get install python-pip -y
	安装 django      
			pip install django -i https://pypi.tuna.tsinghua.edu.cn/simple
	更新源  
	   		apt-get update
	安装 mysql       
			apt-get install mysql-server mysql-client -y     弹窗输入密码：123456
	安装 mysqldb     
			apt-get install python-mysqldb
	安装 djangorestframework            
			pip install djangorestframework -i https://pypi.tuna.tsinghua.edu.cn/simple
	安装 django-filter 		    
			pip install django-filter 
	更新源     
			apt-get update
	安装 markdown 			    
			pip install markdown 
	安装 git   
			apt-get install git -y
	安装 libmysqlclient-dev
			apt-get install libmysqlclient-dev -y
	安装 python-pip python-dev
			apt-get install python-pip python-dev -y
	安装 		apt-get install libtiff5-dev libjpeg8-dev zlib1g-dev \
        	libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python-tk -y
	安装 Pillow
			pip install Pillow -i https://pypi.tuna.tsinghua.edu.cn/simple

3.从github 上下载最新源代码
			git clone https://github.com/lzq941129/FreeSpoon_.git
4.创建 数据库  
进入 mysql      
		mysql -uroot -p    密码：123456
创建数据库名字为FreeSpoon_	
		create database FreeSpoon_ default charset=utf8;
更改编码问题:        
		cd /etc/mysql/    打开目录下的 my.cof 文件   
在client]  下边加上     
		default-character-set=utf8      保存退出   
重启 mysql 服务    	
		service mysql restart
5.在项目的根目录做数据库迁移    含有manage.py  目录下
		python manage.py migrate
6.导入mysql 服务的 环境变量
	export DBHOST=0.0.0.0 && export DBPASSWD=123456
7.创建管理员用户   在python manage.py 同级目录
	python manage.py createsuperuser
	用户名 邮箱 密码
8.启动项目   在manage.py 同级目录
	python manage.py runserver 0.0.0.0:8080
	
9.mysql 远程连接拒绝访问

进入mysql  mysql-uroot -p
use mysql;
GRANT ALL PRIVILEGES ON *.* TO 'myuser'@'%' IDENTIFIED BY 'mypassword' WITH GRANT OPTION;
flush privileges;
exit
