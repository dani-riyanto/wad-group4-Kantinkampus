# 🍜 DapurKita - Frontend Pesanan Restaurant

Sistem Manajemen Pesanan Restoran / Kantin modern berbasis web yang dikembangkan menggunakan **Vue 3 (Composition API)**, **Vite**, dan **Tailwind CSS**. Aplikasi ini terintegrasi langsung dengan backend **FastAPI** untuk pengelolaan data pesanan secara real-time.

Proyek ini dibangun untuk memenuhi kriteria dan **Requirement Wajib 100% Ujian Tengah Semester (UTS) Web Application Development**.

---

## 🛠️ Teknologi & Tools

- **Framework**: Vue 3 (`<script setup>` Composition API)
- **Build Tool**: Vite
- **Styling**: Tailwind CSS v4 (konfigurasi CSS-first `@theme`, tanpa `tailwind.config.js`)
- **HTTP Client**: Native Fetch API dengan `AbortController` (Lifecycle Cleanup)
- **Backend Service**: FastAPI (Running on `http://localhost:8000`)

---

## 📋 Pemenuhan Kriteria Requirement UTS

| Kode | Requirement | Status | Deskripsi Implementasi |
| :--- | :--- | :---: | :--- |
| **[F1]** | **Fetch Lifecycle & Cleanup** | ✅ **100%** | Data pesanan diambil dari API saat `onMounted`. Pembersihan (`AbortController` & `clearTimeout`) dijalankan otomatis pada `onUnmounted`. |
| **[F2]** | **4 State Visual** | ✅ **100%** | Komponen terpisah untuk state **Loading** (`StateLoading.vue`), **Data** (`OrderItem.vue`), **Empty** (`StateEmpty.vue`), dan **Error** (`StateError.vue`) lengkap dengan tombol **Retry**. |
| **[F3]** | **Form POST & Validasi** | ✅ **100%** | `OrderForm.vue` memvalidasi input wajib nama & jumlah $\ge 1$ di sisi klien, serta mampu menangkap dan menampilkan pesan error dari respons server jika API gagal. |
| **[F4]** | **Hapus Data & Refresh** | ✅ **100%** | Tombol hapus memicu konfirmasi dialog bawaan (`window.confirm`). Setelah sukses, daftar pesanan otomatis diperbarui. |
| **[Q1]** | **HTML Semantik** | ✅ **100%** | Setiap elemen input form (termasuk `<select>`, `<textarea>`, dan search) dihubungkan dengan `<label>` via atribut `for` dan `id`. |
| **[Q2]** | **Aksesibilitas Keyboard** | ✅ **100%** | Seluruh tombol dan field dapat diakses via `Tab` keyboard dan memiliki indikator fokus yang jelas (`:focus-visible`). |
| **[Q4]** | **Dekomposisi Komponen** | ✅ **100%** | Komponen dipecah secara modular. **Tidak ada file `.vue` yang melebihi 100 baris kode**. |

---

## 📁 Struktur Komponen & Baris Kode

Seluruh komponen didekomposisi dengan sangat rapi dan modular:

```text
frontend/src/
├── App.vue                  (~100 baris) -> State utama & layout band halaman
├── constants.js             (~8 baris)   -> Preset menu & status pesanan
├── services/
│   └── api.js               (~25 baris)  -> Modul pembungkus Fetch API
└── components/
    ├── HeaderNav.vue        (~33 baris)  -> Navbar gelap & indikator status sistem
    ├── DashboardBanner.vue  (~33 baris)  -> Banner judul (eyebrow + heading) & tanggal
    ├── DashboardStats.vue   (~44 baris)  -> Statistik ringkasan pesanan & pendapatan
    ├── OrderForm.vue        (~100 baris) -> Form pendaftaran pesanan baru
    ├── OrderList.vue        (~59 baris)  -> Kontainer daftar pesanan, pencarian, & tab status
    ├── OrderItem.vue        (~64 baris)  -> Kartu item pesanan & aksi hapus
    ├── QuantityStepper.vue  (~26 baris)  -> Stepper jumlah (v-model)
    ├── SectionHeading.vue   (~34 baris)  -> Eyebrow label + heading + subjudul
    ├── UiButton.vue         (~33 baris)  -> Tombol utama (hover: panah masuk)
    ├── SiteFooter.vue       (~16 baris)  -> Footer band navy
    ├── StateLoading.vue     (~11 baris)  -> Tampilan indikator loading
    ├── StateEmpty.vue       (~11 baris)  -> Tampilan data kosong / hasil cari 0
    └── StateError.vue       (~21 baris)  -> Tampilan error fetch & tombol Retry
```

---

## 🔌 Spesifikasi Integrasi API Backend

Backend FastAPI berjalan di `http://localhost:8000` dengan endpoint berikut:

- `GET /sessions?search={keyword}&skip=0&limit=10` : Mengambil daftar pesanan (dengan opsi pencarian).
- `POST /sessions` : Menambahkan pesanan baru.
- `DELETE /sessions/{id}` : Menghapus pesanan berdasarkan ID.

### Skema JSON Data Pesanan
```json
{
  "id": 1,
  "order_number": "#1048",
  "time": "13.02",
  "customer_name": "Alya Putri",
  "menu": "Nasi Goreng Kampung",
  "quantity": 2,
  "total_price": 56000,
  "status": "Baru",
  "notes": "Tidak pedas"
}
```

---

## 🚀 Panduan Memulai (Getting Started)

### 1. Prasyarat
Pastikan Anda sudah menginstal:
- **Node.js** (versi 18+ direkomendasikan)
- **Python 3.9+** (untuk menjalankan backend FastAPI)

### 2. Jalankan Backend FastAPI
```bash
# Masuk ke direktori backend (jika terpisah)
cd backend
# Jalankan uvicorn server
uvicorn main:app --reload --port 8000
```

### 3. Jalankan Frontend Vue 3
```bash
# Masuk ke folder frontend
cd frontend

# Install dependency
npm install

# Jalankan server pengembangan Vite
npm run dev
```

Aplikasi frontend dapat diakses di browser pada URL `http://localhost:3000` (atau URL yang ditampilkan pada terminal Vite).

---

## 🎨 Tema & Desain UI

Desain navy editorial: tanpa sudut membulat & tanpa bayangan, band warna bergantian per section.

- **Warna**: `primary` `#15283d` (judul, band gelap, tombol), `body` `#3e5166`, `muted` `#607791`,
  `surface-1` `#eef4f8`, `surface-2` `#e4f0f9`, `border` `#ccdce6`, `on-dark` `#c3d5e0`,
  `danger` `#f53838`. Didefinisikan sekali sebagai token di `@theme` (`frontend/src/style.css`).
- **Tipografi**: heading **Merriweather** (serif, bobot 400/700), teks & UI **Inter** — dimuat dari
  Google Fonts di `index.html`.
- **Layout band**: header & footer `primary` → hero putih → ringkasan `surface-1` → konten putih.
- **Eyebrow label**: uppercase Inter `15px` dengan `letter-spacing: .3em` di atas setiap judul section.
- **Bentuk**: radius `0` pada tombol/kartu/input (lingkaran hanya untuk avatar & ikon), garis `1px`,
  tanpa drop shadow, transisi halus `150–300ms`.
- **Tombol utama**: padding `10px 40px`, latar `primary`; saat hover teks bergeser kiri dan anak
  panah masuk (`UiButton.vue`).

---

## 👤 Penulis / Kelompok
- **WAD Group 4 - Kantinkampus**
- **Mata Kuliah**: Web Application Development (UTS)
