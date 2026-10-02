from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas import MenuCreate, MenuResponse

router = APIRouter(prefix="/menus", tags=["Menus"])

# --- DATA DUMMY (In-Memory Database) ---
# Ini akan menyimpan data sementara sebelum kita menggunakan database asli di Sesi 5
db_menus = [
    {
        "id": 1, 
        "nama": "Nasi Goreng Kampung", 
        "harga": 28000, 
        "kategori": "Makanan", 
        "tersedia": True
    },
    {
        "id": 2, 
        "nama": "Ayam Bakar Madu", 
        "harga": 35000, 
        "kategori": "Makanan", 
        "tersedia": True
    },
    {
        "id": 3, 
        "nama": "Es Teh Manis", 
        "harga": 5000, 
        "kategori": "Minuman", 
        "tersedia": True
    },
]

# --- ENDPOINTS ---

# 1. Ambil semua daftar menu (Read All)
@router.get("", response_model=List[MenuResponse])
def get_all_menus():
    return db_menus

# 2. Tambah menu baru (Create)
@router.post("", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(payload: MenuCreate):
    # Logika sederhana untuk membuat ID baru yang unik
    new_id = max([m["id"] for m in db_menus], default=0) + 1
    
    # Membuat objek menu baru dari payload
    new_menu = {
        "id": new_id,
        **payload.model_dump()
    }
    
    db_menus.append(new_menu)
    return new_menu

# 3. Ambil detail menu berdasarkan ID (Read One)
@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu_by_id(menu_id: int):
    for menu in db_menus:
        if menu["id"] == menu_id:
            return menu
    
    # Jika ID tidak ditemukan, kembalikan error 404
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Menu dengan id {menu_id} tidak ditemukan"
    )

# 4. Hapus menu (Delete) - Opsional sebagai pelengkap CRUD
@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(menu_id: int):
    global db_menus
    for index, menu in enumerate(db_menus):
        if menu["id"] == menu_id:
            db_menus.pop(index)
            return None
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="Menu tidak dapat dihapus karena tidak ditemukan"
    )