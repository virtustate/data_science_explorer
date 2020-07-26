import redis
import datetime
import pandas
from io import StringIO


# wrapper class for Redis functionality
class RedisDB:
    chunkLength = 500 * 1000 * 1000  # strings have 512MB limit so split into list
    maximum_databases = 100

    def __init__(self, dataset_id=0):
        self.server = 'localhost'
        self.port = 6379
        self.dataset_id = dataset_id
        if dataset_id == 0:
            self.db_number = 0
        else:
            self.db_number = self.get_dataset_db()
            if self.db_number <= 0:
                self.db_number = self.get_first_free_db()
            if self.db_number <= 0:
                raise BufferError("Maximum Redis dbs already loaded. Unload some to load new ones.")
        self.my_redis_db = redis.Redis(host=self.server, port=self.port, db=self.db_number)

    def ping(self):
        return self.my_redis_db.ping()

    def start_load(self):
        self.my_redis_db.set('dataset_id', self.dataset_id)
        self.my_redis_db.set('lastLoaded', 'loading...')

    def end_load(self):
        self.my_redis_db.set('lastLoaded', datetime.datetime.now().strftime('%Y/%m/%d %H:%M'))

    def error_load(self, message):
        self.my_redis_db.set('lastLoaded', message)

    def set(self, key, value):
        # self.myRedisDB.set(key,value)
        self.save_list(key, value)

    def append(self, key, value):
        for i in range(0, len(value), self.chunkLength):
            self.my_redis_db.rpush(key, value[i:i + self.chunkLength])

    def get(self, key):
        # return self.myRedisDB.get(key).decode('utf-8')
        return self.get_list(key)

    def delete(self, key):
        return self.my_redis_db.delete(key)

    def get_df(self, key):
        df = pandas.read_csv(StringIO(self.get(key)))
        if 'airing' in key.lower():
            # strange, blank string values seem to come back from redis as na's
            # the fillna when creating the dataset doesn't address this
            # df[common.airingMetrics]=df[common.airingMetrics].fillna(0)
            # df[common.airingMetrics]=df[common.airingSegments].fillna('blank')
            # when re-hydrating from csv, make sure on segment columns get int types
            if 'dma' in df.columns:
                df.dma = df.dma.astype(str)
            if 'spotlen' in df.columns:
                df.spotlen = df.spotlen.astype(str)
        if 'visit' in key.lower():
            if 'segment1' in df.columns:
                df.segment1 = df.segment1.astype(str)
            if 'segment2' in df.columns:
                df.segment2 = df.segment2.astype(str)
        df = df.drop(['Unnamed: 0'], axis=1)  # not sure why this column gets added
        return df.fillna('blank')

    def get_metadata(self):
        data = {}
        for x in range(1, self.maximum_databases):
            a_db = redis.Redis(host=self.server, port=self.port, db=x)
            if b'dataset_id' in a_db.keys():
                data[a_db.get('dataset_id').decode('utf-8')] = dict(db=x, lastLoaded=a_db.get(
                    'lastLoaded').decode('utf-8'))
        return data

    def get_first_free_db(self):
        for x in range(1, self.maximum_databases):
            a_db = redis.Redis(host=self.server, port=self.port, db=x)
            if b'dataset_id' not in a_db.keys():
                return x
        return -1

    def flush_all_dbs(self):
        self.my_redis_db = redis.Redis(host=self.server, port=self.port, db=self.db_number)
        self.my_redis_db.flushall()

    def get_dataset_db(self):
        for x in range(1, self.maximum_databases):
            a_db = redis.Redis(host=self.server, port=self.port, db=x)
            if b'dataset_id' in a_db.keys() and a_db.get('dataset_id').decode('utf-8') == str(self.dataset_id):
                return x
        return -1

    def delete_db(self):
        self.my_redis_db.flushdb()

    # use list to exceed Redis string 512MB size limit
    def save_list(self, key, value):
        self.my_redis_db.delete(key)
        for i in range(0, len(value), self.chunkLength):
            self.my_redis_db.rpush(key, value[i:i + self.chunkLength])

    def get_list(self, key):
        blist = self.my_redis_db.lrange(key, 0, -1)
        value = ''
        for chunk in blist:
            value = value + chunk.decode('utf-8')
        return value

    def exists(self, key):
        return self.my_redis_db.exists(key)

    # shared data like broadcastweeks in db=0
    def set_shared(self, key, value):
        self.my_redis_db = redis.Redis(host=self.server, port=self.port, db=0)
        self.set(key, value)
        self.my_redis_db = redis.Redis(host=self.server, port=self.port, db=self.db_number)

    def get_shared_df(self, key):
        self.my_redis_db = redis.Redis(host=self.server, port=self.port, db=0)
        result = None
        if self.exists(key):
            result = self.get_df(key)
        self.my_redis_db = redis.Redis(host=self.server, port=self.port, db=self.db_number)
        return result
