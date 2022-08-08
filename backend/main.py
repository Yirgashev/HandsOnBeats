from ast import For
from fastapi import FastAPI, Header,Form,Request
from fastapi.responses import JSONResponse ,HTMLResponse,RedirectResponse
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import uuid
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

frontend_dir=os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/frontend'
print(frontend_dir)
template=Jinja2Templates(frontend_dir)

@app.get("/")
def user(req:Request):
    return template.TemplateResponse("index.html",context={"request":req})


import base64
from fastapi import Body
origins = [
  "http://localhost",
  "http://localhost:8000",
  "http://localhost:5173",
  "http://127.0.0.1:8000",
  "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/base64file")
async def uploadfile(image=Body(None), suffix=Body(None)):
    imgdata = base64.b64decode(image)
    file_name = os.getcwd() + "/backend/images/" + str(uuid.uuid1()) + "." + suffix
    file = open(file_name, 'wb')
    file.write(imgdata)
    file.close()
    return {"code": 0, "obj": file_name}

if __name__ == '__main__':
    uvicorn.run(app)
#     Popen(['python', '-m', 'https_redirect'])  # Add this
#     uvicorn.run(
#         'main:app', port=443, host='0.0.0.0',
#         reload=True, reload_dirs=['html_files'],
#         ssl_keyfile='/etc/letsencrypt/live/my_domain/privkey.pem',
#         ssl_certfile='/etc/letsencrypt/live/my_domain/fullchain.pem')
