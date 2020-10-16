import json5
import xlwt

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
    
    def exportExcel(self, user_name, exel_list):
        wb = xlwt.Workbook()

        ws = wb.add_sheet("Sentiment Analysis of " + user_name)

        for row, row_value in enumerate(exel_list):
            for col, col_value in enumerate(row_value):
                ws.write(row, col, col_value)

        wb.save(self.file_name)



# f = fileManager("deneme.json")
# comment_list = [{'comment': 'iyi'}, {'comment': 'kötü'}]
# f.addJson(comment_list)