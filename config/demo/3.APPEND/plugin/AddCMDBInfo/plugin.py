class Plugin(object):

    def __init__(self):
        self.name = None
        self.type = None
        self.log = None
        self.redis = None

    def plugin_exec(self, arg, config):
        # arg is ip address
        # todo: api for ip to cmdb info
        result = dict()
        result["flag"] = True
        result["msg"] = dict()
        result["msg"]["agents"] = []
        result["msg"]["created"] = "1629184394"
        result["msg"]["created"] = "1629184394"
        result["msg"]["id"] = "6199eb9759a968c945ebbeae"
        result["msg"]["ipv4"] = "10.74.31.69"
        result["msg"]["ipv6"] = "fd00:0000:ff:1:1:74:31:69"
        result["msg"]["services"] = dict()
        result["msg"]["services"]["department"] = "Data"
        result["msg"]["services"]["description"] = ""
        result["msg"]["services"]["level_tag"] = ""
        result["msg"]["services"]["name"] = "Data"
        result["msg"]["services"]["owner"] = "admin"

        return result

