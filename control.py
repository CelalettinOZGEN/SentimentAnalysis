from tensorflow.python.keras.models import load_model
from Sentiment import tokens_to_string, tokenizer, pad_sequences, max_tokens

from dbManager import dbManager
from fileManager import fileManager

class Control:
    def __init__(self):
        self.db_manager = dbManager
        self.file_manager = fileManager


    def sentiment_analysis(self, comment):
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

    def list_send(self, user_name, send_list):
        self.user_name = user_name
        sentiment_list = []
        for i in send_list:
            comments = self.sentiment_analysis(i)

            for j in comments:
                sentiment = j[0]
                analysis = j[1]

            sentiment_list.append([i, sentiment, analysis])
        
        comment_list = self.json_send(sentiment_list)
        excel_list = self.excel_send(sentiment_list)

        self.inner_menu(comment_list, excel_list)
    
    def json_send(self, json_list):

        comment_list = []
        for i in json_list:
            commnet_dict = {}
            commnet_dict['user'] = self.user_name #* username ata
            commnet_dict['comment'] = i[0]
            commnet_dict['rate'] = i[1]
            commnet_dict['analysis'] = i[2]

            comment_list.append(commnet_dict)

        return comment_list
    
    def excel_send(self, excel_list):

        comment_list = []
        for i in excel_list:
            comment_list.append([self.user_name, i[0], i[1], i[2]]) #*user_name ata

        return comment_list


    def inner_menu(self, db_list, excel_list):
        print(100 * '-')
        print("** Verileriniz Analiz Edilmiştir. Lütfen Aşağıdaki Menüden Bir İşlem Seçiniz")
        import_msg = "| 1- JSON'a Kaydet\n| 2- Excel'e Kaydet\n| 3- JSON ve Excel'e Kaydet\n| 4- Çıkış"

        while True:
            print(import_msg)
            print(100 * '-')
            choose_import = input("Eklemek İstediğiniz Dosya Türünü Seçiniz: ")
            print(100 * '-')

            if choose_import == '1':
                self.add_json(db_list)
                break
                
            elif choose_import == '2':
                self.export_excel(excel_list)
                self.add_db(db_list)
                break

            elif choose_import == '3':
                self.add_json(db_list)
                self.export_excel(excel_list)
                break
                
            elif choose_import == '4':       
                break

            else:
                print("!!! Geçersiz Tıklama")
                print('\n')
    
    def add_db(self, db_list):
        d = self.db_manager()
        d.addComment(db_list)
        print(100 * '-')
        print("** Veriler Database'e Aktarıldı")
        print('\n')

    def add_json(self, json_list):
        file_name = input("JSON Dosyasını Giriniz [*json]: ")

        if '.json' in file_name:
            file_name = file_name

        else:
            file_name =file_name + '.json'

        try:              
            f = self.file_manager(file_name)
            f.addJson(json_list)
            print(f"** Veriler '{file_name}' Dosyasına Kaydedildi")
            print('\n')

        except FileNotFoundError:
            print(100 * '-')
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')

        self.add_db(json_list)
    
    def export_excel(self, excel_list):

        file_name = input("Dosya Adını Giriniz [*xls]: ")
        if '.xls' in file_name:
            file_name = file_name
        else:
            file_name = file_name + '.xls'

        try:
            table_data = [['User', 'Comment', 'Rate', 'Sentiment']]
            
            for i in excel_list:
                table_data.append(i)
            
            f = self.file_manager(file_name)
            f.exportExcel(self.user_name, table_data)

            print(f"Veriler '{file_name}' Dosyasına Kaydedildi")
            print(100 * '-')
        except FileNotFoundError:
            print("Dosya Bulunamadı veya Geçersiz Dosya Türü")
            print('\n')