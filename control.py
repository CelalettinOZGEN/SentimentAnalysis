"""
DOCSTRING: Sentiment analizi ve analizi yapılan yorumların \
dosya türlerine göre ve database'e kaydedilme işlemleri.
"""
from tensorflow.python.keras.models import load_model
from Sentiment import tokenizer, pad_sequences, max_tokens
#unused-import --> tokens_to_string

from dbManager import dbManager
from fileManager import fileManager

class Control:
    """
    DOCSTRING: Yorum ekleme işlemlerin dosya yapılarına göre işlenmesi ve kaydedilemesi işlemleri.
    """
    def __init__(self):
        self.db_manager = dbManager
        self.file_manager = fileManager

    @staticmethod
    def sentiment_analysis(comment):
        """
        DOCSTRING: Liste data yapısı ile gelen yorumların sırasıyla Sentiment Analizinin yapılması
        INPUT: comment_list = ["bu ürün çok iyi", "bu ürünle ilgili çok sorun yaşadım"]
        OUTPUT: Pozitif, Nötr, Negatif
        """
        my_list =[]

        model = load_model('model.h5')
        texts=[comment]
        tokens = tokenizer.texts_to_sequences(texts)
        tokens_pad = pad_sequences(tokens, maxlen=max_tokens)
        sentiment = model.predict(tokens_pad)

        if sentiment>=0.85:
            analysis = "Pozitif"

        elif 0.40 <= sentiment < 0.85:
            analysis = "Nötr"

        else:
            analysis = "Negatif"

        my_list.append([float(sentiment), analysis])

        return my_list

    def list_send(self, user_name, send_list):
        """
        DOCSTRING: Analizi yapılan yorumların dosya tiplerine göre data yapılarına ayrıştırılması
        INPUT: ["bu ürün çok iyi", 0.95760, "Pozitif"]
        OUTPUT: inner_menu()
        """
        sentiment_list = []
        for i in send_list:
            comments = self.sentiment_analysis(i)

            for j in comments:
                sentiment = j[0]
                analysis = j[1]

            sentiment_list.append([i, sentiment, analysis])

        comment_list = self.json_send(user_name, sentiment_list)
        excel_list = self.excel_send(user_name,sentiment_list)

        self.inner_menu(user_name, comment_list, excel_list)

    @staticmethod
    def json_send(user_name, json_list):
        """
        DOCSTRING: list_send() fonksiyonundan gelen json_list'in özelliklerine \
            ayrıştırılarak JSON dosya yapısı ile oluşturulması.
        INPUT: [{comment: "bu ürün çok iyi", rate: 0.95760, sentiment: "Pozitif"}]
        OUTPUT: list_send()
        """
        comment_list = []
        for i in json_list:
            commnet_dict = {}
            commnet_dict['user'] = user_name #* username ata
            commnet_dict['comment'] = i[0]
            commnet_dict['rate'] = i[1]
            commnet_dict['analysis'] = i[2]

            comment_list.append(commnet_dict)

        return comment_list
    @staticmethod
    def excel_send(user_name, excel_list):
        """
        DOCSTRING: list_send() fonksiyonundan gelen excel_list'in özelliklerine \
            ayrıştırılarak EXCEL dosya yapısı ile oluşturulması.
        INPUT: [["bu ürün çok iyi"], [0.95760], ["Pozitif"]}]
        OUTPUT: list_send()
        """

        comment_list = []
        for i in excel_list:
            comment_list.append([user_name, i[0], i[1], i[2]]) #*user_name ata

        return comment_list


    def inner_menu(self, user_name, db_list, excel_list):
        """
        DOCSTRING: Ekleme yapma işleminin opsiyonel olarak seçilme işlemlerini barındıran menüsüdür.
        INPUT: 1
        OUTPUT: add_json()
        """
        print(100 * '-')
        print("** Verileriniz Analiz Edilmiştir. Lütfen Aşağıdaki Menüden Bir İşlem Seçiniz")
        import_msg = "| 1- JSON'a Kaydet\n| 2- Excel'e Kaydet\n\
                      | 3- JSON ve Excel'e Kaydet\n| 4- Çıkış"

        while True:
            print(import_msg)
            print(100 * '-')
            choose_import = input("Eklemek İstediğiniz Dosya Türünü Seçiniz: ")
            print(100 * '-')

            if choose_import == '1':
                self.add_json(db_list)
                break

            elif choose_import == '2':
                self.export_excel(user_name,excel_list)
                self.add_db(db_list)
                break

            elif choose_import == '3':
                self.add_json(db_list)
                self.export_excel(user_name,excel_list)
                break

            elif choose_import == '4':
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')

    def add_db(self, db_list):
        """
        DOCSTRING: Tüm dosya türlerinin kaydedilmesinin ardından muhakkak \
            database'e kaydetmek için kullanılır.
        INPUT: -
        OUTPUT: Veriler Database'e Aktarıldı
        """
        connect_db = self.db_manager()
        connect_db.addComment(db_list)
        print(100 * '-')
        print("** Veriler Database'e Aktarıldı")
        print('\n')

    def add_json(self, json_list):
        """
        DOCSTRING: JSON dosya yapısıyla işlenen verilerin JSON dosyasına kaydedilmesi.
        INPUT: comment_list[]
        OUTPUT: Veriler '{file_name}' Dosyasına Kaydedildi
        """
        file_name = input("JSON Dosyasını Giriniz [*json]: ")

        if '.json' in file_name:
            file_name = file_name

        else:
            file_name =file_name + '.json'

        try:
            connect_fm = self.file_manager(file_name)
            connect_fm.addJson(json_list)
            print(f"** Veriler '{file_name}' Dosyasına Kaydedildi")
            print('\n')

        except FileNotFoundError:
            print(100 * '-')
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')

        self.add_db(json_list)

    def export_excel(self, user_name, excel_list):
        """
        DOCSTRING: EXCEL dosya yapısıyla işlenen verilerin EXCEL dosyasına kaydedilmesi.
        INPUT: comment_list[]
        OUTPUT: Veriler '{file_name}' Dosyasına Kaydedildi
        """

        file_name = input("Dosya Adını Giriniz [*xls]: ")
        if '.xls' in file_name:
            file_name = file_name
        else:
            file_name = file_name + '.xls'

        try:
            table_data = [['User', 'Comment', 'Rate', 'Sentiment']]

            for i in excel_list:
                table_data.append(i)

            connect_fm = self.file_manager(file_name)
            connect_fm.exportExcel(user_name, table_data)

            print(f"Veriler '{file_name}' Dosyasına Kaydedildi")
            print(100 * '-')
        except FileNotFoundError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')