from dbManager import dbManager
from fileManager import fileManager
import xlrd

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
        while comment_size > 0:
            comment = input("Yorum Giriniz: ")
            commnet_dict = {}
            commnet_dict['user'] = self.user_name
            commnet_dict['comment'] = comment

            comment_list.append(commnet_dict)
            
            comment_size -= 1

            if comment_size == 0:

                add_msg = "d- Database'e kaydet\nj- JSON'a kaydet\nl- Exel'e kaydet"
                d = self.dM()

                while True:
                    print(add_msg)
                    choose_add = input("Eklemek İstediğiniz Alanı Seçiniz: ")

                    if choose_add == "d":
                        print(comment_list)     
                        d.addComment(comment_list)
                        break

                    elif choose_add == "j":
                        print(comment_list) 
                        file_name = input("JSON Dosyasını Giriniz: ")
                        file_name = file_name + '.json'
                        
                        f = self.fM(file_name)
                        f.addJson(comment_list)
                        break

                    else:
                        break
    
    def viewJson(self):
        file_name = input("Dosyanızın Adını Giriniz: ")

        f = self.fM(file_name)
        result = f.viewJson()

        for i in result:
            print(i)
    
    def importDb(self):
        d = self.dM()
        msg = "1- Kullanıcıya Göre\n2- Yoruma Göre"
        while True:
            import_msg = input("Aramak İstediğiniz Alanı Seçeniz: ")

            if import_msg == 'u':
                result = d.importComment(self.user_name, 'user', self.user_name)

                for i in result:
                    print(f"Kullanıcı Adı: {i['user']} | Yorum: {i['comment']}")
                break
            
            elif import_msg == 'c':
                comment_msg = input("Aramak İstediğiniz Yorumu Yazınız: ")
                result = d.importComment(self.user_name, 'comment', 'iyi')

                for i in result:
                    print(f"Kullanıcı Adı: {i['user']} | Yorum: {i['comment']}")

            else:
                break
    
    def importExcel(self):
        exel_file = input("Dosya Adınızı Giriniz: ")
        loc = exel_file
        wb = xlrd.open_workbook(loc) 
        sheet = wb.sheet_by_index(0)

        liste = []
        for col_index in range(sheet.ncols):
            for i in range(0, sheet.nrows):
                excel_comment = sheet.cell(i, col_index).value
                
                my_dict = {}
                my_dict['user'] = self.user_name
                my_dict['comment'] = excel_comment

                liste.append(my_dict)
        
        print(liste)
        d = self.dM()
        d.addComment(liste)
        


App().userMenu()