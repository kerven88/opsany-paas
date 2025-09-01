# -*- coding: utf-8 -*-
import requests
import settings
import json


class OpsAnyRbacUserAuth(object):
    APP_CODE = "rbac"
    APP_SECRET = settings.RBAC_APP_SECRET
    BK_URL = "{}://{}".format(settings.HTTP_SCHEMA, settings.PAAS_INNER_DOMAIN)
    ACCESS_TOKEN = "opsany-esb-auth-token-9e8083137204"

    def __init__(self, username="", password="", code="", app_id="", domain="", ad_domain="", sso_code="", sso_sign="", auth_type=""):
        self.username = username
        self.password = password
        self.code = code
        self.app_id = app_id
        self.domain = domain
        self.ad_domain = ad_domain
        self.sso_code = sso_code
        self.sso_sign = sso_sign
        self.auth_type = auth_type

    def check_users(self):
        API = "/api/c/compapi/rbac/user_auth/"
        url = self.BK_URL + API
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "username": self.username,
            "password": self.password,
            "code": self.code,
            "appid": self.app_id,
            "domain": self.domain,
            "ad_domain": self.ad_domain,
            "sso_code": self.sso_code,
            "sso_sign": self.sso_sign,
            "auth_type": self.auth_type,
        }
        res = requests.post(url, json=req, headers={"Cookie": "bk_token=None"}, verify=False)
        try:
            data = res.json().get("data")
        except Exception as e:
            return False, {"message": "Link Error."}
        if data:
            return data.get("auth_status"), data
        return False, {"message": "Auth Error."}

    def get_user_google_auth_status(self):
        API = "/api/c/compapi/rbac/get_user_google_auth_status/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "username": self.username,
            "auth_type": "login"
        }
        url = self.BK_URL + API
        response = requests.get(url, params=req, headers={"Cookie": "bk_token=None"}, verify=False)
        try:
            end_data = json.loads(response.text)
        except Exception as e:
            return 6
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return "6"

    def update_login_log(self, bk_token, address, user_agent, host_name, data=None):
        API = "/api/c/compapi/rbac/post_login_log/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "token": bk_token,
            "username": self.username,
            "address": address,
            "user_agent": user_agent,
            "host_name": host_name,
            "data": data if not data else {}
        }
        url = self.BK_URL + API
        response = requests.get(url, params=req, headers={"Cookie": "bk_token={}".format(bk_token)}, timeout=3, verify=False)
        try:
            end_data = json.loads(response.text)
        except Exception as e:
            return "Failed" 
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return "Failed"
        
    def get_google_auth(self):
        API = "/api/c/compapi/workbench/get_google_auth/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "username": self.username
        }
        URL = self.BK_URL + API
        response = requests.get(url=URL, params=req, headers={"Cookie": "bk_token=None"}, verify=False)
        try:
            end_data = json.loads(response.text)
        except Exception as e:
            return {}
        dt = {}
        if end_data.get("result"):
            end_data = end_data.get("data", {})
            return end_data
        return dt

    def bind_google_auth(self, secret, verify_code):
        API = "/api/c/compapi/workbench/bind_google_auth/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "username": self.username,
            "operator": self.username,
            "secret": secret,
            "verify_code": verify_code
        }
        url = self.BK_URL + API
        response = requests.post(url, data=req, headers={"Cookie": "bk_token=None"}, verify=False)
        end_data = json.loads(response.text)
        return end_data

    def check_google_verify_code(self, verify_code, seven_days_free=0):
        API = "/api/c/compapi/rbac/check_google_verify_code/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "username": self.username,
            "verify_code": verify_code,
            "seven_days_free": seven_days_free,
            "auth_type": "login"
        }
        url = self.BK_URL + API
        response = requests.post(url, data=req, headers={"Cookie": "bk_token=None"}, verify=False)
        end_data = json.loads(response.text)
        if end_data.get("result"):
            end_data = end_data.get("data")
            return end_data
        return False

    def get_vx_work_config(self, domain=""):
        API = "/api/c/compapi/rbac/get_wx_work_config/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "bk_username": "admin",
            "domain": domain
        }
        url = self.BK_URL + API
        response = requests.post(url, data=json.dumps(req), headers={"Cookie": "bk_token=None"}, verify=False)
        print("responseresponseresponse", response.content.decode())

        if 1:
            end_data = json.loads(response.text)
        #except Exception as e:
        #    return False, "Failed"
        if end_data.get("result"):
            end_data = end_data.get("data")
            return True, end_data
        return False, end_data.get("message")

    def get_auth_config(self, auth_type="", domain=""):
        API = "/api/c/compapi/rbac/get_auth_config/"
        req = {
            "bk_app_code": self.APP_CODE,
            "bk_app_secret": self.APP_SECRET,
            "bk_access_token": self.ACCESS_TOKEN,
            "auth_type": auth_type,
            "domain": domain
        }
        url = self.BK_URL + API
        response = requests.post(url, data=json.dumps(req), headers={"Cookie": "bk_token=None"}, verify=False)
        try:
            end_data = json.loads(response.text)
        except Exception as e:
            return True, []
        if end_data.get("result"):
            end_data = end_data.get("data")
            return True, end_data
        return False, end_data.get("message")


if __name__ == '__main__':
    api = OpsAnyRbacUserAuth("huxingqi").get_vx_work_config()
