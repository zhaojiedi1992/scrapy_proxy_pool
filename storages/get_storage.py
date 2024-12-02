import settings
from storages.redis_storage import RedisStorage
from storages.sqllite_storage import SQLiteStorage

DEFAULT_STORAGE_CLASS = None
print(settings.USE_DB)
if settings.USE_DB == "REDIS":
    DEFAULT_STORAGE_CLASS = RedisStorage
elif settings.USE_DB == "SQLITE":
    DEFAULT_STORAGE_CLASS = SQLiteStorage

print(DEFAULT_STORAGE_CLASS)