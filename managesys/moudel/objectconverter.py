# coding:utf8
import new
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.dynamic import AppenderQuery


class ObjectToDict(object):

    def __init__(self, include_path=[], exclude_property=[]):
        self.include_path = include_path
        self.exclude_property = exclude_property

    def _convert(self, obj, path=""):
        fields = {}
        if len(path) != 0:
            if path in self.include_path:
                pass
            return None
        for f in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
            if f in self.exclude_property:
                continue
            value = obj.__getattribute__(f)
            if isinstance(value, new.instancemethod):
                continue
            elif isinstance(value, list):
                r = []
                for i in value:
                    r.append(self._convert(i))
                fields[f] = r
            elif isinstance(value, dict):
                fields[f] = self._convert(value)
            else:
                fields[f] = value
        return fields

    def __call__(self, obj):
        return self._convert(obj)


class ObjectToDictEx(object):

    def __init__(self, include_path=[], exclude_property=[], ref_path={}, convert_call_back=None, convert_parameter={}):
        self.include_path = include_path
        self.exclude_property = exclude_property
        self.ref_path = ref_path
        self._convert_call_back = convert_call_back
        self._convert_parameter = convert_parameter

    def _convert(self, obj):
        fields = {}
        if len(self.include_path) > 0:
            for key in self.include_path:
                fields[key] = getattr(obj, key)
        else:
            for c in obj.get_local_attribute():
                v = getattr(obj, c)
                if c in self.exclude_property:
                    continue
                fields[c] = v
        for f in self.ref_path:
            value = getattr(obj, f)
            if isinstance(value, dict) or isinstance(value.__class__, DeclarativeMeta):
                attributes = {}
                output_keys = self.ref_path[f]
                for i in output_keys:
                    attributes[i] = getattr(value, i)
                fields[f] = attributes
            elif isinstance(value, (list, tuple)):
                output_key = self.ref_path[f]
                attributes = [v.__getattribute__(output_key) for v in value]
                fields[f] = attributes
            elif isinstance(value, AppenderQuery):
                output_key = self.ref_path[f]
                query_value = value.all()
                attributes = [v.__getattribute__(
                    output_key) for v in query_value]
                fields[f] = attributes
        return fields

    def __call__(self, obj):
        if isinstance(obj, (list, tuple)):
            result = []
            for o in obj:
                r = self._convert(o)
                if self._convert_call_back:
                    if isinstance(self._convert_call_back, (list, tuple)):
                        for convert_call_back in self._convert_call_back:
                            d = convert_call_back(o, **self._convert_parameter)
                            if d:
                                for (k, v) in d.iteritems():
                                    r[k] = v
                    else:
                        d = self._convert_call_back(
                            o, **self._convert_parameter)
                        if d:
                            for (k, v) in d.iteritems():
                                r[k] = v
                result.append(r)
            return result
        else:
            r = self._convert(obj)
            if self._convert_call_back:
                if isinstance(self._convert_call_back, (list, tuple)):
                    for convert_call_back in self._convert_call_back:
                        d = convert_call_back(obj, **self._convert_parameter)
                        if d:
                            for (k, v) in d.iteritems():
                                r[k] = v
                else:
                    d = self._convert_call_back(obj, **self._convert_parameter)
                    if d:
                        for (k, v) in d.iteritems():
                            r[k] = v
            return r
