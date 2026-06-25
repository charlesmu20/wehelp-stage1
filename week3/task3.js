function toggle() {
    document.getElementById('burgerMenu').classList.toggle('active');
};
let currentIndex = 13;
let spots=[];
const ContentBlocks = document.querySelector(".Content-blocks");
async function init() {
    const res1 = await fetch("https://cwpeng.github.io/test/assignment-3-1");
    const data1 = await res1.json();
    
    const res2 = await fetch("https://cwpeng.github.io/test/assignment-3-2");
    const data2 = await res2.json();
    //用serial建立圖片的物件
    const picMap={};
    for (const item of data2.rows){
        picMap[item.serial] = item.pics;
    }
    //資料放進spots
    for (const item of data1.rows){
        const pics = picMap[item.serial];
        let firstPic="";
        if (pics){
            firstPic = "/resources" + pics.split("/resources")[1];
        }
        spots.push({
            name : item.sname,
            image :data2.host + firstPic
        })
    }
    //渲染bars
    const barsDiv = document.querySelector(".bars");
    const classes = ["one","two","three"];
    for (let i=0 ; i<3 ; i++){
        const bar = document.createElement("div");
        bar.className = "bar "+classes[i];
        const img = document.createElement("img");
        img.src = spots[i].image;
        const span = document.createElement("span");
        span.textContent = spots[i].name;
        bar.appendChild(img);
        bar.appendChild(span);
        barsDiv.appendChild(bar);
    }
    //渲染Content blocks
    for (let i=3 ; i<13 ;i++){
        //block
        const block = document.createElement("div");
        block.className = "block";
        if (i === 11 || i === 12) {
            block.classList.add("last")
        }
        block.style.backgroundImage = `url(${spots[i].image})`
        //星星span
        const span = document.createElement("span");
        span.className = "star";
        span.textContent="⭐";
        //文字div
        const blockText = document.createElement("div");
        blockText.className = "block-text";
        blockText.textContent = spots[i].name;
        
        block.appendChild(span);
        block.appendChild(blockText);
        ContentBlocks.appendChild(block);
    }
};
//loadMore
function loadMore(){
        const end = Math.min(currentIndex+10,spots.length);

    for (let i=currentIndex;i<end;i++){
        const block = document.createElement("div");
        block.className = "block";
        block.style.backgroundImage = `url(${spots[i].image})`
        //星星span
        const span = document.createElement("span");
        span.className = "star";
        span.textContent="⭐";
        //文字div
        const blockText = document.createElement("div");
        blockText.className = "block-text";
        blockText.textContent = spots[i].name;
        
        block.appendChild(span);
        block.appendChild(blockText);
        ContentBlocks.appendChild(block); 
    };
    currentIndex+=10;
    //最後跑完隱藏按鈕
    if (currentIndex >= spots.length){
        loadBtn.style.display = "none";
    };
}
const loadBtn = document.querySelector(".load");
loadBtn.addEventListener('click',loadMore);
init()

