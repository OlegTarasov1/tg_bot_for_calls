from pydantic_settings import BaseSettings


class RedisEnv(BaseSettings):
    REDIS_PORT: int
    REDIS_HOST: str
    REDIS_V_DB: int

    redis_url: str | None = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redis_url = "redis://{}:{}/{}".format(
           self.REDIS_HOST,
           self.REDIS_PORT,
           self.REDIS_V_DB 
        )


    class Config:
        env_file = None
        env_file_encoding = "utf-8"
        extra = "ignore"
