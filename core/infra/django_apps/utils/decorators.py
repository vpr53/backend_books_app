import json
from ninja_jwt.tokens import AccessToken

from functools import wraps

def authorized(user_attr="user1"):
    def decorator(test_func):
        @wraps(test_func)
        def wrapper(self, *args, **kwargs):
            user = getattr(self, user_attr)
            token = AccessToken.for_user(user)
            self.client.defaults["HTTP_AUTHORIZATION"]= f"Bearer {token}"

            original_post = self.client.post
            original_put = self.client.put
            original_patch = self.client.patch

            def json_method(method, url, data=None, **kw):
                return method(url, data=json.dumps(data), content_type="application/json", **kw)

            self.client.post = lambda url, data=None, **kw: json_method(original_post, url, data, **kw)
            self.client.put = lambda url, data=None, **kw: json_method(original_put, url, data, **kw)
            self.client.patch = lambda url, data=None, **kw: json_method(original_patch, url, data, **kw)

            return test_func(self, *args, **kwargs)

        return wrapper
    return decorator


