import os

# 코드 호출 URL
# 토큰발급 요청시 사용된 code는 재사용할 수 없으며 코드 발급 후 1분이 경과하면 만료됩니다.
# https://{mall_id}.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={redirect_uri}&scope={scope}
CAFE24_CONFIG = {
    'rest_api_url': os.getenv('CAFE24_REST_API_URI'),
    'client_id': os.getenv('CAFE24_CLIENT_ID'),
    'client_secret_key': os.getenv('CAFE24_CLIENT_SECRET_KEY'),
    'code': os.getenv('CAFE24_CODE'),
    'redirect_uri': os.getenv('CAFE24_REDIRECT_URI'),
    'version': os.getenv('CAFE24_VERSION'),
    'shop_no': os.getenv('CAFE24_SHOP_NO')
}

DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST'),
    'user': os.getenv('DATABASE_USER'),
    'password': os.getenv('DATABASE_PASSWORD'),
    'database': os.getenv('DATABASE_NAME')
}
