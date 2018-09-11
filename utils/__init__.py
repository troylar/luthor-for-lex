import json


class DictUtils:
    @staticmethod
    def are_same(dict1, dict2):
        d1 = json.dumps(dict1, sort_keys=True, indent=2)
        d2 = json.dumps(dict2, sort_keys=True, indent=2)
        return d1 == d2
