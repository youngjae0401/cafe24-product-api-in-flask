# 코드 호출 URL
# 토큰발급 요청시 사용된 code는 재사용할 수 없으며 코드 발급 후 1분이 경과하면 만료됩니다.
# https://{mall_id}.cafe24api.com/api/v2/oauth/authorize?response_type=code&client_id={client_id}&state={state}&redirect_uri={redirect_uri}&scope={scope}
CAFE24_CONFIG = {
    'rest_api_url': 'https://{mall_id}.cafe24api.com/api/v2',
    'client_id': '', # client_id
    'client_secret_key': '', # client_secret_key
    'code': '', # 위 주석에 달린 URL을 통해 발급 받은 코드
    'redirect_uri': '', # 카페24에서 설정한 redirect_uri
    'version': '' # API 버전 (ex.2024-06-01)
}

DB_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': 'root',
    'database': 'my_db'
}
