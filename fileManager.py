import json5

class fileManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def addJson(self, comment_list):
        with open(self.file_name, 'w', encoding= 'utf-8') as writejson:
            result = json5.dump(comment_list, writejson)

    def viewJson(self):
        with open(self.file_name, 'r', encoding= 'utf-8') as readjson:
            result = json5.load(readjson)
            return result



# f = fileManager("deneme.json")
# comment_list = [{'comment': 'iyi'}, {'comment': 'kötü'}]
# f.addJson(comment_list)