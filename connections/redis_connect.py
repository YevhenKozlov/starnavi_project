import redis

from core.configs_wrapper import RedisConfig


class RedisConnect:
    """
    Class 'RedisConnect'
    Singleton, connection to Redis
    """

    def __new__(cls):

        if not hasattr(cls, 'instance'):
            cls.instance = super(RedisConnect, cls).__new__(cls)

            config = RedisConfig()

            cls.connection = redis.Redis(
                password=config.password,
                host=config.host,
                port=int(config.port),
                db=int(config.db)
            )

        return cls.instance
