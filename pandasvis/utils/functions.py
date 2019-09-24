
class AutoDictionary(dict):
    """A dictionary easy to populate not-defined keys"""
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value
