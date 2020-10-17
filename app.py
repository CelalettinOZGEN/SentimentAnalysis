from dbManager import dbManager
from fileManager import fileManager
import xlrd

from Sentiment import tokens_to_string, tokenizer, pad_sequences, max_tokens
from tensorflow.python.keras.models import load_model


class App:
    def __init__(self):
        self.dM = dbManager
        self.fM = fileManager
    
    def userMenu(self):
        msg = "e- Giriş Yap\nr- Kayıt Ol"

        while True:
            print(msg)
            input_enterance = input("Bir İşlem Seçiniz: ")
            if input_enterance == 'e':
                self.user_login()
            elif input_enterance == 'r':
                self.user_register()
            else:
                break
    
    def user_login(self):
        hak = 3
        while hak > 0:
            user_name = input("Kullanıcı Adınız: ")
            user_password = input("Kullanıcı Şifreniz: ")

            d = self.dM()
            result = d.loginControl(user_name, user_password)

            if result:
                self.menu(user_name)
                break
        
            else:
                print("Hatalı Kullanıcı Adı veya Parolası.")
                hak -= 1

                if hak == 0:
                    self.user_register()

    def user_register(self):
        while True:
            user_name = input("Kullanıcı Adınız: ")
            user_password = input("Kullanıcı Şifreniz: ")

            d = self.dM()
            result = d.registerControl(user_name)
            
            if result:
                print(f"'{user_name}' Kullanıcı Adı Mevcuttur. Lütfen Tekrar Deneyiniz")
            
            else:
                user_dict = {}
                user_dict['name'] = user_name
                user_dict['password'] = user_password

                d.addUser(user_dict)

                print("Kullanıcınız Oluşturulmuştur")
                break
            

    def menu(self, user_name):
        self.user_name = user_name
        first_msg = "1- Yorum Ekle\n2- JSON'daki Verileri Gözlemle\n3- Database'deki Verileri Gözlemle\n4- Excel Dosyası İçerisindeki Verilerin Analizi"

        while True:
            print(first_msg)
            input_msg = input("Menüden Bir İşlem Seçiniz: ")

            if input_msg == '1':
                self.addComment()
            
            elif input_msg == '2':
                self.viewJson()
            
            elif input_msg == '3':
                self.importDb()

            elif input_msg == '4':
                self.importExcel()

            else:
                break
    
    def addComment(self):
        comment_size = int(input("Kaç Yorum Girilecek: "))

        comment_list = []
        excel_list = []
        while comment_size > 0:
            comment = input("Yorum Giriniz: ")

            commnet_dict = self.sentimentAnalysis(comment)

            comment_list.append(commnet_dict)
            #excel_list.append([self.user_name, comment, float(sentiment), analysis])
            
            comment_size -= 1

            if comment_size == 0:
                self.innerMenu(comment_list,excel_list)
 
    def viewJson(self):
        file_name = input("Dosyanızın Adını Giriniz: ")

        f = self.fM(file_name)
        result = f.viewJson()

        for i in result:
            print(i)
    
    def importDb(self):
        find_choose = "u- Kullanıcıya Göre Ara\nc- Yoruma Göre Ara"

        while True:
            print(find_choose)
            import_msg = input("Aramak İstediğiniz Alanı Seçeniz: ")

            if import_msg == 'u':
                self.viewDb('user', self.user_name)
                break
            
            elif import_msg == 'c':
                comment_msg = input("Aramak İstediğiniz Yorumu Yazınız: ")
                self.viewDb('comment', comment_msg)
                break
            #sentiment sonucuna göre gelecek...

            else:
                break
    
    def importExcel(self):
        exel_file = input("Dosya Adınızı Giriniz [*xlsx]: ")

        if '.xlsx' in exel_file:
            loc = exel_file

        else:
            loc = exel_file + '.xlsx'

        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)

        if '.xlsx' in loc:
            db_list = []
            excel_list = []
            for col_index in range(sheet.ncols):
                for i in range(0, sheet.nrows):
                    excel_comment = sheet.cell(i, col_index).value
                    
                    my_dict = {}
                    my_dict['user'] = self.user_name
                    my_dict['comment'] = excel_comment

                    db_list.append(my_dict)
                    excel_list.append([self.user_name, excel_comment])
            
            print(db_list)
            self.innerMenu(db_list, excel_list)
        
        else:
            print("Geçersiz Dosya Türü!")
    
    def exportExcel(self, excel_list):

        file_name = input("Dosya Adını Giriniz [*xls]: ")
        if '.xls' in file_name:
            file_name = file_name
        else:
            file_name = file_name + '.xls'

        table_data = [['User', 'Comment', 'Rate', 'Sentiment']]
        
        for i in excel_list:
            table_data.append(i)
        
        f = self.fM(file_name)
        f.exportExcel(self.user_name, table_data)

        print(f"Veriler '{file_name}' Dosyasına Kaydedildi")
    
    def addDb(self, db_list):
        d = self.dM()
        d.addComment(db_list)
        print("Veriler Database'e Aktarıldı")
    
    def addJson(self, json_list):
        file_name = input("JSON Dosyasını Giriniz [*json]: ")

        if '.json' in file_name:
            file_name = file_name

        else:
            file_name = file_name + '.json'
                        
        f = self.fM(file_name)
        f.addJson(json_list)
        print(f"Veriler '{file_name}' Dosyasına Kaydedildi")

        self.addDb(json_list)
    
    def viewDb(self, key, value):
        d = self.dM()

        result = d.importComment(self.user_name, key, value)

        print(f"'{self.user_name}' kullanıcısının '{key}' anahtarındaki '{value}' yorumları: \n")
        for i in result:
            print(f"Kullanıcı Adı: {i['user']} | Yorum: {i['comment']}")

    def innerMenu(self, db_list, excel_list):
        import_msg = "j- JSON'a Kaydet\nl- Excel'e Kaydet\nt- JSON ve Excel'e Kaydet"

        while True:
            print(import_msg)
            choose_import = input("Eklemek İstediğiniz Dosya Türünü Seçiniz: ")

            if choose_import == 'j':
                self.addJson(db_list)
                break
                
            elif choose_import == 'l':
                self.exportExcel(excel_list)
                self.addDb(db_list)
                break

            elif choose_import == 't':
                self.addJson(db_list)
                self.exportExcel(excel_list)
                break
                
            elif choose_import == 'x':       
                break
    
    def sentimentAnalysis(self, comment):
        model = load_model('model.h5')
        texts=[comment]
        tokens = tokenizer.texts_to_sequences(texts)
        tokens_pad = pad_sequences(tokens, maxlen=max_tokens)
        sentiment = model.predict(tokens_pad)

        if (sentiment>=0.85):
            analysis = "Pozitif"
        elif (0.40 <= sentiment < 0.85):
            analysis = "Nötr"
        else:
            analysis = "Negatif"
                
            
        commnet_dict = {}
        commnet_dict['user'] = self.user_name
        commnet_dict['comment'] = comment
        commnet_dict['rate'] = float(sentiment)
        commnet_dict['analysis'] = analysis

        return commnet_dict

        
App().userMenu()