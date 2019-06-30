import uuid


USER_KEY = "uid"
TEN_YEARS = 60 * 60 * 24 * 365 * 10


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):  # 新版本中间件这样用，没看懂逻辑，参考自强学堂中间件
        """请求来执行这里"""
        uid = self.generate_uid(request)
        request.uid = uid

        """响应去执行这里"""
        response = self.get_response(request)  # 如果不执行get_response直接返回一个response，那就直接返回给浏览器了，后续中间件失效了
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid































