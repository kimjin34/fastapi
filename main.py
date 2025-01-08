from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Allow React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 허용할 출처
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # 허용할 HTTP 메서드
    allow_headers=["*"],  # 허용할 헤더
)

# 사용자 데이터 구조 정의
class User(BaseModel):
    id: str
    password: str
    name: str

class IdCheck(BaseModel):
    id: str

# 사용자 데이터 저장소 (딕셔너리 형태로 관리)
users = {}

@app.post("/create")
def create(user: User):
    if user.id in users:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID입니다.")
    if not user.id or not user.password or not user.name:
        raise HTTPException(status_code=400, detail="모든 필드를 채워주세요.")
    users[user.id] = {"password": user.password, "name": user.name}
    return {"message": "사용자가 생성되었습니다.", "user": user.dict()}

@app.post("/login")
def login(user: User):
    if user.id in users and users[user.id]["password"] == user.password and users[user.id]["name"] == user.name:
        return {"message": "일치합니다."}
    else:
        raise HTTPException(status_code=401, detail="일치하지 않습니다.")

@app.post("/check-id")
def check_id(data: IdCheck):
    """아이디 중복 확인 엔드포인트"""
    if data.id in users:
        return {"exists": True}
    return {"exists": False}

@app.get("/return")
def ret():
    return {"users": users}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
