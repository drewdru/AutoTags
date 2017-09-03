DATABASES = {
    'sqlalchemy': {
        'drivername': 'DRIVERNAME',
        'host': 'HOST',
        'port': 'PORT',
        'username': 'USERNAME',
        'password': 'PASSWORD',
        'database': 'DATABASE'
    },
}

VK = {
    'app_id': 'APP_ID',
    'user_login': 'USER_LOGIN', 
    'user_password': 'USER_PASSWORD', 
    'scope': 'photos, wall, groups, offline',
    'owner_id': 'OWNER_ID',
    'isResume': True,
    'resumeAlbumID': 49782714,
}

try:     
    from .local_settings import *
except Exception:
    try:
        from local_settings import *
    except ImportError:
        pass
