from fastapi import FastAPI, Depends
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# --- 1. Import thêm đồ chơi cho Database ---
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- 2. Cài đặt Database (Tạo file data.db) ---
# Dòng này sẽ tạo ra 1 file tên là 'data.db' ngay trong thư mục code
DATABASE_URL = "sqlite:///./data.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 3. Thiết kế cái "Bảng Excel" để lưu trữ ---
class LichSu(Base):
    __tablename__ = "lich_su_tinh_toan"
    
    id = Column(Integer, primary_key=True, index=True) # Số thứ tự (1, 2, 3...)
    so_a = Column(Integer)  # Cột lưu số thứ nhất
    so_b = Column(Integer)  # Cột lưu số thứ hai
    ket_qua = Column(Integer) # Cột lưu kết quả

# Lệnh tạo bảng (nếu chưa có)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Cấu hình CORS (Giữ nguyên) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hàm phụ để mở ngăn kéo Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API TÍNH TOÁN CŨ (Được nâng cấp) ---
class phepcong(BaseModel):
    a: int
    b: int

@app.post("/tinh-tong")
def sum(dat: phepcong, db: Session = Depends(get_db)): # <--- Thêm db vào đây
    tong = dat.a + dat.b
    
    # --- ĐOẠN NÀY MỚI: Lưu vào Database ---
    # 1. Tạo dòng dữ liệu mới
    ghi_chep = LichSu(so_a=dat.a, so_b=dat.b, ket_qua=tong)
    # 2. Thêm vào sổ
    db.add(ghi_chep)
    # 3. Đóng dấu lưu (Save)
    db.commit()
    # --------------------------------------

    return {
        "First_num": dat.a,
        "Second_num": dat.b,
        "ans": tong,
        "note": "Đã lưu vào lịch sử nhé sếp!" # Thông báo mới
    }

# --- API MỚI: XEM LẠI LỊCH SỬ ---
@app.get("/xem-lich-su")
def xem_history(db: Session = Depends(get_db)):
    # Lấy tất cả dòng trong bảng LichSu ra
    tat_ca = db.query(LichSu).all()
    return tat_ca