from dbManager import dbManager


class App:
    def __init__(self):
        self.dM = dbManager
    
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
                self.menu()
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
            

    def menu(self):
        first_msg = "1- Yorum Ekle\n2- JSON'a Ekle"

        while True:
            print(first_msg)
            input_msg = input("Menüden Bir İşlem Seçiniz: ")

            if input_msg == '1':
                self.addComment()
            else:
                break
    
    def addComment(self):
        comment_size = int(input("Kaç Yorum Girilecek: "))

        comment_list = []
        while comment_size > 0:
            comment = input("Yorum Giriniz: ")
            commnet_dict = {}
            commnet_dict['comment'] = comment

            comment_list.append(commnet_dict)
            
            comment_size -= 1

            if comment_size == 0:
                print(comment_list)
                d = self.dM()
                d.addComment(comment_list)

App().userMenu()