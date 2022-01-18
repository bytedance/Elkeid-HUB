import json
class Plugin(object):

    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None

    def plugin_exec(self, arg, config):
        file = open("/tmp/elkeid_action.txt","a+")
        file.write(json.dumps(arg, sort_keys=True, indent=4,separators=(', ', ': ')) + "\n")
        file.close()
        result = dict()
        result["done"] = True
        return result

