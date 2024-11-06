from sqlalchemy.pool import QueuePool

POOL_CONFIG = {
    'poolclass': QueuePool,
    'pool_size': 5,
    'max_overflow': 10,
    'pool_pre_ping': True,
    'pool_recycle': 3600,
} 