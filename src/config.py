class Config:
    secret_key = "DHLForms|DHL2023"

class Developmentconfig(Config):
    DEBUG = True

config ={
    'development' : Developmentconfig
}