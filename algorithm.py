import numpy as np
import pandas as pd

#Bu fonksiyon verilen koordinatın orijin ile arasındaki uzaklığı ve pozitif açısını bulur.
def hipo(x, y):

    if x == None:
        print("x none {x}")
    elif y == None:
        print("y none {y}")
        
    try:
        m = x / y
    except:
        m = 0

    return [np.sqrt(np.power(np.float64(x), 2) + np.power(np.float64(y), 2)), np.arctan(m)]

#Excel Dosyasını oku.
all_sheets = pd.read_excel('Veriler.xlsx', sheet_name = None)

sheet_tables = []

for sheet_name, data in all_sheets.items():
    #Bos sayfalari alma
    if data.empty:
        continue
    
    #Empty degerleri cikar
    i = 0
    j = 0
    l = len(data)


    for m in range(l):
        if pd.isna(data.iloc[m, 0]):
            i += 1

    for n in range(l):
        if pd.isna(data.iloc[n, 1]):
            j += 1

    if i > j:    
        l = l - i
    else:
        l = l - j

    data = data.iloc[:l, :].copy()

    #Veriyi Numpy icin kullanilabilir hale getir.
    for i in range(l):
        data.iloc[i, :] = data.iloc[i ,:].str.replace('[', '').str.replace(']', '').str.split().copy()
        
    #Yeni table olusturuldu.
    data_ = pd.DataFrame(columns=['Prev', 'Curr'])
    data_['Prev'] = data.iloc[:, 0]
    data_['Curr'] = data.iloc[:, 1]
    sheet_tables.append(data_)


#Her koordinat icin bir sonraki nokta ile arasindaki mesafeyi bul ve hipo() fonksiyonuna yaz.
for table in sheet_tables:
    
    l = len(table['Prev'])

    for i in range(l - 1):  
        try:
            x1 = float(table.iloc[i, 0][0])
            x2 = float(table.iloc[i + 1, 0][0])

            y1 = float(table.iloc[i, 0][1])
            y2 = float(table.iloc[i + 1, 0][1])

            # Hesaplanan mesafeyi kaydet. (Prev kolonu icin.)
            table.iloc[i, 0].append(hipo(x1 - x2, y1 - y2))

            x1 = float(table.iloc[i, 1][0])
            x2 = float(table.iloc[i + 1, 1][0])

            y1 = float(table.iloc[i, 1][1])
            y2 = float(table.iloc[i + 1, 1][1])

            # Hesaplanan mesafeyi kaydet. (Curr kolonu icin.)
            table.iloc[i, 1].append(hipo(x1 - x2, y1 - y2))

        except Exception as e:  # Hata mesajını yazdır
            pass
            #print(f"Hata: {e}")  


'''
    Burada kendi algoritmam ile iki nokta arasindaki mesafeyi ve kenarin acisini agirliklarina gore carpip bir değer elde ettim.
    Elde ettigim degeri gozlemledigim deger ile karsilastirip kosula gore bir karara vardim.

    Edge Error List = Prev - Curr : Prev ile Curr arasinda her kenarin farkini buldum.
    Acceleration Error List = Prev - Curr : Prev ile Curr arasindaki her acinin farkini buldum.

    Last_Value = EEL * (AEL^10)

    Verilerden gözlemledigim kadari ile Last_Value <= 2.5 optimize bir sart olup bu sarti saglayan verilerin  ayni seri olduguna karar verilmistir.   
'''
for table in sheet_tables:
    l = len(table)

    edge_error_list = np.array([])
    acceleration_error_list = np.array([])


    # EEL ve AEL atamalari yapilmistir.

    for i in range(l - 1):
            for j in range(2):
                
                diff = np.abs(table['Prev'][i][2][j] - table['Curr'][i][2][j])
                
                if j == 0:
                    edge_error_list = np.append(edge_error_list,diff)
                else:
                    acceleration_error_list = np.append(acceleration_error_list,diff)

    #Last Value hesaplanmistir.
    avg_eel = np.average(edge_error_list)
    avg_ael = np.average(acceleration_error_list)

    last_value = avg_eel*(np.power(avg_ael, 10))

    if last_value <= 2.5:
        print(f"Ayni Seri, Last Value: {str(last_value)[:4]}")
    else:
        print(f"Farkli Seri, Last Value: {str(last_value)[:4]}")