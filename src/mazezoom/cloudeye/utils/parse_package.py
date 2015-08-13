# -*- coding:utf-8 -*-

# Stdlib imports
import re
import zipfile
import mimetypes
from hashlib import md5

# Django Core imports
from django.conf import settings

# Project imports
from cloudeye.models import Application
from commons import storage_path, get_filename, call_subprocess

PACKAGE_META_INFO_CMD = '%s d badging %s'


def compute_md5sum(package):
    md5func = md5()
    with open(package) as f:
        for line in f:
            md5func.update(line)
    md5sum = md5func.hexdigest()
    return md5sum


def parse_android_metainfo(package):

    def process_name_version():
        """
        名字和版本
        """
        version = ''
        package_name = ''
        metainfo = items[0]
        pack_version_regx = re.compile(
            ".+name='(?P<package_name>.+?)'.+versionName='(?P<version>.+)'"
        )
        match = pack_version_regx.match(metainfo)
        if match is not None:
            package_name = match.group('package_name')
            version = match.group('version')
        return version, package_name

    def process_icon(icon):
        """
        图标处理
        """
        icon_name = get_filename(icon)
        icon_path, icon_sub_path = storage_path(icon_name)
        zp = zipfile.ZipFile(package)
        with open(icon_path, 'wb') as f:
            f.write(zp.read(icon))
            f.flush()
        return icon_path, icon_sub_path

    def process_label_icon():
        """
        处理applicaiton,版本
        """
        label = ''
        icon_path = ''
        icon_sub_path = ''
        # "application: label='\xe6\x9d\xad\xe5\xb7\x9e\xe9\x93\xb6\xe8\xa1\x8c' icon='res/drawable/icon.png'"
        label_icon_regx = re.compile(
            ".+label='(?P<label>.+)'.+icon='(?P<icon>.+)'"
        )
        for line in items:
            if line.startswith(label_token):
                label_raw = line
                break

        if label_raw:
            label_match = label_icon_regx.match(label_raw)
            if label_match is not None:
                label = label_match.group('label')
                icon = label_match.group('icon')
                if icon:
                    icon_path, icon_sub_path = process_icon(icon)
        return label, icon_path, icon_sub_path

    version = package_name = label = ''
    icon_path = icon_sub_path = ''
    cmd = PACKAGE_META_INFO_CMD % (settings.AAPT, package)
    message = call_subprocess(cmd)
    items = message.splitlines()
    label_token = 'application: label='
    if items:
        version, package_name = process_name_version()
        label, icon_path, icon_sub_path = process_label_icon()
    return (version, package_name, label, icon_sub_path)


def parse_normal_metainfo(package, rawname):
    version = icon_path = ''
    package_name = label = rawname
    return (version, package_name, label, icon_path)


def parse_package_metainfo(package, rawname=None):
    mimetype, _ = mimetypes.guess_type(package)
    android = Application.ANDROID_FILE_TYPE
    f_zip = Application.ZIP_FILE_TYPE
    so = Application.SO_FILE_TYPE
    if mimetype == android:
        mime_type = Application.ANDROID
        (version, package_name,
         label, icon_path) = parse_android_metainfo(package)
    elif mimetype == so or mimetype == f_zip:
        mime_type = File.MIME_MAP.get(mimetype, '')
        (version, package_name,
         label, icon_path) = parse_normal_metainfo(package, rawname)
    md5sum = compute_md5sum(package)
    return (version, package_name, label, icon_path, mime_type, md5sum)


if __name__ == "__main__":
    pp = "cn.com.hzb.mobilebank.per_1.0.6_liqucn.com.apk"
    print parse_package_metainfo(pp)
