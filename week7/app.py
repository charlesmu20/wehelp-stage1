import mysql.connector
import os
import hashlib
import secrets
from fastapi import FastAPI,Request,Form,Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request

con = mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.environ.get("DB_PASSWORD"),
        database="website"
    )

mcp = FastMCP("Testing Message Website")
mcp_app = mcp.http_app(path="/")
app= FastAPI(lifespan=mcp_app.lifespan)
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
def post_message(request: Request, body: dict=Body(None)):
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
    cursor.execute("SELECT message.id, member.name, message.content, message.member_id FROM message JOIN member ON message.member_id = member.id ORDER BY message.id ASC")
    results = cursor.fetchall()
    cursor.close()
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
#刪除留言
@app.delete("/api/message/{id}")
def delete_message(request: Request,id: int):
    if request.session.get("member") is None:
        return {"error": True}
    # 後端確認這則留言是否屬於當下登入的使用者
    member_id = request.session["member"]["id"]
    cursor = con.cursor()
    cursor.execute("SELECT member_id FROM message WHERE id=%s",(id,))
    result = cursor.fetchone()
    if result is None or result[0] != member_id:
        cursor.close()
        return{"error":True}
    #根據id刪除留言資料
    cursor.execute("DELETE FROM message WHERE id=%s",(id,))
    con.commit()
    cursor.close()
    return {"ok":True}

#Create Token API
@app.put("/api/token")
def create_token(request: Request):
    if request.session.get("member") is None:
        return {"error": True}
    try:
        #產生token
        member_id = request.session["member"]["id"]
        random_string = secrets.token_hex(16)
        token = hashlib.sha256(random_string.encode()).hexdigest()
        #存進資料庫
        cursor = con.cursor()
        cursor.execute("UPDATE member SET token=%s WHERE id=%s",(token,member_id))
        con.commit()
        cursor.close()
        return{"ok":True,"token":token}
    except:
        return {"error": True}
    
#mcp tool
@mcp.tool()
def create_message(content: str):
    """Create a new message in Testing Message Website."""
    #取出token
    request = get_http_request()
    auth_header = request.headers.get("authorization","")
    print("Auth header:", auth_header) 
    if not auth_header.startswith("Bearer "):
        return {"error": True}
    token = auth_header[7:]
    #去資料庫查對應的會員
    cursor= con.cursor()
    cursor.execute("SELECT id FROM member WHERE token=%s",(token,))
    result = cursor.fetchone()
    if result is None:
        return{"error":True}
    member_id = result[0]
    cursor.execute("INSERT INTO message (member_id, content) VALUES (%s, %s)", (member_id, content))
    con.commit()
    cursor.close()
    return {"ok":True}
## 掛載到 FastAPI 的 /mcp 路徑
app.mount("/mcp", mcp_app)
#靜態檔案
app.mount("/static", StaticFiles(directory="static"), name="static")


