from pydantic_settings import BaseSettings
from pydantic import SecretStr
import sqlalchemy


class EnvData(BaseSettings):
    PG_HOST: str
    PG_USERNAME: str
    PG_EXTERNAL_PORT: int
    PG_PASSWORD: SecretStr
    PG_DB_NAME: str

    BOT_TOKEN: SecretStr

    url: sqlalchemy.engine.URL | None = None
    
    class Config:
        env_file = None
        env_file_encoding = "utf-8"
        extra = "ignore"


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = self.__new_url_with_custom_name(self.PG_DB_NAME)


    def __new_url_with_custom_name(self, db_name):
        url = sqlalchemy.engine.URL.create(
            drivername="postgresql+psycopg",
            username=self.PG_USERNAME,
            password=self.PG_PASSWORD.get_secret_value(),
            host=self.PG_HOST,
            port=self.PG_EXTERNAL_PORT,
            database=db_name,
        )

        return url
