# -*- coding:utf-8 -*-

import os
import zipfile

GETCERTINFO = "getCertInfo.jar"
MEDIA_TEMP_OUT = 'temp.out'
GETCERTINFO_JAR = os.path.join(TOOL_DIR, GETCERTINFO)

def generate_public_key(owndir, rsa, uuid1_file, logger):
    """
    获取原apk的公钥，取前50个字节，然后用uuid[1]做密钥，对它加密后写入nagain.secr文件的公钥位置
    *******************************************************************
    * java -jar getCertInfo.jar .RSA文件  输出文件                    *
    *******************************************************************
    """
    # 生成临时文件temp.out
    temp_out = get_media_file(owndir, MEDIA_TEMP_OUT)
    cmd = "java -jar %s %s %s" % (
        GETCERTINFO_JAR,
        rsa,
        temp_out
    )
    logger_subprocess(logger, cmd)
    return data


def compute_rsa_md5sum(rsa_path, apk_path):
    filename = apk_path.rpslit('/', 1).split('.')[0]
    owndir = os.path.join('/data/rsa', filename)
    if not os.path.exists(owndir):
        os.makedirs(owndir)
    zp = zipfile.ZipFile(apk_path)
    rsa = zp.extract(rsa_path, owndir)

