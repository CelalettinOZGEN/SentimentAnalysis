import re

class ControlUser:

    def __init__(self, password):
        self.password = password

    def passwordControl(self):
        if len(self.password) >= 8:
            if re.search("[A-Z]", self.password) is None:
                print("Büyük Harf Bulunmamaktadır.")
            
            elif re.search("[a-z]", self.password) is None:
                print("Küçük Harf Bulunmamaktadır.")
            
            elif re.search("[0-9]", self.password) is None:
                print("Sayısal Değer Bulunmamaktadır")
            
            elif re.search("[0-9]{5}", self.password):
                print("5 defa üst üste sayısal değer getirilemez.")
            
            elif re.search("([A-Z]|[a-z]){5}", self.password):
                print("5 defa üst üste harf getirilemez.")
            
            elif re.search("\W", self.password) is None:
                print("Özel karakterler Bulunmamaktadır.")

            else:
                print("Şifreniz Onaylandı")
                return self.password

        elif len(self.password) == 0:
            print("!! Şifre Boş Gönderilemez. !!\n")
            return None

        else:
            print("!! Zayıf Güçte Bir Şifre Kullanılamaz. !!\n")
            return None