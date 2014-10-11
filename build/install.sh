#! /bin/sh

CURRENT_DIR=`pwd`
ROOT_DIR=`dirname $CURRENT_DIR`
PROJECT_NAME='mazezoom'
PROJECT_ROOT="${ROOT_DIR}/src"

SOURCE_CODE_SRC="${ROOT_DIR}/src/${PROJECT_NAME}"
REQUIRMENTS_PYLIB="${ROOT_DIR}/src/${PROJECT_NAME}/requirements.txt"
MAZEZOOM_PRODUCTION_SETTINGS="${SOURCE_CODE_SRC}/settings/production.py"

#syncdb
#MAZEZOOM_SYNCDB="python ${SOURCE_CODE_SRC}/manage.py syncdb"

#supervisor
MAZEZOOM_SUPERVISOR_CONF_FILENMAE="mazezoom_supervisord.conf"
MAZEZOOM_SUPERVISOR_CONF_FILE="${CURRENT_DIR}/${MAZEZOOM_SUPERVISOR_CONF_FILENMAE}"
MAZEZOOM_SUPERVSIOR_CONF_PATH="/etc/supervisor/conf.d/${MAZEZOOM_SUPERVISOR_CONF_FILENAME}"
MAZEZOOM_POSITION_DISPATCHE="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/position_dispatcher.py" 
MAZEZOOM_POSITION_SCHEDULE="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/position_schedule.py" 
MAZEZOOM_CHANNEL_REALTIME="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/channel_realtime_worker.py"
MAZEZOOM_CHANNEL_SCHEDULE="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/channel_schedule.py"
MAZEZOOM_CHANNEL_DISPATCH="${SOURCE_CODE_SRC}/creepers/channel_dispatcher.py"
MAZEZOOM_POSITION_DISPATCHE_LOG="/data/log/supervisord/position.log"
MAZEZOOM_POSITION_SCHEDULE_LOG="/data/log/supervisord/pschedule.log"
MAZEZOOM_CHANNEL_REALTIME_LOG="/data/log/supervisord/channel_realtime.log"
MAZEZOOM_CHANNEL_SCHEDULE_LOG="/data/log/supervisord/channel_schedule.log"

#crontab
SYSTEM_CRON="${CURRENT_DIR}/system.cron"


#Redis
REDIS_DB=0
REDIS_PORT=6379
REDIS_HOST='127.0.0.1'
REDIS_PASSWD="afc7c7180c3c43b51b1ebfebae76b5e8"

#Mongodb
MONGO_DB='mazezoom'
MONGO_PORT=27017
MONGO_HOST='127.0.0.1'
MONGO_USER='root'
MONGO_PASSWD='admin4u'

#Mysql
MYSQL_DB='enginet'
MYSQL_USER='admin'
MYSQL_PASSWD='admin4u'
MYSQL_HOST=''


if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

#删除mazezoom_supervisord.conf, 如果存在
if [ -f "${MAZEZOOM_SUPERVSIOR_CONF_FILE}" ]; then
    rm ${MAZEZOOM_SUPERVISOR_CONF_FILE}
fi

#ETH0_INET=`ifconfig eth0 | grep "inet addr"| awk '{print $2}'| awk -F : '{print $2}'`
#if [ -z $ETH0_INET ];then
#    ETH0_INET='127.0.0.1'
#fi
#echo "etho ip address: $ETH0_INET"


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

    echo "sudo apt-get install -y supervisor"
    sudo apt-get install -y supervisor
}

install_fchksum(){
    echo "wget  http://down1.chinaunix.net/distfiles/python-fchksum-1.7.1.tar.gz"
    wget  http://down1.chinaunix.net/distfiles/python-fchksum-1.7.1.tar.gz

    echo "tar -xvzf python-fchksum-1.7.1.tar.gz"
    tar -xvzf python-fchksum-1.7.1.tar.gz

	cd python-fchksum-1.7.1
    echo "python setup.py build"
    python setup.py build

    echo "python setup.py install"
    python setup.py install
    cd ..
}

dispatcher_supervisor(){
    program="dispatcher" 
    cat <<EOM >>${MAZEZOOM_SUPERVISOR_CONF_FILE}
[program:${program}]
command=python ${MAZEZOOM_POSITION_DISPATCHE}
stdout_logfile=${MAZEZOOM_POSITION_DISPATCHE_LOG}
stderr_logfile=${MAZEZOOM_POSITION_DISPATCHE_LOG}
autostart=true
autorestart=true

EOM
}

schedule_supervisor(){
    program="schedule"
    cat <<EOM >>${MAZEZOOM_SUPERVISOR_CONF_FILE}
[program:${program}]
command=python ${MAZEZOOM_POSITION_SCHEDULE}
stdout_logfile=${MAZEZOOM_POSITION_SCHEDULE_LOG}
stderr_logfile=${MAZEZOOM_POSITION_SCHEDULE_LOG}
autostart=true
autorestart=true

EOM
}

channel_realtime_supervisor(){
    program="channel_realtime"
    cat <<EOM >>${MAZEZOOM_SUPERVISOR_CONF_FILE}
[program:${program}]
command=python ${MAZEZOOM_CHANNEL_REALTIME}
stdout_logfile=${MAZEZOOM_CHANNEL_REALTIME_LOG}
stderr_logfile=${MAZEZOOM_CHANNEL_REALTIME_LOG}
autostart=true
autorestart=true

EOM
}

channel_schedule_supervisor(){
    program="channel_schedule"
    cat <<EOM >>${MAZEZOOM_SUPERVISOR_CONF_FILE}
[program:${program}]
command=python ${MAZEZOOM_CHANNEL_SCHEDULE}
stdout_logfile=${MAZEZOOM_CHANNEL_SCHEDULE_LOG}
stderr_logfile=${MAZEZOOM_CHANNEL_SCHEDULE_LOG}
autostart=true
autorestart=true

EOM
}

init_cron(){
    cat <<EOM > ${SYSTEM_CRON}
0 13,21 * * *  python ${MAZEZOOM_CHANNEL_DISPATCH}
EOM
crontab ${SYSTEM_CRON}
}

smart_redis(){
    read -p "Please set IP address for Redis, default:(127.0.0.1):" REIDS_HOST
    if [ -z $REDIS_HOST ];then
        REDIS_HOST='127.0.0.1'
    fi
    echo "Redis host address: ${REDIS_HOST}"
    redis_conf="/etc/redis/redis.conf"
    echo "mv /etc/redis/redis.conf /etc/redis/redis.conf.bak"
    mv $redis_conf /etc/redis/redis.conf.bak
    cat <<EOM >${redis_conf}
daemonize yes
pidfile /var/run/redis/redis-server.pid
port ${REDIS_PORT}
bind ${redis_host}
timeout 0
loglevel notice
logfile /var/log/redis/redis-server.log
databases 16
save 900 1
save 300 10
save 60 10000
rdbcompression yes
dbfilename dump.rdb
dir /var/lib/redis
slave-serve-stale-data yes
requirepass ${REDIS_PASSWD} 
appendonly no
appendfsync everysec
no-appendfsync-on-rewrite no
list-max-ziplist-entries 512
list-max-ziplist-value 64
set-max-intset-entries 512
activerehashing yes
EOM
    /etc/init.d/redis-server restart
}


smart_mongodb(){
    read -p "Please set Mongodb host, default:(127.0.0.1):" MONGO_HOST
    if [ -z $MONGO_HOST ];then
        MONGO_HOST='127.0.0.1'
    fi
    echo "Mongodb host address: ${MONGO_HOST}"

    read -p "Please set a username for access mongodb, default:(root):" mongo_user
    if [ -z $MONGO_USER ];then
        MONGO_USER='root'
    fi
    echo "Mongodb username:" ${MONGO_USER}

    read -p "Please set password, default:(admin4u):" MONGO_PASSWD
    if [ -z $MONGO_PASSWD ];then
        MONGO_PASSWD='admin4u'
    fi
    echo "Mongodb password:" ${mongo_passwd}

    mongo ${MONGO_HOST}:27017/admin --eval="db.addUser('${MONGO_USER}', '${MONGO_PASSWD}')"

    mongo_conf="/etc/mongodb.conf"
    dbpath="/data/mongodb/${PROJECT_NAME}"
    logpath="/data/log/mongodb"
    echo "mkdir -p ${dbpath}"
    mkdir -p ${dbpath}

    echo "mdkir -p ${logpath}"
    mkdir -p ${logpath}

    mv ${mongo_conf} /etc/mongodb.conf.bak

    cat <<EOM >${mongo_conf}
dbpath=${dbpath}
logpath=${logpath}/${PROJECT_NAME}.log
logappend=true
bind_ip=${MONGO_HOST}
port=27017
journal=true
auth=true
smallfiles=true
EOM
    /etc/init.d/mongodb restart
}


smart_supervisor(){
    dispatcher_supervisor
    schedule_supervisor
    channel_realtime_supervisor
    channel_schedule_supervisor
    echo "ln -s ${MAZEZOOM_SUPERVISOR_CONF_FILE} ${MAZEZOOM_SUPERVSIOR_CONF_PATH}"
    ln -s ${MAZEZOOM_SUPERVISOR_CONF_FILE} ${MAZEZOOM_SUPERVSIOR_CONF_PATH}
    echo "supervisorctl update"
    supervisorctl update
    supervisorctl start all
}

install_pylib_with_pip(){
    echo "安装Python扩展包"
    pip install -r ${REQUIRMENTS_PYLIB}
    echo "Python扩展包安装完成"
}


install_src(){
    echo "git clone https://github.com/pymmrd/mazezoom"
    git clone https://github.com/pymmrd/mazezoom
}

init_mysql(){
    read -p "Please input root user for mysql, default:(root)" root_user
    if [ -z $root_user ];then
        root_user='root'
    fi
    read -p "Plaase input password for root user" root_passwd
    read -p "Please input mysql host(127.0.0.1):" MYSQL_HOST
    read -p "Please input db name:" MYSQL_DB
    read -p "Please input access ${MYSQL_DB} user:": MYSQL_USER
    read -p "Please set password for ${MYSQL_USER}:": MYSQL_PASSWD
    if [ -z $MYSQL_HOST ];then
        MYSQL_HOST='127.0.0.1'
    fi
    if [ -z $MYSQL_DB ];then
        echo "Access db name is required"
        exit 1
    fi
    if [ -z $MYSQL_PASSWD ];then
        echo "Access password is required"
        exit 1
    fi
    mysql -u${root_user} -h${MYSQL_HOST} -p${root_passwd} -e"create database if not exists ${MYSQL_DB} character set utf8;grant all on ${MYSQL_DB}.* to \"${MYSQL_USER}\"@\"localhost\" identified by '${MYSQL_PASSWD}'"
}

init_production_settings(){
    cat <<EOM > ${MAZEZOOM_PRODUCTION_SETTINGS}
# -*- coding:utf-8 -*-
from base import *
from mongoengine import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': '${MYSQL_DB}',
        'USER': '${MYSQL_USER}',
        'PASSWORD': '${MYSQL_PASSWD}',
        'HOST': '${MYSQL_HOST}',
        'PORT': '',
        'STORAGE_ENGINE': 'INNODB',
    }
}

MONGO_HOST = '${MONGO_HOST}'
MONGO_PORT = ${MONGO_PORT}
MONGO_DB = '${MONGO_DB}'
MONGO_POOL_AUTH = {
    'user': '${MONGO_USER}',
    'passwd': '${MONGO_PASSWD}',
}

REDIS_HOST = '${REDIS_HOST}'
REDIS_PORT = ${REDIS_PORT}
REDIS_PASSWORD = '${REDIS_PASSWD}'
REDIS_CONF = {
    'host': REDIS_HOST,
    'password': REDIS_PASSWORD,
    'port': REDIS_PORT,
    'db': ${REDIS_DB},
}

EOM
    #syncdb
    python ${SOURCE_CODE_SRC}/manage.py syncdb
}



setup(){
    install_libdev
    install_fchksum
    install_pylib_with_pip 
    smart_mongodb
    smart_redis
    init_mysql
    init_production_settings
    smart_supervisor
    init_cron
}

setup
