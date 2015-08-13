# Create your views here.
from django.template import RequestContext
from cloudeye.utils.parse_package import parse_package_metainfo
from commons import storage_path, get_filename


def file_upload(request, tmpl=""):
    if request.method == 'POST':
        upload_file = request.FILES.get('file', None)
        if upload_file:
            rawname = upload_file.name
            filesize = upload_file.size
            filename = get_filename(rawname)
            file_path, sub_path = storage_path(filename, prefix='channlapk')
            destination = open(file_path, 'wb')
            for chunk in upload_file.chunks():
                destination.write(chunk)
            destination.close()
            (version, package_name,
             label, icon_path,
             mime_type, md5sum) = parse_package_metainfo(
                file_path,
                rawname
            )
            file_object = File(
                user=user,
                application=application,
                name=label,
                raw_name=rawname[:255],
                package_name=package_name,
                version=version,
                icon=icon_path,
                storage=file_path,
                md5sum=md5sum,
                size=str(filesize),
                mime_type=mime_type
            )
            file_object.save()
    return render_to_response(tmpl, context_instance=RequestContext(request, {}))
