import functools
import sqlalchemy

from js9 import j


class SqlDb(object):

    """
    SQL connection
    """

    def __init__(self, lazyConfig):
        self._lazyConfig = lazyConfig
        self._sqldb = None

    def _getSqlDb(self):
        if not self._sqldb:
            host, database, user, password = self._lazyConfig()
            self._sqldb = j.db.sqlConnectionTool.getConnection(host, database,
                                                               user, password)
        return self._sqldb

    def query(self, query):
        """
        Execute a query on the DB

        @param query: SQL query to execute
        @type query: string
        @return: query result
        @rtype: pgqueryobject
        """
        return self._getSqlDb().sqlexecute(query)


def genericLazyConfig(db, dbKey, serviceName, clusterName):
    if db.exists(dbKey):
        rawConfig = db.get(dbKey)

        try:
            config = j.data.serializer.json.loads(rawConfig)
        except ValueError as e:
            raise ValueError("Failed to decode SQL DB config %s: %s" % (config, e))

        try:
            host = config["host"]
            database = config["database"]
            user = config["user"]
            password = config["password"]
        except KeyError as e:
            raise KeyError("Missing a required SQL config key in config %s: %s" % (config, e))

        return host, database, user, password
    else:
        raise RuntimeError("No SQL connection configures for "
                           "service %s of cluster %s" % (
                               serviceName, clusterName))


class __SqlAlchemyConnectionFactory(object):

    """
    SQL alchemy factory, creates sqlalchemy connections and sessions
    """

    def __init__(self):
        self._connections = {}

    def build(self, config):
        engineId = 'postgresql://%(user)s:%(password)s@%(host)s:5432/%(database)s' % config
        if engineId not in self._connections:
            conn = sqlalchemy.create_engine(engineId)

            SessionMaker = sqlalchemy.orm.sessionmaker(bind=conn)
            session = SessionMaker()
            self._connections[engineId] = (conn, session)

        return self._connections[engineId]


class __SqlDbFactory(object):

    """
    SQL DB factory, creates and configures SQL connections

    Created SQL connections are cached, so they are created only once per
    Arakoon db.
    """

    def __init__(self):
        self._dbs = {}

    def _getDbKey(self, serviceName):
        return "applicationserver2_sqldb_config_%s" % serviceName

    def build(self, db, clusterName, serviceName):
        key = "%s_%s" % (clusterName, serviceName)
        dbKey = self._getDbKey(serviceName)

        if key not in self._dbs:
            lazyConfig = functools.partial(genericLazyConfig, db, dbKey,
                                           serviceName, clusterName)
            self._dbs[key] = SqlDb(lazyConfig)
        return self._dbs[key]

    def hasConfig(self, db, serviceName):
        """
        Check if there is an SQL config in `db` for service named `serviceName`

        @param db: Arakoon DB
        @type db: Arakoon DB object
        @param serviceName: name of the service
        @type serviceName: string
        @return: True if there is an SQL config in `db`, False otherwise
        @rtype: boolean
        """
        dbKey = self._getDbKey(serviceName)
        return db.exists(dbKey)

    def configure(self, db, serviceName, host, database, user, password):
        config = j.data.serializer.json.dumps({
            "host": host,
            "database": database,
            "user": user,
            "password": password,
        })
        dbKey = self._getDbKey(serviceName)
        db.set(dbKey, config)

    def getConfig(self, db, serviceName):
        key = self._getDbKey(serviceName)
        if not db.exists(key):
            raise RuntimeError("No SQL connection was configured for service %s"
                               % serviceName)
        rawConfig = db.get(key)
        return j.data.serializer.json.loads(rawConfig)

sqlDbFactory = __SqlDbFactory()
sqlAlchemyConnectionFactory = __SqlAlchemyConnectionFactory()
