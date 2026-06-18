character = {
    "悟空": {"x": 0, "y": 0},
    "丁滿": {"x": -1, "y": 4},
    "辛巴": {"x": -3, "y": 3},
    "貝吉塔": {"x": -4, "y": -1},
    "弗利沙": {"x": 4, "y": -1},
    "特南克斯": {"x": 1, "y": -2}
}

sideA = ["丁滿", "弗利沙"]
sideB = ["辛巴", "貝吉塔", "悟空", "特南克斯"]

def getDistance(char1, char2):
    distance = abs(character[char1]["x"] - character[char2]["x"]) + abs(character[char1]["y"] - character[char2]["y"])
    if not (char1 in sideA and char2 in sideA or char1 in sideB and char2 in sideB):
        distance += 2
    return distance

def func1(name):
    others = [n for n in character if n != name]
    distances = [{"name": n, "dis": getDistance(name, n)} for n in others]
    maxDist = max(d["dis"] for d in distances)
    minDist = min(d["dis"] for d in distances)
    farthest = [d["name"] for d in distances if d["dis"] == maxDist]
    closest = [d["name"] for d in distances if d["dis"] == minDist]
    print(f"最遠{'、'.join(farthest)}；最近{'、'.join(closest)}")

func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯") 

bookings = {"S1":[],"S2":[],"S3":[]}
def func2(ss,start,end,criteria):
    # 解析條件
    if ">=" in criteria:
        field,value = criteria.split(">=")
        op = ">="
    elif "<=" in criteria:
        field,value = criteria.split("<=")
        op = "<="
    else:
        field, value = criteria.split("=")
        op = "="
    if field != "name":
        value = float(value)
    # 篩選符合條件的服務
    matched =[]
    for s in ss:
        if op == "=":
            if s[field] == value:
                matched.append(s)
        elif op == ">=":
            if s[field] >= value:
                matched.append(s)
        elif op == "<=":
            if s[field] <= value:
                matched.append(s)
    #從matched找出有沒有被預約的時間
    available =[]
    for s in matched:
        name = s["name"]
        is_available= True
        for booking_start,booking_end in bookings[name]:
            if not (end<=booking_start or start>= booking_end):
                is_available = False
                break
        if is_available:
            available.append(s)
    #找尋最佳
    best = None
    if available:
        if op == ">=":
            best = min(available, key=lambda s: s[field])
        elif op == "<=":
            best = max(available, key=lambda s: s[field])
        else:
            best = available[0]
    else:
        best = None
    if best:
        bookings[best["name"]].append((start, end))
        print(best["name"])
    else:
        print("Sorry")

services=[
{"name":"S1","r":4.5,"c":1000},
{"name":"S2","r":3,"c":1200},
{"name":"S3","r":3.8,"c":800}
]
func2(services, 15, 17,"c>=800") 
func2(services, 11, 13, "r<=4")    
func2(services, 10, 12, "name=S3") 
func2(services, 15, 18, "r>=4.5") 
func2(services, 16, 18, "r>=4")    
func2(services, 13, 17, "name=S1")
func2(services, 8, 9, "c<=1500")   

def func3(index):
    diffs = [0, -2, -5, -4]
    groupIndex = index // 4
    posIndex = index % 4
    start = 25 - groupIndex * 2
    print(start + diffs[posIndex])

func3(1)
func3(5)
func3(10)
func3(30)

def func4(sp, stat, n):
    available = []
    for i in range(len(sp)):
        if stat[i] == "0":
            available.append({"index": i, "space": sp[i]})
    
    fitted = [c for c in available if c["space"] >= n]
    
    if fitted:
        best = fitted[0]
        for c in fitted:
            if c["space"] < best["space"]:
                best = c
    else:
        best = available[0]
        for c in available:
            if c["space"] > best["space"]:
                best = c
    
    print(best["index"])
    
func4([3, 1, 5, 4, 3, 2],"101000", 2) 
func4([1, 0, 5, 1, 3],"10100", 4) 
func4([4, 6, 5, 8],"1000", 4) 