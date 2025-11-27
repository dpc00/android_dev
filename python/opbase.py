import json
import io
from pathlib import PosixPath


class OpBaseEncoder(json.JSONEncoder):
    def default(self, obj):
        from pathlib import PosixPath
        from edge import Edge
        if isinstance(obj, PosixPath):
            #print(1, obj.__class__)
            return str(obj)
        if isinstance(obj, OpBase):
            #print(2, obj.__class__)
            return {
                str(obj.__class__): {
                    'npl1': obj.npl1,
                    'npl2': obj.npl2,
                    'opts': obj.opts
                }
            }
        elif isinstance(obj, Edge):
            return [obj.di, obj.si, obj.cdt, obj.udt]
        elif isinstance(obj, set):
            #print(4, obj.__class__)
            return list(obj)
        elif isinstance(obj, tuple):
            return repr(obj)
        elif isinstance(obj, bytes):
            return obj.hex()
        else:
            #print(5, obj.__class__)
            raise Exception('bad type:', obj.__class__)


class OpBase():
    def __init__(self, *args):
        kt = ('npl1', 'npl2', 'opts')
        for k, v in zip(kt, args):
            setattr(self, k, v)
