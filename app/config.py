from decouple import config

class Config:
    SECRET_KEY=config('SECRET_KEY')
    PGSQL_HOST=config('PGSQL_HOST')
    PGSQL_USER=config('PGSQL_USER')
    PGSQL_PASSWORD=config('PGSQL_PASSWORD')
    PGSQL_DATABASE=config('PGSQL_DATABASE')
    
class DevelopmentConfig(Config):
    DEBUG=True

config={
    'development': DevelopmentConfig
}