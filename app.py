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
        msg = "| e- Giriş Yap\n| r- Kayıt Ol\n| x-Çıkış"

        while True:
            print(msg)
            input_enterance = input("Bir İşlem Seçiniz: ")
            if input_enterance == 'e' or input_enterance == 'E':
                self.user_login()

            elif input_enterance == 'r' or input_enterance == 'R':
                self.user_register()
            
            else:
                print("!!! Geçersiz Tıklama")
                print('\n')
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
        first_msg = "| 1- Yorum Ekle\n| 2- JSON'daki Verileri Gözlemle\n| 3- Database'deki Verileri Gözlemle\n| 4- Excel Dosyası İçerisindeki Verilerin Analizi\n| x- Çıkış"

        
        while True:
            print(first_msg)
            print(100 * '-')
            input_msg = input("Menüden Bir İşlem Seçiniz: ")

            if input_msg == '1':
                self.addComment()
            
            elif input_msg == '2':
                self.viewJson()
            
            elif input_msg == '3':
                self.importDb()

            elif input_msg == '4':
                self.importExcel()

            elif input_msg == 'x' or input_msg == 'X':
                break
            
            else:
                print("!!! Geçersiz Tıklama")
                print('\n')
    
    def addComment(self):
        print('\n')
        print(100 * '-')
        comment_size = int(input("Kaç Yorum Girilecek: "))
        print(100 * '*')
        liste = []
        while comment_size > 0:
            comment = input("Yorum Giriniz: ")

            liste.append(comment)
            
            comment_size -= 1

            if comment_size == 0:
                self.denemeFunc(liste)
        print(100 * '*')
                                       
    def viewJson(self):
        print('\n')
        print(100 * '-')
        file_name = input("Dosyanızın Adını Giriniz: ")
        print(100 * '-')

        if '.json' in file_name:
            file_name = file_name
        
        else:
            file_name = file_name + '.json'

        try: 
            f = self.fM(file_name)
            result = f.viewJson()

            print('\n')
            print(f"'{file_name}' Dosyası İçerisindeki Veriler: ")
            for i in result:
                print(100 * '-')
                print(f"|{i['comment']} | {i['rate']} | {i['analysis']}|")
            print(100 * '-')
            print('\n')

        except FileNotFoundError or FileExistsError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')
    
    def importDb(self):
        print('\n')
        print(100 * '-')
        find_choose = "| u- Kullanıcıya Göre Ara\n| c- Yoruma Göre Ara\n| s- Duygu Analizine Göre\n| x- Çıkış"

        while True:
            print(find_choose)
            print(100 * '-')
            import_msg = input("Aramak İstediğiniz Alanı Seçeniz: ")

            if import_msg == 'u' or import_msg == 'U':
                self.viewDb('user', self.user_name)
                break
            
            elif import_msg == 'c' or import_msg == 'C':
                print(100 * '-')
                comment_msg = input("Aramak İstediğiniz Yorumu Yazınız: ")
                print(100 * '-')
                self.viewDb('comment', comment_msg)
                break
            
            elif import_msg == 's' or import_msg == 'S':
                print(100 * '-')
                print("p- Pozitif\nn- Negatif\nr- Nötr")
                print(100 * '-')
                inner_input = input("Aramak İstediğiniz Duygu Analizi Sonucunu Giriniz: ")
                print(100 * '-')

                if inner_input == "p" or inner_input == "P":
                    self.viewDb('analysis', "Pozitif")
                elif inner_input == "n":
                    self.viewDb('analysis', "Negatif")
                elif inner_input == "r":
                    self.viewDb('analysis', "Nötr")
                break

            elif import_msg == 'x' or import_msg == 'X':
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')
    
    def importExcel(self):
        print(100 * '-')
        exel_file = input("Dosya Adınızı Giriniz [*xlsx]: ")
        print(100 * '-')

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
            print('\n')
    
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
            print(100 * '-')
        except FileNotFoundError or FileExistsError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')
    
    def addDb(self, db_list):
        d = self.dM()
        d.addComment(db_list)
        print(100 * '-')
        print("** Veriler Database'e Aktarıldı")
        print('\n')
    
    def addJson(self, json_list):
        file_name = input("JSON Dosyasını Giriniz [*json]: ")

        if '.json' in file_name:
            file_name = file_name

        else:
            file_name = file_name + '.json'

        try:              
            f = self.fM(file_name)
            f.addJson(json_list)
            print(f"** Veriler '{file_name}' Dosyasına Kaydedildi")
            print('\n')

        except FileNotFoundError or FileExistsError:
            print(100 * '-')
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')

        self.addDb(json_list)
    
    def viewDb(self, key, value):
        d = self.dM()

        result = d.importComment(self.user_name, key, value)

        print(f"'{self.user_name}' kullanıcısının '{key}' anahtarındaki '{value}' yorumları: \n")
        for i in result:
            print(100 * '-')
            print(f"|Kullanıcı Adı: {i['user']} | Yorum: {i['comment']} | Rate: {i['rate']} | Analiz: {i['analysis']}|")
        
        print(100 * '-')
        print('\n')

    def innerMenu(self, db_list, excel_list):
        print(100 * '-')
        print("** Verileriniz Analiz Edilmiştir. Lütfen Aşağıdaki Menüden Bir İşlem Seçiniz")
        import_msg = "| j- JSON'a Kaydet\n| l- Excel'e Kaydet\n| t- JSON ve Excel'e Kaydet\n |x- Çıkış"

        while True:
            print(import_msg)
            print(100 * '-')
            choose_import = input("Eklemek İstediğiniz Dosya Türünü Seçiniz: ")
            print(100 * '-')

            if choose_import == 'j' or choose_import == 'J':
                self.addJson(db_list)
                break
                
            elif choose_import == 'l' or choose_import == 'L':
                self.exportExcel(excel_list)
                self.addDb(db_list)
                break

            elif choose_import == 't' or choose_import == 'T':
                self.addJson(db_list)
                self.exportExcel(excel_list)
                break
                
            elif choose_import == 'x' or choose_import == 'X':       
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')
    
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