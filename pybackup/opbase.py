import json
from pathlib import PosixPath

from edge import Edge


class OpBaseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PosixPath):
            # print(1, obj.__class__)
            return str(obj)
        if isinstance(obj, OpBase):
            # print(2, obj.__class__)
            return {
                str(obj.__class__): {
                    "npl1": obj.npl1,
                    "npl2": obj.npl2,
                    "opts": obj.opts,
                }
            }
        if isinstance(obj, Edge):
            return [obj.di, obj.si, obj.cdt, obj.udt]
        if isinstance(obj, set):
            # print(4, obj.__class__)
            return list(obj)
        elif isinstance(obj, tuple):
            return repr(obj)
        elif isinstance(obj, bytes):
            return obj.hex()
        else:
            print(5, obj.__class__)
            return str(obj.__class__)
            # raise Exception('bad type:', obj.__class__)


class OpBase:
    def __init__(self, npl1, npl2, opts={}) -> None:
        self.npl1 = npl1
        self.npl2 = npl2
        self.opts = opts

    def ischanged(self, e: Edge):
        return e.chk_ct()

    def __repr__(self) -> str:
        return (
            str(self.__class__)
            + ": \n"
            + "\t"
            + str(self.npl1)
            + ", "
            + "\t"
            + str(self.npl2)
            + ", "
            + "\t"
            + str(self.opts)
            + "\n\n"
        )
