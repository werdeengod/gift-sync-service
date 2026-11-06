from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str

    RABBITMQ_HOST: str
    RABBITMQ_PORT: str
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    TELEGRAM_SESSION_STRING: str
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    PHONE: str

    DEBUG: bool

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def broker_url(self):
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"

    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')


config = Settings()
