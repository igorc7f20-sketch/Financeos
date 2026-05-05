from .base import *

DEBUG = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOWED_CREDENTIALS = True

#─── production.py ───────────────────────────────────────────────────────────
# backend/config/settings/production.py

# from .base import *
# from decouple import config
#
# DEBUG = False
#
# CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default="").split(",")
#
# SECURE_HSTS_SECONDS = 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True