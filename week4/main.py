from fastapi import FastAPI,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
import urllib.request
import json

# 抓旅館資料
url_ch = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
with urllib.request.urlopen(url_ch) as response:
    ch_data = json.loads(response.read())
    ch_list = ch_data["list"]

url_en = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"
with urllib.request.urlopen(url_en) as response:
    en_data = json.loads(response.read())
    en_list = en_data["list"]
# 英文資料轉字典
en_dict = {}
for hotel in en_list:
    en_dict[hotel["_id"]] = hotel
    
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="12344522133")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(request,"index.html")

@app.post("/login")
def login(request:Request,email: Annotated[str, Form()]="", password: Annotated[str, Form()]=""):
    if email == "" or password == "":
        return RedirectResponse("/ohoh?msg=請輸入信箱和密碼",status_code=303)
    elif email == "abc@abc.com" and password == "abc":
        request.session["login"]=True
        return RedirectResponse("/member",status_code=303)
    else :
        return RedirectResponse("/ohoh?msg=信箱或密碼輸入錯誤",status_code=303)
# 會員頁  
@app.get("/ohoh")
def ohoh(request:Request,msg:str):
    return templates.TemplateResponse(request,"error.html",{"msg":msg})

@app.get("/member")
def member(request:Request):
    if request.session.get("login")==True:
        return templates.TemplateResponse(request,"member.html")
    else:
        return RedirectResponse("/")
@app.get("/logout")
def logout(request:Request):
    request.session["login"]=False
    return RedirectResponse("/")
# 取得旅館資訊
@app.get("/hotel/{id}")
def get_hotel(request:Request,id:int):
    hotel_data = None
    for hotel in ch_list:
        if hotel["_id"] == id:
            hotel_data = {
                "chinese_name": hotel["旅宿名稱"],
                "english_name": en_dict[hotel["_id"]]["hotel name"],
                "phone": hotel["電話或手機號碼"]
            }
            break
    if hotel_data != None:
        return templates.TemplateResponse(request,"hotel.html",{"hotel": hotel_data})
    else:
        return templates.TemplateResponse(request,"hotel.html",{"hotel": None})
# 靜態檔案處理
app.mount("/static", StaticFiles(directory="static"), name="static")

# uvicorn main:app --reload