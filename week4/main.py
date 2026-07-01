from fastapi import FastAPI,Request,Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="900306")
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
    
# 靜態檔案處理
app.mount("/static", StaticFiles(directory="static"), name="static")

# uvicorn main:app --reload