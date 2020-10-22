"""
DOCSTRING: Sentiment analiz uygulama ekranı.
"""
import xlrd
from dbManager import dbManager
from fileManager import fileManager
from control import Control



class App:
    """
    DOCSTRING: Uygulama yapısı ve menüler.
    """
    def __init__(self):
        self.db_manager = dbManager
        self.file_manager = fileManager
        self.control_manager = Control()
        self.user_name = 'Empty'
        self.file_name = 'Empty'

    def user_menu(self):
        """
        DOCSTRING: Kullanıcı Giriş Menüsü
        INPUT: e
        OUTPUT: username, password
        """
        print(100 * '-')
        msg = "| 1- Giriş Yap\n| 2- Kayıt Ol\n| 3-Çıkış"

        while True:
            print(msg)
            input_enterance = input("Bir İşlem Seçiniz: ")
            if input_enterance == '1':
                self.user_login()

            elif input_enterance == '2':
                self.user_register()

            elif input_enterance == '3':
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')
        print('\n')

    def user_login(self):
        """
        DOCSTRING: Kullanıcı Girişi
        INPUT: name = ozgen , password = 123
        OUTPUT: menu()
        """
        hak = 3
        print(100 * '-')
        while hak > 0:
            self.user_name = input("Kullanıcı Adınız: ")
            user_password = input("Kullanıcı Şifreniz: ")

            login_db = self.db_manager()
            result = login_db.loginControl(self.user_name, user_password)

            if result:
                self.menu()
                break

            else:
                print("Hatalı Kullanıcı Adı veya Parolası.")
                hak -= 1

                if hak == 0:
                    self.user_register()
        print('\n')

    def user_register(self):
        """
        DOCSTRING: Kullanıcı Kayıt
        INPUT: name = ozgen , password = 123
        OUTPUT: user_login()
        """
        while True:
            self.user_name = input("Kullanıcı Adınız: ")
            user_password = input("Kullanıcı Şifreniz: ")

            register_db = self.db_manager()
            result = register_db.registerControl(self.user_name)
            if result:
                print(f"'{self.user_name}' Kullanıcı Adı Mevcuttur. Lütfen Tekrar Deneyiniz")

            else:
                user_dict = {}
                user_dict['name'] = self.user_name
                user_dict['password'] = user_password

                register_db.addUser(user_dict)

                print("Kullanıcınız Oluşturulmuştur")
                break

    def menu(self):
        """
        DOCSTRING: Application Menu
        INPUT: 1
        OUTPUT: add_comment()
        """
        print(100 * '-')
        #self.user_name = user_name #*
        print(f"Hoşgeldin {self.user_name}\n")
        first_msg = "| 1- Yorum Ekle\n| 2- JSON'daki Verileri Gözlemle\
                     \n| 3- Database'deki Verileri Gözlemle\
                     \n| 4- Excel Dosyası İçerisindeki Verilerin Analizi\n| 5- Çıkış"


        while True:
            print(first_msg)
            print(100 * '-')
            input_msg = input("Menüden Bir İşlem Seçiniz: ")

            if input_msg == '1':
                self.add_comment()

            elif input_msg == '2':
                self.view_json()

            elif input_msg == '3':
                self.import_db()

            elif input_msg == '4':
                self.import_excel()

            elif input_msg == '5':
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')

    def add_comment(self):
        """
        DOCSTRING: Yorum girilmesi ve yorumların değişik dosya tipleirnde kayıt edilmesi
        INPUT: comment = bu ürün çok iyi
        OUTPUT: inner_menu()
        """
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
                self.control_manager.listSend(self.user_name, comment_list)

        print(100 * '*')

    def view_json(self):
        """
        DOCSTRING: JSON'daki verilerin gözlemlenmesi
        INPUT: file_name
        OUTPUT: keys and values
        """
        print('\n')
        print(100 * '-')
        self.file_name = input("Dosyanızın Adını Giriniz: ")
        print(100 * '-')

        if '.json' in self.file_name:
            self.file_name = self.file_name

        else:
            self.file_name = self.file_name + '.json'

        try:
            json_file = self.file_manager(self.file_name)
            result = json_file.viewJson()

            print('\n')
            print(f"'{self.file_name}' Dosyası İçerisindeki Veriler: ")
            for i in result:
                print(100 * '-')
                print(f"|{i['comment']} | {i['rate']} | {i['analysis']}|")
            print(100 * '-')
            print('\n')

        except FileNotFoundError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')

    def import_db(self):
        """
        DOCSTRING: Database içerisindeki verilerin gözlemlenmesi
        INPUT: u
        OUTPUT: viewDb()
        """
        print('\n')
        print(100 * '-')
        find_choose = "| 1- Kullanıcıya Göre Ara\n| 2- Yoruma Göre Ara\
                       \n| 3- Duygu Analizine Göre\n| 4- Çıkış"

        while True:
            print(find_choose)
            print(100 * '-')
            import_msg = input("Aramak İstediğiniz Alanı Seçeniz: ")

            if import_msg == '1':
                self.view_db('user', self.user_name)
                # break

            elif import_msg == '2':
                print(100 * '-')
                comment_msg = input("Aramak İstediğiniz Yorumu Yazınız: ")
                print(100 * '-')
                self.view_db('comment', comment_msg)
                # break

            elif import_msg == '3':
                print(100 * '-')
                print("1- Pozitif\n2- Negatif\n3- Nötrn\n4- Çıkış")
                print(100 * '-')
                inner_input = input("Aramak İstediğiniz Duygu Analizi Sonucunu Giriniz: ")
                print(100 * '-')

                if inner_input == "1" :
                    self.view_db('analysis', "Pozitif")
                elif inner_input == "2":
                    self.view_db('analysis', "Negatif")
                elif inner_input == "3":
                    self.view_db('analysis', "Nötr")
                # break

            elif import_msg == '4' :
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')

    def import_excel(self):
        """
        DOCSTRING: Excel dosyasından alınan verilerin sentiment
                   analiz yapılarak işlenmesi ve kayıt edilmesi.
        INPUT: file_name
        OUTPUT: inner_menu()
        """
        print(100 * '-')
        exel_file = input("Dosya Adınızı Giriniz [*xlsx]: ")
        print(100 * '-')

        if '.xlsx' in exel_file:
            loc = exel_file

        else:
            loc = exel_file+'.xlsx'

        try:
            work_book = xlrd.open_workbook(loc)
            sheet = work_book.sheet_by_index(0)
            if '.xlsx' in loc:
                xlsx_list = []
                for col_index in range(sheet.ncols):
                    for i in range(0, sheet.nrows):
                        excel_comment = sheet.cell(i, col_index).value

                        xlsx_list.append(excel_comment)

                self.control_manager.listSend(self.user_name, xlsx_list)

        except FileNotFoundError:
            print("Dosya Bulunamadı")
            print('\n')

    def view_db(self, key, value):
        """
        DOCSTRING: Database de bulunan verilerin çekilmesi
        INPUT: key,value
        OUTPUT: importDb()
        """
        view_db = self.db_manager()

        result = view_db.importComment(self.user_name, key, value)

        print(f"'{self.user_name}' kullanıcısının '{key}' anahtarındaki '{value}' yorumları: \n")
        for i in result:
            print(100 * '-')
            print(f"|Kullanıcı Adı: {i['user']} | Yorum: {i['comment']} \
                | Rate: {i['rate']} | Analiz: {i['analysis']}|")
        print(100 * '-')
        print('\n')


App().user_menu()