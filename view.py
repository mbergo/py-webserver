# encoding: utf-8
from . import DEFAULT_MIMETYPE, LOG, json


class Response(object):
    ''' Generic Response object '''

    def __init__(self, status=200, content=None,
                 mimetype=DEFAULT_MIMETYPE):
        self.status = status
        self.content = content
        self.mimetype = mimetype


class WebHandler(object):
    ''' Receive web request, process and returns Response object '''

    def __init__(self, datastore):
        self.datastore = datastore

    def get_metadata_from_path(self, path):
        meta_data = self.datastore.read()
        mime = DEFAULT_MIMETYPE

        # /dump show all data
        if path == '/dump':
            return json.dumps(meta_data, indent=2), mime

        # remove version number from api
        path = '/'.join(path.split('/')[2:])

        # remove last '/' (if exist)
        if path.endswith('/'):
            path = path[:-1]

        if path.startswith('/'):
            path = path[1:]

        for subpath in path.split('/'):
            if type(meta_data) == dict:
                sub_data = meta_data.get(subpath, None)
                # if <subpath>.mime exist, there is the mime-type
                mime = meta_data.get('%s.mime' % subpath, mime)
            else:
                # path doesn't exist
                sub_data = None
                break
            # next navigation will be on internal element
            meta_data = sub_data

        if type(sub_data) == dict:
            lines = []
            for k, v in sub_data.items():
                if not k.endswith('.mime'):
                    if type(v) == dict:
                        lines.append('%s/' % (k,))
                    else:
                        lines.append('%s' % (k,))
            data = '\n'.join(lines)
        elif sub_data is None:
            data = None
        else:
            data = str(sub_data)

        LOG.debug('Response from path "%s": (%s) %s',
                  path, mime, data)
        return data, mime

    def head(self, path):
        ''' HEAD request '''
        body, mime = self.get_metadata_from_path(path)
        if body is None:
            return Response(status=404)
        else:
            return Response(status=200, mimetype=mime)

    def get(self, path):
        ''' GET request '''
        body, mime = self.get_metadata_from_path(path)
        if body is None:
            return Response(status=404)
        else:
            return Response(status=200, content=body, mimetype=mime)

    def post(self, path):
        ''' POST request. Same as GET '''
        return self.get(path)
