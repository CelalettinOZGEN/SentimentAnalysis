from dbManager import dbManager
from fileManager import fileManager
from control import Control
import xlrd


class App:
    def __init__(self):
        self.dM = dbManager
        self.fM = fileManager
        self.cM = Control()
  
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
            
            elif input_enterance == 'x' or input_enterance == 'X':
                break
            
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

        comment_list = []
        while comment_size > 0:
            comment = input("Yorum Giriniz: ")

            comment_list.append(comment)
            
            comment_size -= 1

            if comment_size == 0:
                self.cM.listSend(self.user_name, comment_list)

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
                xlsx_list = []
                for col_index in range(sheet.ncols):
                    for i in range(0, sheet.nrows):
                        excel_comment = sheet.cell(i, col_index).value

                        xlsx_list.append(excel_comment)

                self.cM.listSend(self.user_name, xlsx_list)

        except FileNotFoundError:
            print("Dosya Bulunamadı")
            print('\n')

    def viewDb(self, key, value):
        d = self.dM()

        result = d.importComment(self.user_name, key, value)

        print(f"'{self.user_name}' kullanıcısının '{key}' anahtarındaki '{value}' yorumları: \n")
        for i in result:
            print(100 * '-')
            print(f"|Kullanıcı Adı: {i['user']} | Yorum: {i['comment']} | Rate: {i['rate']} | Analiz: {i['analysis']}|")
        
        print(100 * '-')
        print('\n')
         
App().userMenu()