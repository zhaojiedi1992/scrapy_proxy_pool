from environs import Env

env = Env()
env.read_env()

# Redis setttings
REDIS_HOST = env.str("REDIS_HOST", "127.0.0.1")
REDIS_PORT = env.str("REDIS_PORT", "6379")
REDIS_DB = env.str("REDIS_DB", "0")
REDIS_PASSWORD = env.str("REDIS_PASSWORD", "zhaojiedi")
REDIS_KEY_PREFIX = env.str("REDIS_KEY_PREFIX", "proxy:scrapy")
REDIS_STORAGE_LIMIT = env.int("REDIS_STORAGE_LIMIT", 5000)

# define proxy scores
PROXY_SCORE_MAX = env.int('PROXY_SCORE_MAX', 100)
PROXY_SCORE_MIN = env.int('PROXY_SCORE_MIN', 8)
PROXY_SCORE_INIT = env.int('PROXY_SCORE_INIT', 10)

# crawler settings
CRAWL_TIMEOUT = env.int("CRAWL_TIMEOUT", 10)

# tester settings
TEST_BATCH_COUNT = env.int("TEST_BATCH_COUNT", 100)
TEST_URL = env.str('TEST_URL', 'http://www.baidu.com')
TEST_TIMEOUT = env.int('TEST_TIMEOUT', 10)
# only save anonymous proxy
TEST_ANONYMOUS = env.bool('TEST_ANONYMOUS', True)
# TEST_HEADERS = env.json('TEST_HEADERS', {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
# })
TEST_VALID_STATUS = env.list('TEST_VALID_STATUS', [200, 206, 302])
# whether to set max score when one proxy is tested valid
TEST_DONT_SET_MAX_SCORE = env.bool('TEST_DONT_SET_MAX_SCORE', False)

# server settings
SERVER_HOST = env.str('SERVER_HOST', '127.0.0.1')
SERVER_PORT = env.int('SERVER_PORT', 8001)
SERVER_THREAD = env.int('SERVER_THREAD', 10)

#engine settings
ENABLE_TESTER = env.bool('ENABLE_TESTER', True)
ENABLE_GETTER = env.bool('ENABLE_GETTER', True)
ENABLE_SERVER = env.bool('ENABLE_SERVER', True)
ENGINE_CYCLE_GETTER = env.int('ENGINE_CYCLE_GETTER', 10)
ENGINE_CYCLE_TESTER =env.int('ENGINE_CYCLE_TESTER',10)