import urllib.request
import json
import csv
#抓中英文資料
url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
with urllib.request.urlopen(url_ch) as response:
    ch_data = json.loads(response.read())
    ch_list = ch_data["list"]
url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with urllib.request.urlopen(url_en) as response:
    en_data = json.loads(response.read())
    en_list = en_data["list"]
#英文資料轉換成字典，用_id當key
en_dict = {}
for hotel in en_list:
    en_dict[hotel["_id"]] = hotel
#把英文資料合併到中文+ 輸出hotel.csv
with open("hotel.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    for hotel in ch_list:
        chinese_name = hotel["旅宿名稱"]
        english_name = en_dict[hotel["_id"]]["hotel name"]
        chinese_address = hotel["地址"]
        english_address = en_dict[hotel["_id"]]["address"]
        phone = hotel["電話或手機號碼"]
        room_count = hotel["房間數"]
        writer.writerow([chinese_name, english_name, chinese_address, english_address, phone, room_count])

# district.csv
hotel_count = {}
room_count = {}
for hotel in ch_list:
    #切出區名
    address = hotel["地址"]
    start = address.find("市")+1
    end = address.find("區")+1
    district = address[start:end]
    # 累加該區的飯店數量 & 房間數量，第一次遇到該區時從0開始
    hotel_count[district] = hotel_count.get(district,0) +1
    room_count[district] = room_count.get(district,0) + int(hotel["房間數"])
#寫入csv
with open("districts.csv","w",newline="",encoding="utf-8") as f:
    writer = csv.writer(f)
    for district in hotel_count:
        writer.writerow([district,hotel_count[district],room_count[district]])

