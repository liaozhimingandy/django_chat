
# 单例
class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self.uniqueInstance = None

    def __call__(self,  *args, **kwargs):
        if self.uniqueInstance is None:
            self.uniqueInstance = self._cls(*args, **kwargs)
        return self.uniqueInstance

