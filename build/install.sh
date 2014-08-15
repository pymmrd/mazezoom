#! /bin/sh

CURRENT_DIR=`pwd`
SOFT_DOWN_ADDR="10.2.252.0:89"
SYSTEM_NGINX_DIR="/etc/nginx"
SYSTEM_UWSGI_DIR="/etc/conf.d"
ROOT_DIR=`dirname $CURRENT_DIR`
PROJECT_INSTALL_DIR="/opt/webtrack"
PROJECT_DATA_DIR="/opt/webtrack/data"
NGINX_CONFIG_FILE="${SYSTEM_NGINX_DIR}/nginx.conf"
CLOUDEYE_UWSGI_CONFIG_FILE="${CURRENT_DIR}/cloudeye.ini" 
CLOUDEYE_NGINX_CONFIG_FILE="${CURRENT_DIR}/nginx.conf"
CLOUDEYE_NGINX_REAL_CONFIG_FILE="${CURRENT_DIR}/nginx_cloudeye.conf"

MONGODB_INSTALL_PATH="/usr/local/mongo"
MONGODB_CONFIG_FILE="${CURRENT_DIR}/mongodb.conf"
MONGODB_UPSTART_CONFIG="${CURRENT_DIR}/upstart/mongodb.conf"

REDIS_CONFIG_FILE="${CURRENT_DIR}/redis.conf"
SOURCE_CODE_SRC="${ROOT_DIR}/src/server"
REQUIRMENTS_PYLIB="${ROOT_DIR}/src/server/requirements.txt"

if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

backup_nginx_config(){
    if [ -f "${NGINX_CONFIG_FILE}"]; then
        mv ${NGINX_CONFIG_FILE} "${NGINX_CONFIG_FILE}.bak" 
    fi
}


install_libdev(){
  sudo apt-get install -y python-dev gcc libsqlite3-dev libqtwebkit-dev make g++ libfreetype6-dev  libfontconfig-dev libyaml-dev 

}

install_java(){
    echo "安装Java"
    sudo apt-get install -y openjdk-7-jdk
    echo "Java安装成功"

}

install_redis_server(){
    echo "安装Redis"

    echo "apt-get install -y redis-server"
    apt-get install -y redis-server

    echo "cp $REDIS_CONFIG_FILE /etc/redis/"
    cp $REDIS_CONFIG_FILE /etc/redis/

    echo "/etc/init.d/redis-server restart"
    /etc/init.d/redis-server restart

    echo "Redis安装成功"
}

install_nginx(){
    echo "安装Nginx."
    apt-get install -y nginx
    echo "Nginx安装成功."

}

nginx_load(){
    install_nginx

    echo "cp -f ${CLOUDEYE_NGINX_CONFIG_FILE} /etc/nginx/"
    cp -f ${CLOUDEYE_NGINX_CONFIG_FILE} /etc/nginx/

    echo "cp -f ${CLOUDEYE_NGINX_REAL_CONFIG_FILE} /etc/nginx/conf.d/"
    cp -f ${CLOUDEYE_NGINX_REAL_CONFIG_FILE} /etc/nginx/conf.d/

    echo "/etc/init.d/nginx restart"
    /etc/init.d/nginx restart

}

install_uwsgi(){
    echo "安装uwsgi"
    apt-get install -y uwsgi uwsgi-plugin-python
    echo "安装uwsgi结束."
}

uwsgi_load(){
    install_uwsgi
    echo "cp -f ${CLOUDEYE_UWSGI_CONFIG_FILE} /etc/uwsgi/apps-enabled"
    cp -f ${CLOUDEYE_UWSGI_CONFIG_FILE} /etc/uwsgi/apps-enabled
    /etc/init.d/uwsgi restart
}

install_pip(){
    echo "安装PIP"
    apt-get install -y python-pip
    echo "安装PIP成功"
}

install_pylib_with_pip(){
    echo "安装Python扩展包"
    pip install -r ${REQUIRMENTS_PYLIB}
    echo "Python扩展包安装完成"
}


install_phantomjs(){
    echo "安装Phantomjs"
    phantomjsversion="phantomjs-1.9.2"
    phantomjs="$phantomjsversion.tar.gz"

    down_url="http://$SOFT_DOWN_ADDR/$phantomjs"
    echo "开始下载$phantomjs"
    wget $down_url
    echo "$phantomjs下载完成"

    echo "tar -xvzf $phantomjs"
    tar -xvzf $phantomjs

    echo "mv ./phantomjs-1.9.2/phantomjs /usr/bin"
    mv ./phantomjs-1.9.2/phantomjs /usr/bin
    rm $phantomjsversion -r
    rm $phantomjs
}

init_mongodb(){
    dbname="cloudwaf"
    initdata="$dbname.tar"
    down_url="http://$SOFT_DOWN_ADDR/$initdata"
    echo "wget $down_url"
    wget $down_url

    echo "tar -xvf $initdata"
    tar -xvf $initdata
    echo "/usr/local/mongo/bin/mongo -h127.0.0.1 --port=27017 -uroot -padmin4u --authenticationDatabase admin -d cloudwaf cloudwaf"
    /usr/local/mongo/bin/mongorestore -h127.0.0.1 --port=27017 -uroot -padmin4u --authenticationDatabase admin -d $dbname $dbname
    rm $dbname -R
    rm $initdata
}

install_mongodb(){
    mongodb="mongodb-linux-x86_64-2.4.9.tgz"
    down_url="http://$SOFT_DOWN_ADDR/$mongodb"

    echo "开始下载$mongodb"
    echo "wget $down_url"
    wget $down_url
    echo "$mongodb下载完成"

    echo "tar -xvzf $mongodb"
    tar -xvzf $mongodb

    if [ -d "$MONGODB_INSTALL_PATH" ]
    then
        rm $MONGODB_INSTALL_PATH -rf
    fi

    echo "mv ./mongodb-linux-x86_64-2.4.9 $MONGODB_INSTALL_PATH"
    mv ./mongodb-linux-x86_64-2.4.9 $MONGODB_INSTALL_PATH

    echo "mongodb.conf /etc/mongodb.conf"
    cp mongodb.conf /etc/mongodb.conf

    echo " $MONGODB_UPSTART_CONFIG /etc/init/mongodb.conf"
    cp $MONGODB_UPSTART_CONFIG /etc/init/mongodb.conf

    echo "initctl start mongodb"
    initctl start mongodb

    echo "/usr/local/mongo/bin/mongo 127.0.0.1:27017/admin --eval=\"db.addUser('root', 'admin4u')\""
    /usr/local/mongo/bin/mongo 127.0.0.1:27017/admin --eval="db.addUser('root', 'admin4u')"

    rm $mongodb
}

install_src(){
    echo "cp $SOURCE_CODE_SRC $PROJECT_INSTALL_DIR -R"
    cp $SOURCE_CODE_SRC $PROJECT_INSTALL_DIR -R
    echo "chown daemon:daemon $PROJECT_INSTALL_DIR -R"
    chown daemon:daemon $PROJECT_INSTALL_DIR -R
}

init_user(){
    python /opt/webtrack/server/manage.py create_default_user
}

download_geo(){
   echo "wget -P $PROJECT_DATA_DIR http://$SOFT_DOWN_ADDR/GeoIPCity.dat" 
   wget -P $PROJECT_DATA_DIR "http://$SOFT_DOWN_ADDR/GeoIPCity.dat" 
   echo "wget -P $PROJECT_DATA_DIR http://$SOFT_DOWN_ADDR/cities.sqlite.dat" 
   wget -P $PROJECT_DATA_DIR "http://$SOFT_DOWN_ADDR/cities.sqlite.dat" 
   echo "wget -P $PROJECT_DATA_DIR http://$SOFT_DOWN_ADDR/tldextract.cache" 
   wget -P $PROJECT_DATA_DIR "http://$SOFT_DOWN_ADDR/tldextract.cache" 

  
}


setup(){
    mkdir -p $PROJECT_INSTALL_DIR
    mkdir -p $PROJECT_DATA_DIR
    install_src
    download_geo
    addgroup daemon
    adduser daemon daemon
    install_libdev
    install_redis_server
    install_phantomjs
    install_mongodb
    install_pip 
    install_pylib_with_pip 
    nginx_load
    init_mongodb
    uwsgi_load
    #TODO数据库的初始化
    init_user
}

setup

if [ -s /opt/clish/conf_mgr.py ]; then
    /opt/clish/conf_mgr.py inst_prod webui
fi
