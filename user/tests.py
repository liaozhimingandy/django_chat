from django.test import TestCase

from .lib.TokenUtil import TokenUtils


# Create your tests here.
class TokenUtilTest(TestCase):
    def test_token_create(self):
        """
        创建token
        """
        payload = {
            "appid": "8f7f81324dd740bc8649a2820bb70f90",
            "system_code": "ESB",
            "system_name": "集成平台",
            "software_provider_code": "91320191MA25QY6C6Y",
            "software_provider_name": "恺恩泰（南京）科技有限公司",
            "org_code": "1244030345576818XP",
            "org_name": "深圳市罗湖区人民医院"
        }
        token = TokenUtils.create_token(payload=payload, token_timeout=3600*24*7)
        print(token)
        self.assertEqual(token['expires_in'], 7200, '有效期不为7200')
