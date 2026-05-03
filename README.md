# Fertilizer SQL Factory

Alat otomatisasi untuk mengonversi dataset rekomendasi pupuk dari format CSV ke SQL Dump yang siap pakai. Alat ini dirancang untuk mempermudah migrasi data riset pertanian ke dalam sistem database relasional.

## Fitur Utama

- Otomatisasi Konversi: Mengubah ribuan baris data CSV menjadi perintah INSERT SQL dalam hitungan detik.
- ID Generator (CUID): Menggunakan cuid untuk menjamin keunikan ID di setiap baris data.
- Data Cleaning: Pembersihan otomatis nilai NULL dan pemetaan kolom agar sesuai dengan skema database modern.
- SQL Escaping: Penanganan karakter khusus (seperti tanda petik tunggal) untuk mencegah error SQL.
- Transactional Dump: Output SQL dibungkus dalam blok BEGIN dan COMMIT untuk menjamin integritas data.

## Struktur Proyek

```bash
.
├── data/
│   └── fertilizer_recommendation.csv  # Input dataset
├── sql_dump/
│   └── seed_data.sql                 # Output hasil konversi
├── csv2sql_factory.ipynb             # Notebook konversi utama
├── requirements.txt                  # Dependensi Python
├── .gitignore                        # Konfigurasi Git ignore
└── LICENSE                           # Lisensi Proyek
```

## Tutorial Setup Environment

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan kerja Anda:

### 1. Persiapan Python
Pastikan Anda sudah menginstal Python (versi 3.8 ke atas direkomendasikan). Cek dengan perintah:
```bash
python --version
```

### 2. Membuat Virtual Environment
Disarankan menggunakan virtual environment agar dependensi tidak bentrok dengan proyek lain:

**Linux / macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalasi Dependensi
Setelah virtual environment aktif, instal library yang dibutuhkan:
```bash
pip install -r requirements.txt
```

## Setup dan Menjalankan Jupyter Notebook

Karena konverter ini berbentuk file .ipynb, Anda perlu menjalankan server Jupyter:

### 1. Instalasi Jupyter
Jika Anda belum memiliki Jupyter, instal melalui pip:
```bash
pip install jupyter
```

### 2. Menjalankan Server
Jalankan perintah berikut di terminal:
```bash
jupyter notebook
```
Perintah ini akan membuka browser secara otomatis. Jika tidak, klik link yang muncul di terminal (biasanya http://localhost:8888).

### 3. Eksekusi Konverter
1. Di halaman utama Jupyter, pilih file `csv2sql_factory.ipynb`.
2. Pastikan file dataset sudah ada di folder `data/fertilizer_recommendation.csv`.
3. Pilih menu **Cell** -> **Run All** untuk menjalankan seluruh proses konversi.
4. Hasil SQL akan muncul di folder `sql_dump/seed_data.sql`.

## Skema Tabel Target

Data akan dimasukkan ke dalam tabel "soil_references" dengan struktur berikut:

| Kolom | Tipe Data | Deskripsi |
| :--- | :--- | :--- |
| id | VARCHAR | Unique ID (CUID) |
| soil_type | VARCHAR | Jenis Tanah |
| temperature | FLOAT | Suhu Lingkungan |
| humidity | FLOAT | Kelembapan |
| crop_type | VARCHAR | Jenis Tanaman |
| nitrogen | FLOAT | Kadar Nitrogen (N) |
| phosphorus | FLOAT | Kadar Fosfor (P) |
| potassium | FLOAT | Kadar Kalium (K) |
| ph | FLOAT | pH Tanah |
| organic_carbon | FLOAT | Karbon Organik |
| electrical_conductivity | FLOAT | Konduktivitas Listrik |
| rainfall | FLOAT | Curah Hujan |
| recommended_fertilizer | VARCHAR | Pupuk yang Direkomendasikan |

## Lisensi

Proyek ini dibuat untuk mendukung ekosistem pertanian digital Indonesia. Bebas digunakan untuk keperluan riset dan pengembangan sesuai dengan ketentuan Lisensi MIT.

---
Built by Lumbung Stack
