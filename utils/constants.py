ACCESS_TOKEN_EXPIRE_MINUTES = 12 * 60  # 12 hours
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = 'Example@Secret123'  # this should be an environ variable
JWT_REFRESH_SECRET_KEY = (
    'Example@Secret123'  # this should be an environ variable
)
