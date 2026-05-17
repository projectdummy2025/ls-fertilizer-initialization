# Prototipe Sistem Rekomendasi Pupuk Presisi Berbasis Kesehatan Tanah

> **Decision Support System (DSS)** untuk mengatasi Inefisiensi Penggunaan Pupuk Bersubsidi & Degradasi Tanah di Indonesia.

---

## Problem Statement
Petani kecil sering menggunakan pupuk secara umum (misal: hanya Urea) tanpa melihat kondisi tanah dan kadar unsur hara (pH, N, P, K). Hal ini menyebabkan:
*   **Tanah Menjadi Asam:** Kerusakan struktur tanah jangka panjang.
*   **Biaya Membengkak:** Penggunaan pupuk yang tidak efisien menghabiskan modal.
*   **Hasil Panen Tidak Maksimal:** Nutrisi tidak sesuai dengan kebutuhan tanaman.

**Solusi:** Sebuah alat berbasis web di mana pengguna memasukkan kondisi tanah, unsur hara, & tanaman, dan sistem memberikan rekomendasi jenis pupuk yang *tepat* beserta estimasi penghematan biaya.

---

## Fitur Utama (MVP)
1.  **Input Kondisi Tanah & Unsur Hara:** Parameter pH, kelembapan, suhu, serta kadar Nitrogen (N), Fosfor (P), dan Kalium (K).
2.  **Smart Prediction:** Menggunakan model Machine Learning (Random Forest) untuk menentukan rekomendasi pupuk terbaik.
3.  **Soil Health Status:** Identifikasi otomatis status tanah (Asam/Normal/Basa).
4.  **Business Intelligence:** Estimasi biaya pemupukan per kg untuk membantu perencanaan anggaran petani.

---

## Tech Stack
*   **Language:** Python 3.8+
*   **Framework:** [Streamlit](https://streamlit.io/) (Web UI)
*   **ML Libraries:** Scikit-Learn, Pandas, NumPy
*   **Modeling:** Random Forest Classifier

---

## Panduan Instalasi & Setup

Ikuti langkah-langkah berikut untuk menyiapkan lingkungan kerja Anda:

### 1. Membuat Virtual Environment
Disarankan menggunakan *virtual environment* agar dependensi tidak bentrok dengan proyek lain:

**Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Instalasi Dependensi
Setelah masuk ke *environment*, instal library yang diperlukan:
```bash
pip install -r requirements.txt
```

---

## Rencana Pengembangan

| Hari | Fokus | Tugas Utama |
| :--- | :--- | :--- |
| **1** | **Data Prep** | Cleaning & Lokalisasi Musim (Hujan/Kemarau). |
| **2** | **EDA** | Analisis korelasi pH & nutrisi terhadap jenis pupuk. |
| **3** | **Modeling** | Training model Random Forest/XGBoost. |
| **4** | **Logic Biz** | Integrasi sistem peringatan kesehatan tanah (pH warning). |
| **5** | **Dev UI** | Pembangunan interface Streamlit yang intuitif. |
| **6** | **Testing** | Uji coba dengan data dummy & validasi logika. |
| **7** | **Deploy** | Deployment ke Streamlit Cloud & Finalisasi Dokumentasi. |

---

## Implementasi Teknis

### 1. Training Model
Sistem menggunakan `Random Forest Classifier` untuk memproses input numerik dan kategorikal. 
### 2. Logika Keputusan
Selain prediksi ML, sistem menyertakan *business rules*:
- Jika `pH < 5.5`: Peringatan tanah terlalu asam & saran pengapuran.
- Jika `pH > 7.5`: Peringatan tanah terlalu basa & saran penggunaan pupuk asam (ZA).

---

## Roadmap & Rencana Mendatang
Untuk meningkatkan nilai praktis bagi petani di lapangan, rencana pengembangan selanjutnya meliputi:
1.  **Local Brand Mapping:** Mengintegrasikan database pupuk komersial Indonesia (misal: Phonska, Mutiara, Nitrea) agar rekomendasi merujuk pada produk nyata di pasar, bukan sekadar istilah kimia.
2.  **Kalkulator Dosis Presisi:** Menambahkan fitur penghitungan jumlah karung pupuk yang harus dibeli berdasarkan luas lahan pengguna (Hektar/Are).
3.  **Integrasi Harga Dinamis:** Menghubungkan sistem dengan referensi Harga Eceran Tertinggi (HET) pupuk bersubsidi dan harga pasar non-subsidi untuk perencanaan anggaran yang lebih akurat.

---

## Disclaimer & Risiko
*   **Lokalisasi Data:** Dataset saat ini memerlukan kalibrasi ulang untuk karakteristik tanah vulkanik spesifik di Indonesia (Data Balits Tanah).
*   **Variabel Eksternal:** Belum memperhitungkan harga pupuk dinamis di pasar lokal.
*   **Validasi:** Rekomendasi sistem tetap disarankan untuk dikonsultasikan dengan penyuluh pertanian setempat.

---
**Built with love by Lumbung Stack Team**
