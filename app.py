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
        print(100 * '-')
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
        print('\n')
    
    def user_login(self):
        hak = 3
        print(100 * '-')
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
        print('\n')

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
        print(100 * '-')
        self.user_name = user_name
        print(f"Hoşgeldin {self.user_name}\n")
        first_msg = "1- Yorum Ekle\n2- JSON'daki Verileri Gözlemle\n3- Database'deki Verileri Gözlemle\n4- Excel Dosyası İçerisindeki Verilerin Analizi"

        
        while True:
            print(first_msg)
            print(100 * '#')
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
        print('\n')
        print(100 * '-')
        comment_size = int(input("Kaç Yorum Girilecek: "))

        liste = []
        while comment_size > 0:
            print(100 * '*')
            comment = input("Yorum Giriniz: ")

            liste.append(comment)
            
            comment_size -= 1

            if comment_size == 0:
                self.denemeFunc(liste)
                                       
    def viewJson(self):
        file_name = input("Dosyanızın Adını Giriniz: ")

        f = self.fM(file_name)
        result = f.viewJson()

        for i in result:
            print(i)
    
    def importDb(self):
        find_choose = "u- Kullanıcıya Göre Ara\nc- Yoruma Göre Ara\ns- Duygu Analizine Göre\nx- Çıkış"

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
            
            elif import_msg == 's':
                print("p- Pozitif\nn- Negatif\nr- Nötr")
                inner_input = input("Aramak İstediğiniz Duygu Analizi Sonucunu Giriniz: ")

                if inner_input == "p":
                    self.viewDb('analysis', "Pozitif")
                elif inner_input == "n":
                    self.viewDb('analysis', "Negatif")
                elif inner_input == "r":
                    self.viewDb('analysis', "Nötr")
                break

            elif import_msg == 'x':
                break
    
    def importExcel(self):
        exel_file = input("Dosya Adınızı Giriniz [*xlsx]: ")

        if '.xlsx' in exel_file:
            loc = exel_file

        else:
            loc = exel_file + '.xlsx'

        try:
            wb = xlrd.open_workbook(loc) 
            sheet = wb.sheet_by_index(0)

            if '.xlsx' in loc:
                
                liste = []
                for col_index in range(sheet.ncols):
                    for i in range(0, sheet.nrows):
                        excel_comment = sheet.cell(i, col_index).value

                        liste.append(excel_comment)

                self.denemeFunc(liste)
        except FileNotFoundError:
            print("Dosya Bulunamadı")
    
    def exportExcel(self, excel_list):

        file_name = input("Dosya Adını Giriniz [*xls]: ")
        if '.xls' in file_name:
            file_name = file_name
        else:
            file_name = file_name + '.xls'

        try:
            table_data = [['User', 'Comment', 'Rate', 'Sentiment']]
            
            for i in excel_list:
                table_data.append(i)
            
            f = self.fM(file_name)
            f.exportExcel(self.user_name, table_data)

            print(f"Veriler '{file_name}' Dosyasına Kaydedildi")
        except FileNotFoundError or FileExistsError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
    
    def addDb(self, db_list):
        d = self.dM()
        d.addComment(db_list)
        print('\n')
        print("Veriler Database'e Aktarıldı")
    
    def addJson(self, json_list):
        file_name = input("JSON Dosyasını Giriniz [*json]: ")

        if '.json' in file_name:
            file_name = file_name

        else:
            file_name = file_name + '.json'

        try:              
            f = self.fM(file_name)
            f.addJson(json_list)
            print('\n')
            print(f"Veriler '{file_name}' Dosyasına Kaydedildi")
        except FileNotFoundError or FileExistsError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")

        self.addDb(json_list)
    
    def viewDb(self, key, value):
        d = self.dM()

        result = d.importComment(self.user_name, key, value)

        print(f"'{self.user_name}' kullanıcısının '{key}' anahtarındaki '{value}' yorumları: \n")
        for i in result:
            print(f"Kullanıcı Adı: {i['user']} | Yorum: {i['comment']} | Rate: {i['rate']} | Analiz: {i['analysis']}")

    def innerMenu(self, db_list, excel_list):
        print(100 * '-')
        import_msg = "j- JSON'a Kaydet\nl- Excel'e Kaydet\nt- JSON ve Excel'e Kaydet\nx- Çıkış"

        while True:
            print(import_msg)
            print(100 * '#')
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
        my_list =[]

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
        
        my_list.append([float(sentiment), analysis])

        return my_list

    def jsonSend(self, my_list):

        comment_list = []
        for i in my_list:
            commnet_dict = {}
            commnet_dict['user'] = self.user_name
            commnet_dict['comment'] = i[0]
            commnet_dict['rate'] = i[1]
            commnet_dict['analysis'] = i[2]

            comment_list.append(commnet_dict)
        
        return comment_list

    def excelSend(self, my_list):

        excel_list = []
        for i in my_list:
            excel_list.append([self.user_name, i[0], i[1], i[2]])

        return excel_list
    
    def denemeFunc(self, liste):
        deneme_list = []
        for i in liste:
            deneme = self.sentimentAnalysis(i)

            for j in deneme:
                sentiment = j[0]
                analysis = j[1]

            deneme_list.append([i, sentiment, analysis])
        
        comment_list = self.jsonSend(deneme_list)
        excel_list = self.excelSend(deneme_list)
        self.innerMenu(comment_list, excel_list)
              
App().userMenu()