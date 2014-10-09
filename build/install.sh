#! /bin/sh

CURRENT_DIR=`pwd`
ROOT_DIR=`dirname $CURRENT_DIR`
PROJECT_NAME='mazezoom'
PROJECT_ROOT="${ROOT_DIR}/src"

SOURCE_CODE_SRC="${ROOT_DIR}/src/${PROJECT_NAME}"
REQUIRMENTS_PYLIB="${ROOT_DIR}/src/${PROJECT_NAME}/requirements.txt"

#supervisor
MAZEZOOM_SUPERVISOR_CONF_FILE="mazezoom_supervisord.conf"
MAZEZOOM_SUPERVSIOR_CONF_PATH="/etc/supervisor/conf.d/${MAZEZOOM_SUPERVISOR_CONF_FILE}"
MAZEZOOM_POSITION_DISPATCHE="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/position_dispatcher.py" 
MAZEZOOM_POSITION_DISPATCHE_LOG="/data/log/supervisord/position.log"
MAZEZOOM_POSITION_SCHEDULE="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/position_schedule.py" 
MAZEZOOM_POSITION_SCHEDULE_LOG="/data/log/supervisord/pschedule.log"
MAZEZOOM_CHANNEL_REALTIME="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/channel_realtime_worker.py"
MAZEZOOM_CHANNEL_SCHEDULE="${PROJECT_ROOT}/${PROJECT_NAME}/creepers/channel_schedule.py"
MAZEZOOM_CHANNEL_REALTIME_LOG="/data/log/supervisord/channel_realtime.log"
MAZEZOOM_CHANNEL_SCHEDULE_LOG="/data/log/supervisord/channel_schedule.log"


if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

ETH0_INET=`ifconfig eth0 | grep "inet addr"| awk '{print $2}'| awk -F : '{print $2}'`
if [ -z $ETH0_INET ];then
	ETH0_INET='127.0.0.1'
fi
echo "etho ip address: $ETH0_INET"


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

smart_redis(){
    redis_conf="/etc/redis/redis.conf"
    echo "mv /etc/redis/redis.conf /etc/redis/redis.conf.bak"
    mv $redis_conf /etc/redis/redis.conf.bak
    cat <<EOM >${redis_conf}
daemonize yes
pidfile /var/run/redis/redis-server.pid
port 6379
bind ${ETH0_INET}
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
requirepass afc7c7180c3c43b51b1ebfebae76b5e8
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
    read -p "Please set a username for access mongodb:" mongo_user
    read -p "Please set password:" mongo_passwd
    mongo 127.0.0.1:27017/admin --eval="db.addUser('${mongo_user}', '${mongo_passwd}')"

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
bind_ip=${ETH0_INET}
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
    echo "supervisorctl update"
    supervisorctl update
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
    read -p "Please input mysql host(127.0.0.1):" bind_ip
    read -p "Please input db name:" db_name
    read -p "Please input access ${db_name} user:": username
    read -p "Please set password for ${username}:": password
    if [ -z $bind_ip ];then
        bind_ip='127.0.0.1'
    fi
    if [ -z $db_name ];then
        exit 1
    fi
    if [ -z $password ];then
        exit 1
    fi
    mysql -uroot -h${bind_ip}-p -e"create database if not exist ${db_name} character set utf8;grant all on $"
}


setup(){
    install_libdev
    install_fchksum
    install_pylib_with_pip 
    smart_mongodb
    smart_redis
    smart_supervisor
}

setup
