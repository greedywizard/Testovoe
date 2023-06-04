import json


class RestoreData:
    def __init__(self):
        self.seed_phrase = None

    def FromJson(self, json_string):
        json_dict = json.loads(json_string)
        for i in vars(self):
            self.__setattr__(i, json_dict[i])
        return self


a = RestoreData().FromJson('{"seed_phrase":"milk craft duck galaxy occur copy rich drastic also wise hair project"}')
print(a.seed_phrase)
