"""
DOCSTRING: Sentiment analizi ve analizi yapılan yorumların \
dosya türlerine göre ve database'e kaydedilme işlemleri.
"""
import numpy as np
from datetime import datetime
from tensorflow.python.keras.models import load_model
from Sentiment import tokenizer, pad_sequences, max_tokens
#unused-import --> tokens_to_string

from dbManager import dbManager
from fileManager import fileManager
from graph import Graph

class Control:
    """
    DOCSTRING: Yorum ekleme işlemlerin dosya yapılarına göre işlenmesi ve kaydedilemesi işlemleri.
    """
    def __init__(self):
        self.db_manager = dbManager
        self.file_manager = fileManager
        now = datetime.today()
        self.date = datetime.strftime(now, '%d.%m.%Y')

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

        comment_list = self.json_send(user_name, self.date, sentiment_list)
        excel_list = self.excel_send(user_name, self.date, sentiment_list)

        self.inner_menu(user_name, comment_list, excel_list)

    @staticmethod
    def json_send(user_name, date, json_list):
        """
        DOCSTRING: list_send() fonksiyonundan gelen json_list'in özelliklerine \
            ayrıştırılarak JSON dosya yapısı ile oluşturulması.
        INPUT: [{comment: "bu ürün çok iyi", rate: 0.95760, sentiment: "Pozitif"}]
        OUTPUT: list_send()
        """
        comment_list = []
        for i in json_list:
            commnet_dict = {}
            commnet_dict['user'] = user_name
            commnet_dict['date'] = date
            commnet_dict['comment'] = i[0]
            commnet_dict['rate'] = i[1]
            commnet_dict['analysis'] = i[2]

            comment_list.append(commnet_dict)

        return comment_list
    
    @staticmethod
    def excel_send(user_name, date, excel_list):
        """
        DOCSTRING: list_send() fonksiyonundan gelen excel_list'in özelliklerine \
            ayrıştırılarak EXCEL dosya yapısı ile oluşturulması.
        INPUT: [["bu ürün çok iyi"], [0.95760], ["Pozitif"]}]
        OUTPUT: list_send()
        """

        comment_list = []
        for i in excel_list:
            comment_list.append([user_name, date, i[0], i[1], i[2]]) #*user_name ata

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
            table_data = [['User', 'Date', 'Comment', 'Rate', 'Sentiment']]

            for i in excel_list:
                table_data.append(i)

            connect_fm = self.file_manager(file_name)
            connect_fm.exportExcel(user_name, table_data)

            print(f"Veriler '{file_name}' Dosyasına Kaydedildi")
            print(100 * '-')
        except FileNotFoundError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')
    
    def view_db(self, user_name, key, value, graph_title):
        """
        DOCSTRING: Database de bulunan verilerin çekilmesi
        INPUT: key,value
        OUTPUT: importDb()
        """
        view_db = self.db_manager()

        result = view_db.importComment(user_name, key, value)
        
        deneme_list = []
        for deneme in result:
            deneme_list.append(deneme)

        total = np.count_nonzero(deneme_list)


        print(f"\n'{user_name}' kullanıcısının '{key}' anahtarındaki '{value}' yorumları '{total}' adettir:")
        p_list = []
        n_list = []
        r_list = []

        for i in deneme_list:
            print(100 * '-')

            print(f"|Kullanıcı Adı: {i['user']} | Tarih: {i['date']} | Yorum: {i['comment']} | Rate: {i['rate']} | Analiz: {i['analysis']}|")
            
            if i['analysis'] == "Pozitif":
                p_list.append(i['analysis'])

            elif i['analysis'] == "Negatif":
                n_list.append(i['analysis'])

            elif i['analysis'] == "Nötr":
                r_list.append(i['analysis'])
            

        total_p = np.count_nonzero(p_list)
        total_n = np.count_nonzero(n_list)
        total_r = np.count_nonzero(r_list)
        title = value+' '+graph_title

        self.graphView(total, total_p, total_n, total_r, title)
        
        print(100 * '-')
         
    def graphView(self, total, total_p, total_n, total_r, title):
        g_msg = "| 0- Grafik Olarak Gözlemle\n| 9- Çıkış"

        while True:
            print('\n')
            print(g_msg)
            graph_msg = input("Yapmak İstediğiniz İşlemi Seçiniz: ")
            print("-" * 100)

            if graph_msg == '0':
                if total > 0:
                    Graph(total, total_p, total_n, total_r,title)
                else:
                    print("** Grafik Değerleri Yetersizdir")
                    break
            elif graph_msg == '9':
                break



if __name__ == "__main":
    print("Bu Sayfadan İşlem Yapamazsınız")