import os

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Configuration
    DATA_GOV_URL = os.environ.get('DATA_GOV_URL') or 'https://api.data.gov.in/resource/<RESOURCE_ID>'
    DATA_GOV_API_KEY = os.environ.get('DATA_GOV_API_KEY')
    
    # Cache Configuration
    CACHE_EXPIRY_HOURS = int(os.environ.get('CACHE_EXPIRY_HOURS', 24))
    MAX_CACHE_RECORDS = int(os.environ.get('MAX_CACHE_RECORDS', 12))
    
    # Database
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'mgnrega_cache.db'
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Use PostgreSQL in production if available
    DATABASE_URL = os.environ.get('DATABASE_URL')

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_PATH = ':memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
