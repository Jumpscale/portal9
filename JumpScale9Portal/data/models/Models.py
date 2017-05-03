
from mongoengine.fields import IntField, StringField, ListField, BooleanField, DictField, EmbeddedDocumentField, FloatField
from mongoengine import DoesNotExist, EmbeddedDocument, Document
import hmac
from js9 import j

try:
    import fcrypt as crypt
except ImportError:
    import crypt

DB = 'jumpscale_system'

default_meta = {'allow_inheritance': True, "db_alias": DB}


def extend(a, b):
    if isinstance(a, list):
        return a + b
    elif isinstance(a, dict):
        tmp = a.copy()
        for i in b:
            if i not in tmp:
                tmp[i] = b[i]
            else:
                tmp[i] = extend(tmp[i], b[i])
        return tmp
    else:
        return b


class ModelBase:
    DoesNotExist = DoesNotExist

    gid = IntField(
        default=lambda: j.application.whoAmI.gid if j.application.whoAmI else 0)
    nid = IntField(
        default=lambda: j.application.whoAmI.nid if j.application.whoAmI else 0)
    epoch = IntField(default=j.data.time.getTimeEpoch)
    meta = default_meta

    @property
    def guid(self):
        return self.pk

    @guid.setter
    def guid(self, value):
        self.pk = value

    def to_dict(self):
        d = j.data.serializer.json.loads(Document.to_json(self))
        d.pop("_cls")
        if "_id" in d:
            d.pop("_id")
        return d

    @classmethod
    def find(cls, query):
        redis = getattr(cls, '__redis__', False)
        if redis:
            raise j.exceptions.RuntimeError("not implemented")
        else:
            return cls.objects(__raw__=query)

    @classmethod
    def _getKey(cls, guid):
        """
        @return hsetkey,key
        """
        ttype = cls._class_name.split(".")[-1]
        key = "models.%s" % ttype
        key = '%s_%s' % (key, guid)
        key = key.encode('utf-8')
        return key

    @classmethod
    def get(cls, guid, returnObjWhenNonExist=False):
        """
        default needs to be in redis, need to mention if not
        """
        redis = getattr(cls, '__redis__', False)

        if redis:
            modelraw = j.core.db.get(cls._getKey(guid))
            if modelraw:
                modelraw = modelraw.decode()
                obj = cls.from_json(modelraw)
                return obj
            else:
                res = None
        else:
            try:
                res = cls.objects.get(id=guid)
            except DoesNotExist:
                res = None
        return res

    @classmethod
    def _save_redis(cls, obj):
        key = cls._getKey(obj.guid)
        meta = cls._meta['indexes']
        expire = meta[0].get('expireAfterSeconds', None) if meta else None
        raw = j.data.serializer.json.dumps(obj.to_dict())
        j.core.db.set(key, raw)
        if expire:
            j.core.db.expire(key, expire)
        return obj

    def validate(self, clean):
        return Document.validate(self, clean)

    def _datatomodel(self, data):
        for key, value in data.items():
            setattr(self, key, value)

    def save(self, data=None):
        redis = getattr(self, '__redis__', False)
        if data:
            self._datatomodel(data)
        if redis:
            return self._save_redis(self)
        else:
            return Document.save(self)

    def delete(self):
        redis = getattr(self, '__redis__', False)
        if redis:
            key = self._getKey(self.guid)
            j.core.db.delete(key)
        else:
            return Document.delete(self)

    @classmethod
    def exists(cls, guid):
        return bool(cls.get(guid=guid))

    def getset(cls):
        redis = getattr(cls, '__redis__', False)
        key = cls._getKey(cls.guid)
        if redis:
            model = cls.get(key)
            if model is None:
                model = cls.save()
            return model
        else:
            if not cls.get(cls.guid):
                cls.save()
            return cls.get(cls.guid)

    def __str__(self):
        return j.data.serializer.json.dumps(self.to_dict(), indent=2)

    __repr__ = __str__


class Errorcondition(ModelBase, Document):
    nid = IntField(required=True)
    gid = IntField(required=True)
    aid = IntField(default=0)
    pid = IntField(default=0)
    jid = StringField(default='')  # TODO: *2 is this right, string???
    masterjid = IntField(default=0)
    appname = StringField(default="")
    level = IntField(default=1, required=True)
    type = StringField(choices=("BUG", "PERF", "OPS", "UNKNOWN"),
                       default="UNKNOWN", required=True)
    state = StringField(choices=("NEW", "ALERT", "CLOSED"),
                        default="NEW", required=True)
    # StringField() <--- available starting version 0.9
    errormessage = StringField(default="")
    errormessagePub = StringField(default="")  # StringField()
    category = StringField(default="")
    tags = StringField(default="")
    code = StringField()
    funcname = StringField(default="")
    funcfilename = StringField(default="")
    funclinenr = IntField(default=0)
    backtrace = StringField()
    backtraceDetailed = StringField()
    extra = StringField()
    lasttime = IntField(default=j.data.time.getTimeEpoch())
    closetime = IntField(default=j.data.time.getTimeEpoch())
    occurrences = IntField(default=0)


class Log(ModelBase, Document):
    aid = IntField(default=0)
    pid = IntField(default=0)
    jid = StringField(default='')
    masterjid = IntField(default=0)
    appname = StringField(default="")
    level = IntField(default=1, required=True)
    message = StringField(default='')
    type = StringField(choices=("BUG", "PERF", "OPS", "UNKNOWN"),
                       default="UNKNOWN", required=True)
    state = StringField(choices=("NEW", "ALERT", "CLOSED"),
                        default="NEW", required=True)
    # StringField() <--- available starting version 0.9
    category = StringField(default="")
    tags = StringField(default="")
    epoch = IntField(default=j.data.time.getTimeEpoch())


class Grid(ModelBase, Document):
    name = StringField(default='master')
    #  id = IntField(default=1)


class Group(ModelBase, Document):
    name = StringField(default='')
    domain = StringField(default='')
    gid = IntField(default=1)
    roles = ListField(StringField())
    active = BooleanField(default=True)
    description = StringField(default='master')
    lastcheck = IntField(default=j.data.time.getTimeEpoch())


class Job(EmbeddedDocument):
    nid = IntField(required=True)
    gid = IntField(required=True)
    data = StringField(default='')
    streams = ListField(StringField())
    level = IntField()
    state = StringField(required=True, choices=(
        'SUCCESS', 'ERROR', 'TIMEOUT', 'KILLED', 'QUEUED', 'RUNNING'))
    starttime = IntField()
    time = IntField()
    tags = StringField()
    critical = StringField()

    meta = extend(default_meta, {
        'indexes': [{'fields': ['epoch'], 'expireAfterSeconds': 3600 * 24 * 5}],
        'allow_inheritance': True,
        "db_alias": DB
    })


class Command(ModelBase, Document):
    guid = StringField(unique=True, required=True)
    gid = IntField(default=0)
    nid = IntField(default=0)
    cmd = StringField()
    roles = ListField(StringField())
    fanout = BooleanField(default=False)
    args = DictField()
    data = StringField()
    tags = StringField()
    starttime = IntField()
    jobs = ListField(EmbeddedDocumentField(Job))

    meta = extend(default_meta, {
        'indexes': [{'fields': ['guid']}]
    })


class Audit(ModelBase, Document):
    user = StringField(default='')
    result = StringField(default='')
    call = StringField(default='')
    status_code = IntField(default=0)
    args = StringField(default='')
    kwargs = StringField(default='')
    timestamp = IntField(default=j.data.time.getTimeEpoch())

    meta = extend(default_meta, {'indexes': [
        {'fields': ['epoch'], 'expireAfterSeconds': 3600 * 24 * 5}
    ], 'allow_inheritance': True, "db_alias": DB})


class Disk(ModelBase, Document):
    partnr = IntField()
    path = StringField(default='')
    size = IntField(default=0)
    free = IntField()
    ssd = IntField()
    fs = StringField(default='')
    mounted = BooleanField()
    mountpoint = StringField(default='')
    active = BooleanField()
    model = StringField(default='')
    description = StringField(default='')
    type = ListField(StringField())  # BOOT, DATA, ...
    # epoch of last time the info was checked from reality
    lastcheck = IntField(default=j.data.time.getTimeEpoch())


class VDisk(ModelBase, Document):

    machineguid = StringField(required=True)
    diskid = IntField()
    fs = StringField(default='')
    size = IntField(default=0)
    free = IntField()
    sizeondisk = IntField()
    mounted = BooleanField()
    path = StringField(default='')
    description = StringField(default='')
    mountpoint = StringField(default='')
    role = ListField(StringField())
    type = ListField(StringField())
    order = IntField()
    devicename = StringField(default='')  # if known device name in vmachine
    lastcheck = IntField(default=j.data.time.getTimeEpoch())
    backup = BooleanField()
    backuplocation = StringField()
    backuptime = IntField(default=j.data.time.getTimeEpoch())
    backupexpiration = IntField()


class Alert(ModelBase, Document):
    username = StringField(default='')
    description = StringField(default='')
    descriptionpub = StringField(default='')
    level = IntField(min_value=1, max_value=3, default=1)
    # dot notation e.g. machine.start.failed
    category = StringField(default='')
    tags = StringField(default='')  # e.g. machine:2323
    state = StringField(choices=("NEW", "ALERT", "CLOSED"),
                        default='NEW', required=True)
    history = ListField(DictField())
    # first time there was an error condition linked to this alert
    inittime = IntField(default=j.data.time.getTimeEpoch())
    # last time there was an error condition linked to this alert
    lasttime = IntField()
    closetime = IntField()  # alert is closed, no longer active
    # $nr of times this error condition happened
    nrerrorconditions = IntField()
    errorconditions = ListField(IntField())  # ids of errorconditions


class Heartbeat(ModelBase, Document):

    """
    """
    lastcheck = IntField(default=j.data.time.getTimeEpoch())


class Machine(ModelBase, Document):
    name = StringField(default='')
    roles = ListField(StringField())
    netaddr = StringField(default='')
    ipaddr = ListField(StringField())
    active = BooleanField()
    # STARTED,STOPPED,RUNNING,FROZEN,CONFIGURED,DELETED
    state = StringField(choices=("STARTED", "STOPPED", "RUNNING", "FROZEN",
                                 "CONFIGURED", "DELETED"), default='CONFIGURED', required=True)
    mem = IntField()  # $in MB
    cpucore = IntField()
    description = StringField(default='')
    otherid = StringField(default='')
    type = StringField(default='')  # VM,LXC
    # epoch of last time the info was checked from reality
    lastcheck = IntField(default=j.data.time.getTimeEpoch())


class Nic(ModelBase, Document):
    name = StringField(default='')
    mac = StringField(default='')
    ipaddr = ListField(StringField())
    active = BooleanField(default=True)
    # poch of last time the info was checked from reality
    lastcheck = IntField(default=j.data.time.getTimeEpoch())


class Node(ModelBase, Document):
    name = StringField(default='')
    roles = ListField(StringField())
    netaddr = DictField(default={})
    machineguid = StringField(default='')
    ipaddr = ListField(StringField())
    active = BooleanField()
    peer_stats = IntField()  # node which has stats for this node
    # node which has transactionlog or other logs for this node
    peer_log = IntField()
    peer_backup = IntField()  # node which has backups for this node
    description = StringField(default='')
    lastcheck = IntField(default=j.data.time.getTimeEpoch())
    # osisrootobj,$namespace,$category,$version
    _meta = ListField(StringField())


class Process(ModelBase, Document):
    aysdomain = StringField(default='')
    aysname = StringField(default='')
    pname = StringField(default='')  # process name
    sname = StringField(default='')  # name as specified in startup manager
    ports = ListField(IntField())
    instance = StringField(default='')
    systempid = ListField(IntField())  # system process id (PID) at this point
    epochstart = IntField()
    epochstop = IntField()
    active = BooleanField()
    lastcheck = IntField(default=j.data.time.getTimeEpoch())
    cmd = StringField(default='')
    workingdir = StringField(default='')
    parent = StringField(default='')
    type = StringField(default='')
    statkey = StringField(default='')
    nr_file_descriptors = FloatField()
    nr_ctx_switches_voluntary = FloatField()
    nr_ctx_switches_involuntary = FloatField()
    nr_threads = FloatField()
    cpu_time_user = FloatField()
    cpu_time_system = FloatField()
    cpu_percent = FloatField()
    mem_vms = FloatField()
    mem_rss = FloatField()
    io_read_count = FloatField()
    io_write_count = FloatField()
    io_read_bytes = FloatField()
    io_write_bytes = FloatField()
    nr_connections_in = FloatField()
    nr_connections_out = FloatField()


class Test(ModelBase, Document):
    name = StringField(default='')
    testrun = StringField(default='')
    path = StringField(default='')
    state = StringField(choices=("OK", "ERROR", "DISABLED"),
                        default='OK', required=True)
    priority = IntField()  # lower is highest priority
    organization = StringField(default='')
    author = StringField(default='')
    version = IntField()
    categories = ListField(StringField())
    starttime = IntField(default=j.data.time.getTimeEpoch())
    endtime = IntField()
    enable = BooleanField()
    result = DictField()
    output = DictField(default={})
    eco = DictField(default={})
    license = StringField(default='')
    source = DictField(default={})


class User(ModelBase, Document):
    name = StringField(default='')
    domain = StringField(default='')
    passwd = StringField(default='')  # stored hashed
    roles = ListField(StringField())
    active = BooleanField()
    description = StringField(default='')
    emails = ListField(StringField())
    xmpp = ListField(StringField())
    mobile = ListField(StringField())
    # epoch of last time the info updated
    lastcheck = IntField(default=j.data.time.getTimeEpoch())
    groups = ListField(StringField())
    authkey = StringField(default='')
    data = StringField(default='')
    authkeys = ListField(StringField())

    def authenticate(username, passwd):
        for user in User.find({'name': username}):
            if hmac.compare_digest(user.passwd, j.sal.unix.crypt(passwd, user.passwd)):
                return True
        return False

    def save(user):
        if not user.id:
            user.passwd = j.sal.unix.crypt(user.passwd)
        else:
            olduser = User.get(user.id)
            if olduser.passwd != user.passwd:  # change passwd
                user.passwd = j.sal.unix.crypt(user.passwd)
        super(ModelBase, user).save()


class SessionCache(ModelBase, Document):
    __redis__ = True
    user = StringField()
    kwargs = DictField()
    _creation_time = IntField(default=j.data.time.getTimeEpoch())
    _accessed_time = IntField(default=j.data.time.getTimeEpoch())
    _expire_at = IntField(default=None)
    guid = StringField()
    meta = extend(default_meta, {'indexes':
                                 [{'fields': ['epoch'], 'expireAfterSeconds': 432000}],
                                 'allow_inheritance': True,
                                 'db_alias': DB})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _save_redis(self, obj):
        key = self._getKey(obj.guid)
        indexes = self._meta['indexes']
        expire = next(iter(indexes), {}).get('expireAfterSeconds', None)
        raw = j.data.serializer.json.dumps(obj.to_dict())
        j.core.db.set(key, raw)
        if self._expire_at:
            j.core.db.expireat(self._getKey(self.guid), self._expire_at)
        elif expire:
            j.core.db.expire(key, expire)
        return obj


del EmbeddedDocument
