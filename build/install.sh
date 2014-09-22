#! /bin/sh

CURRENT_DIR=`pwd`
ROOT_DIR=`dirname $CURRENT_DIR`

MONGODB_INSTALL_PATH="/usr/local/mongo"
MONGODB_CONFIG_FILE="${CURRENT_DIR}/mongodb.conf"
MONGODB_UPSTART_CONFIG="${CURRENT_DIR}/upstart/mongodb.conf"

REDIS_CONFIG_FILE="${CURRENT_DIR}/redis.conf"
SOURCE_CODE_SRC="${ROOT_DIR}/src/mazezoom"
REQUIRMENTS_PYLIB="${ROOT_DIR}/src/mazezoom/requirements.txt"

if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi


install_libdev(){
    echo "sudo apt-get update"
    sudo apt-get update

    echo "sudo apt-get install -y python-dev gcc libsqlite3-dev make g++ libfreetype6-dev"
    sudo apt-get install -y python-dev gcc libsqlite3-dev make g++ libfreetype6-dev

    echo "sudo apt-get install -y libfontconfig-dev libyaml-dev git-core redis-server mongodb"
    sudo apt-get install -y libfontconfig-dev libyaml-dev git-core redis-server mongodb

    echo "sudo apt-get install -y libmysqlclient-dev python-pip zlib1g-dev" 
    sudo apt-get install -y libmysqlclient-dev python-pip zlib1g-dev 

    echo "sudo apt-get install -y mysql-server mysql-client" 
    sudo apt-get install -y mysql-server mysql-client 

}

install_fchksum(){
    echo "wget  http://down1.chinaunix.net/distfiles/python-fchksum-1.7.1.tar.gz"
    wget  http://down1.chinaunix.net/distfiles/python-fchksum-1.7.1.tar.gz

    echo "tar -xvzf python-fchksum-1.7.1.tar.gz"
    tar -xvzf python-fchksum-1.7.1.tar.gz

    echo "python ./python-fchksum-1.7.1/setup.py build"
    python ./python-fchksum-1.7.1/setup.py build
    
    echo "python ./pyhton-fchksum-1.7.1/setup.py install"
    python ./pyhton-fchksum-1.7.1/setup.py install

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
    echo "git clone https://github.com/pymmrd/mazezoom"
    git clone https://github.com/pymmrd/mazezoom
}


setup(){
    install_libdev
    install_fchksum
    install_src
    install_redis_server
    install_pylib_with_pip 
}

setup

if [ -s /opt/clish/conf_mgr.py ]; then
    /opt/clish/conf_mgr.py inst_prod webui
fi
