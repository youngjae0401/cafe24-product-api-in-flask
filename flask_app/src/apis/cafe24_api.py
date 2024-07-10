from config import CAFE24_CONFIG
from src.utils.logger import logger
from src.models.log import Log
from src.models.cafe24_authorization import Cafe24Authorization
from datetime import datetime
import base64, json, requests

class Cafe24API:
    def __init__(self):
        self.rest_api_url = CAFE24_CONFIG['rest_api_url']
        self.client_id = CAFE24_CONFIG['client_id']
        self.client_secret_key = CAFE24_CONFIG['client_secret_key']
        self.code = CAFE24_CONFIG['code']
        self.redirect_uri = CAFE24_CONFIG['redirect_uri']
        self.version = CAFE24_CONFIG['version']

    def call_api(self, method, endpoint, data=None, json=None, params=None, headers=None):
        url = self.rest_api_url + endpoint

        try:
            response = requests.request(method, url, headers=headers, data=data, json=json, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"API call failed: {e}")
            Log.save("ERROR", f"API call failed: {e}")
            raise

        Log.save("INFO", f"API call: method={method}, url={url}, data={data}, json={json}, params={params}, status_code={response.status_code}, response={response.text}")

        return response.text

    def get_auth(self, data):
        auth_string = f"{self.client_id}:{self.client_secret_key}"
        auth_base64 = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

        headers = {
            "Authorization": f"Basic {auth_base64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        return self.call_api("POST", "/oauth/token", data=data, headers=headers)

    def get_access_token(self):
        try:
            token_data = Cafe24Authorization.find_one()

            if token_data:
                current_time = datetime.now()
                expires_at = token_data['expires_at']
                refresh_token_expires_at = token_data['refresh_token_expires_at']

                if expires_at > current_time: # Access Token이 유효한 경우
                    return token_data['access_token']
                elif refresh_token_expires_at > current_time: # Refresh Token이 유효한 경우
                    data = {
                        "grant_type": "refresh_token",
                        "refresh_token": token_data['refresh_token']
                    }

                    return self.__save_and_return_access_token(data)

            # 토큰 정보가 없을 경우
            data = {
                "grant_type": "authorization_code",
                "code": self.code,
                "redirect_uri": self.redirect_uri
            }

            return self.__save_and_return_access_token(data)
        except Exception as e:
            logger.error(f"Failed to get access token: {e}")
            Log.save("ERROR", f"Failed to get access token: {e}")
            raise

    def find_product(self, product_no):
        return self.call_api("GET", f"/admin/products/{product_no}", headers=self.__get_headers())

    def find_products(self, params=None):
        return self.call_api("GET", "/admin/products", params=params, headers=self.__get_headers())

    def find_product_variants(self, product_no):
        return self.call_api("GET", f"/admin/products/{product_no}/variants", headers=self.__get_headers())

    def find_product_variant(self, product_no, variant_code):
        return self.call_api("GET", f"/admin/products/{product_no}/variants/{variant_code}", headers=self.__get_headers())

    def find_product_count(self):
        return self.call_api("GET", "/admin/products/count", headers=self.__get_headers())

    def update_product(self, product_no, request_data):
        return self.call_api("PUT", f"/admin/products/{product_no}", json={"request": request_data}, headers=self.__get_headers())

    def update_product_variants(self, product_no, request_data):
        return self.call_api("PUT", f"/admin/products/{product_no}/variants", json={"request": request_data}, headers=self.__get_headers())

    def update_product_variant(self, product_no, variant_code, request_data):
        return self.call_api("PUT", f"/admin/products/{product_no}/variants/{variant_code}", json={"request": request_data}, headers=self.__get_headers())

    def delete_product(self, product_no):
        return self.call_api("DELETE", f"/admin/products/{product_no}", headers=self.__get_headers())

    def __get_headers(self):
        access_token = self.get_access_token()

        return {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "X-Cafe24-Api-Version": self.version
        }

    def __save_and_return_access_token(self, data):
        cafe24_token = self.get_auth(data=data)
        token_dict = json.loads(cafe24_token)
        Cafe24Authorization.save(token_dict)

        return token_dict['access_token']
