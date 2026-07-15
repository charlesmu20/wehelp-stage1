import mysql.connector
import os

from fastapi import FastAPI,Request,Form,Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
con = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD"),
        database="website"
    )
app= FastAPI()
app.add_middleware(SessionMiddleware, secret_key="K9mP2nQ7rL4wV8j")
templates = Jinja2Templates(directory="templates")

@app.get("/")
#首頁
def home(request:Request):
    return templates.TemplateResponse(request,"index.html")
# 會員頁 
@app.get("/member")
def member(request:Request):
    if request.session.get("member"):
        name = request.session["member"]["name"]
        return templates.TemplateResponse(request,"member.html",{"name":name})
    else:
        return RedirectResponse("/")
#錯誤頁面
@app.get("/ohoh")
def ohoh(request: Request, msg: str):
    return templates.TemplateResponse(request, "error.html", {"msg": msg})
#登出
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")
#註冊會員
@app.post("/signup")
def signup(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()]):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        cursor.close()
        return RedirectResponse("/ohoh?msg=重複的電子郵件", status_code=303)
    else:
        cursor.execute("INSERT INTO member (name, email, password) VALUES (%s,%s,%s)",(name, email, password))
        con.commit()
        cursor.close()
        return RedirectResponse("/", status_code=303)
#登入會員
@app.post("/login")
def login(request: Request, email: Annotated[str, Form()], password: Annotated[str, Form()]):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM member WHERE email = %s AND password = %s",(email,password))
    result = cursor.fetchone()
    if result:
        cursor.close()
        request.session["member"] = {
            "id": result[0],
            "name": result[1],
            "email": result[2]
        }
        return RedirectResponse("/member",status_code=303)
    else:
        cursor.close()
        return RedirectResponse("/ohoh?msg=電子郵件或密碼錯誤", status_code=303)
    
#建立留言
@app.post("/api/message")
def create_message(request: Request, body: dict=Body(None)):
    #先檢查登入狀態
    if request.session.get("member") is None:
        return {"error": True}
    #抓留言資料
    member_id = request.session["member"]["id"]
    content = body["content"]
    #新增到資料庫
    cursor = con.cursor()
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)",(member_id, content))
    con.commit()
    cursor.close()
    return {"ok":True}
#取得留言
@app.get("/api/message")
def get_message(request: Request):
    if request.session.get("member") is None:
        return {"error": True}
    #從資料庫抓所有留言資料
    cursor = con.cursor()
    cursor.execute("SELECT message.id, member.name, message.content, message.member_id FROM message JOIN member ON message.member_id = member.id")
    results = cursor.fetchall()
    cursor.close()
    print(results)
    #把資料存成指定格式再return回前端
    data=[]
    member_id = request.session["member"]["id"]
    for result in results:
        data.append({
            "id": result[0],
            "name": result[1],
            "content": result[2],
            "self":  result[3]== member_id
        })
    return {"ok":True,"data":data}
#靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")


# uvicorn main:app --reload
