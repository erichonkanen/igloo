from pyramid.session import JSONSerializer
from pyramid.session import PickleSerializer


class Serializer(object):
    def __init__(self):
        self.json = JSONSerializer()
        self.pickle = PickleSerializer()

    def dumps(self, value):
        # maybe catch serialization errors here and keep using pickle
        # while finding spots in your app that are not storing
        # JSON-serializable objects, falling back to pickle
        return self.json.dumps(value)

    def loads(self, value):
        try:
            return self.json.loads(value)
        except ValueError:
            return self.pickle.loads(value)
