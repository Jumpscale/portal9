import mongoengine
import inspect
from JumpScale9Lib.data.models import Models
from js9 import j


def create(outputpath='/optvar/var/populate.json'):
    """
    Creates dummy objects of all defined models and writes the json objects in a file
    """
    j.portal.tools.models.system.connect2mongo()
    output = []
    for name, mem in inspect.getmembers(Models, inspect.isclass):
        if issubclass(mem, mongoengine.base.document.BaseDocument) and issubclass(mem, Models.ModelBase):
            new = mem()
            for attrname, attr in new._fields.items():
                default = attr.default() if inspect.isfunction(attr) else attr.default
                if default:
                    continue
                if attr.__class__ == mongoengine.fields.StringField:
                    setattr(new, attrname, '%s_%s' % (name, attrname))
                elif attr.__class__ == mongoengine.fields.IntField:
                    setattr(new, attrname, 2)
                elif attr.__class__ == mongoengine.fields.BooleanField:
                    setattr(new, attrname, True)
            new.save()
            output.append(new.to_json())
    j.sal.fs.writeFile(outputpath, '\n'.join(output))


def load(path='/optvar/var/populate.json'):
    """
    loads objects from a json file into mongoengine
    """
    if not j.sal.fs.exists(path):
        path = '/optvar/var/populate.json'
        create(path)
    contents = j.sal.fs.fileGetContents(path).splitlines()
    for obj in contents:
        obj = j.data.serializer.json.loads(obj)
        cls = obj.pop('_cls')
        model = getattr(j.portal.tools.models.system, cls)()
        model.save(data=obj)
