const character={
    "悟空": { x: 0, y: 0 },
    "丁滿": { x: -1, y: 4 },
    "辛巴": { x: -3, y: 3 },
    "貝吉塔": { x: -4, y: -1 },
    "弗利沙": { x: 4, y: -1 },
    "特南克斯": { x: 1, y: -2 }
}
const sideA = ["丁滿", "弗利沙"];
const sideB = ["辛巴", "貝吉塔", "悟空", "特南克斯"];

function getDistance(char1, char2) {
    let distance=Math.abs(character[char1].x-character[char2].x)+Math.abs(character[char1].y-character[char2].y);
    const sameSide = (sideA.includes(char1) && sideA.includes(char2)) || 
                     (sideB.includes(char1) && sideB.includes(char2));
    if (!sameSide) distance += 2;
    return distance;
}
function func1(name){
    const others=Object.keys(character).filter(n => n !== name);
    let distances=others.map(n => ({name: n,dis: getDistance(name, n)}));
    const maxDist=Math.max(...distances.map(d => d.dis));
    const minDist=Math.min(...distances.map(d => d.dis));
    const farthest = distances.filter(d => d.dis===maxDist).map(d=>d.name);
    const closest = distances.filter(d => d.dis === minDist).map(d => d.name);
    console.log(`最遠${farthest.join("、")}；最近${closest.join("、")}`);
}

func1("辛巴");
func1("悟空"); 
func1("弗利沙"); 
func1("特南克斯"); 

const bookings = {"S1":[], "S2":[], "S3":[]};

function func2(ss, start, end, criteria){
    //解析條件
    let field, value, op;
    if (criteria.includes(">=")) {
        [field, value] = criteria.split(">=");
        op = ">=";
    } else if (criteria.includes("<=")) {
        [field, value] = criteria.split("<=");
        op = "<=";
    } else {
        [field, value] = criteria.split("=");
        op = "=";
    }
    // 篩選符合條件的服務
    const matched = ss.filter(s => {
        if (op === "=") return s[field] == value;
        if (op === ">=") return s[field] >= value;
        if (op === "<=") return s[field] <= value;
    });
    // 篩選時段可用的服務
    const available = matched.filter(s => {
        return bookings[s.name].every(([bs, be]) => end <= bs || start >= be);
    });
    // 找最佳
    let best = available[0];
    for (let s of available) {
        if (op === ">=") {
            if (s[field] < best[field]) best = s;
        } else if (op === "<=") {
            if (s[field] > best[field]) best = s;
        }
    }
    if (best){
        bookings[best.name].push([start,end]);
        console.log(best.name)
    }
    else{
        console.log("Sorry");
    }
}
const services=[
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

function func3(index) {
    const diffs = [0, -2, -5, -4];
    const groupIndex = Math.floor(index / 4);
    const posIndex = index % 4;
    const start = 25 - groupIndex * 2;
    console.log(start + diffs[posIndex]);
}

func3(1);
func3(5);
func3(10);
func3(30);

function func4(sp, stat, n){
    const available = [];
    for (let i = 0; i < sp.length; i++) {
        if (stat[i] === "0") {
            available.push({index: i, space: sp[i]});
        }
    }
    const fitted = available.filter(c => c.space >= n);
    let best;
    if (fitted.length > 0) {
        best = fitted[0];
        for (const c of fitted) {
            if (c.space < best.space) best = c;
        }
    } else {
        best = available[0];
        for (const c of available) {
            if (c.space > best.space) best = c;
        }
    }
    console.log(best.index);
}
func4([3, 1, 5, 4, 3, 2],"101000", 2);
func4([1, 0, 5, 1, 3],"10100", 4); 
func4([4, 6, 5, 8],"1000", 4);