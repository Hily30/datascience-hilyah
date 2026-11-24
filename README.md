# 📚 EDA Penjadwalan Mata Kuliah

### Analisis jadwal dengan mempertimbangkan preferensi dosen dan mahasiswa

Proyek ini merupakan tahap awal penelitian **optimasi penjadwalan mata kuliah**. Exploratory Data Analysis (EDA) digunakan untuk memahami data, memeriksa potensi bentrok, mengevaluasi kapasitas ruang, dan mengukur kesesuaian preferensi sebelum model optimasi dikembangkan.

> **Penting:** seluruh data pada proyek ini adalah **data sintetis (dummy)**. Hasilnya tidak menggambarkan kondisi kampus tertentu. Aplikasi saat ini melakukan **audit jadwal**, belum menyusun jadwal baru atau menghasilkan solusi optimal.

---

## 📌 Ringkasan Proyek

| Komponen | Keterangan |
|---|---|
| Dataset | 600 baris jadwal sintetis, 14 kolom awal |
| Unit analisis | Satu baris mewakili satu pertemuan kelas mingguan |
| Sumber data | Dibuat dengan Python; seed `20261123` |
| Data yang dicakup | 18 mata kuliah, 72 dosen, 60 kelompok mahasiswa, 35 ruang |
| Analisis | Kualitas data, distribusi, pencilan, bentrok, kapasitas, preferensi |
| Aplikasi | Dashboard interaktif berbasis Python dan Streamlit |
| Tahap penelitian | EDA dan audit awal, **bukan optimasi** |

> Preferensi mahasiswa pada data dummy diwakili oleh **preferensi satu kelompok**, bukan preferensi tiap mahasiswa.

## 🧭 Daftar Isi

1. [Pendahuluan](#1-pendahuluan)
2. [Memahami Dataset](#2-memahami-dataset)
3. [Alur Analisis](#3-alur-analisis)
4. [Hasil EDA](#4-hasil-exploratory-data-analysis)
5. [Pengujian Aplikasi](#5-pengujian-aplikasi)
6. [Struktur Proyek](#6-struktur-proyek)
7. [Keterbatasan dan Pengembangan](#7-keterbatasan-dan-pengembangan)
8. [Daftar Pustaka](#8-daftar-pustaka)
9. [Tutorial Menjalankan Aplikasi](#9-tutorial-menjalankan-aplikasi)

---

## 1. Pendahuluan

### Latar belakang

Penjadwalan mata kuliah melibatkan dosen, kelompok mahasiswa, ruang, kapasitas, hari, dan waktu. Jadwal yang tidak diperiksa dapat menimbulkan **bentrok dosen atau ruangan**, ruangan yang terlalu kecil, serta waktu yang kurang sesuai dengan preferensi pengguna.

Penelitian penjadwalan merupakan masalah optimasi dengan kendala yang dapat berbeda antar institusi. Studi terdahulu membahas formulasi dan benchmark penjadwalan pendidikan [1], serta penggunaan preferensi dosen dan aturan ruang pada penjadwalan mata kuliah [2].

### Tujuan

1. Memahami struktur dan kualitas 600 data jadwal dummy.
2. Mengidentifikasi bentrok dosen, kelompok mahasiswa, dan ruang.
3. Memeriksa apakah kapasitas ruang mencukupi.
4. Mengukur kecocokan jadwal dengan preferensi yang tersedia.
5. Menyiapkan data dan metrik untuk tahap optimasi berikutnya.

### Jenis masalah dan metrik

Masalah utama termasuk **optimasi penjadwalan berbatas**, bukan otomatis masalah klasifikasi atau regresi. Target pada tahap optimasi nantinya adalah **nol bentrok** dan **nol pelanggaran kapasitas** sebagai kendala keras, sekaligus meningkatkan kesesuaian preferensi sebagai tujuan lunak. Target tersebut **belum diuji pada solusi optimasi** dalam proyek ini.

---

## 2. Memahami Dataset

### Sumber dan asumsi

Data dihasilkan oleh [`buat_data.py`](buat_data.py) dan disimpan dalam [`data/jadwal_dummy_600.csv`](data/jadwal_dummy_600.csv). Semua jadwal diasumsikan terjadi dalam satu minggu yang sama. Data dibuat secara acak tanpa menjamin jadwal layak, sehingga bentrok dan kekurangan kapasitas dapat muncul.

### Kolom utama

| Kolom | Keterangan |
|---|---|
| `id_jadwal` | Identitas unik jadwal |
| `kode_matakuliah`, `nama_matakuliah` | Kode dan nama mata kuliah |
| `sks` | Bobot mata kuliah: 2 atau 3 SKS |
| `id_dosen` | Identitas dosen fiktif |
| `id_kelompok` | Identitas kelompok mahasiswa fiktif |
| `jumlah_mahasiswa` | Jumlah mahasiswa dalam kelompok |
| `id_ruang`, `kapasitas_ruang` | Identitas dan kapasitas ruang |
| `hari`, `jam_mulai`, `jam_selesai` | Waktu pelaksanaan jadwal |
| `preferensi_dosen` | Preferensi periode dosen: Pagi, Siang, Sore, atau kosong |
| `preferensi_mahasiswa` | Preferensi periode kelompok: Pagi, Siang, Sore, atau kosong |

Dalam simulasi ini, **1 SKS = 50 menit**. Periode ditentukan berdasarkan **jam mulai**: Pagi sebelum 12.00, Siang 12.00–14.59, dan Sore mulai 15.00. Peraturan dan periode nyata harus disesuaikan dengan kebijakan kampus.

---

## 3. Alur Analisis

```text
Data dummy CSV
      ↓
Muat data dan periksa struktur
      ↓
Cek nilai kosong, duplikat, format, dan pencilan
      ↓
Analisis distribusi serta hubungan variabel
      ↓
Audit bentrok, kapasitas, dan preferensi
      ↓
Visualisasi, laporan, dan rekomendasi optimasi
```

| Tahap | Perangkat / keluaran |
|---|---|
| Membuat data | NumPy dan pandas; `buat_data.py` |
| Membaca dan menganalisis | pandas dan NumPy; `analisis.py` |
| Visualisasi | Matplotlib dan seaborn [6] |
| Audit interaktif | Streamlit; `app.py` |
| Pengujian | `unittest` dan Streamlit AppTest |
| Pelaporan | Dokumen Word, presentasi PPT, dan README |

---

## 4. Hasil Exploratory Data Analysis

Semua angka berikut merupakan **hasil simulasi**, bukan hasil survei atau evaluasi kampus nyata. Hasil dapat direproduksi dari dataset dan kode yang disertakan.

### 4.1 Kualitas data

| Pemeriksaan | Hasil |
|---|---:|
| Jumlah jadwal | 600 baris |
| Kolom awal | 14 kolom |
| Preferensi dosen kosong | 47 baris (7,83%) |
| Preferensi mahasiswa kosong | 46 baris (7,67%) |
| Kedua preferensi lengkap | 512 baris |
| Duplikat baris penuh | 0 |
| Waktu tidak valid | 0 |
| Durasi tidak sesuai asumsi SKS | 0 |

Nilai preferensi kosong **tidak diisi dengan tebakan** dan tidak dianggap sebagai tidak cocok. Kondisi data hilang perlu dievaluasi dengan mempertimbangkan proses pengumpulannya [4].

### 4.2 Distribusi jadwal

| Hari | Jumlah jadwal |
|---|---:|
| Senin | 124 |
| Selasa | 117 |
| Rabu | 114 |
| Kamis | 129 |
| Jumat | 116 |
| **Total** | **600** |

Berdasarkan jam mulai, ada **310 jadwal pagi**, **191 jadwal siang**, dan **99 jadwal sore**.

![Distribusi jadwal menurut hari dan periode](grafik/01_distribusi.png)

*Gambar 1. Distribusi jumlah jadwal berdasarkan hari dan periode mulai.*

### 4.3 Audit bentrok jadwal

| Sumber daya | Baris terlibat bentrok | Pasangan bentrok |
|---|---:|---:|
| Dosen | 252 | 161 |
| Kelompok mahasiswa | 305 | 211 |
| Ruang | 420 | 377 |

Secara keseluruhan, **530 dari 600 baris** (88,33%) terlibat dalam sedikitnya satu bentrok. Satu baris dapat mengalami lebih dari satu jenis bentrok, sehingga jumlah baris pada tiap jenis **tidak boleh dijumlahkan** sebagai total baris unik. Satu pasangan juga dapat muncul pada lebih dari satu jenis sumber daya.

**Aturan bentrok:** hari dan sumber daya sama, serta interval waktunya beririsan. Jika satu jadwal selesai tepat saat jadwal berikutnya mulai, keduanya tidak dianggap bentrok. Daftar rinci tersedia dalam [`hasil/daftar_bentrok.csv`](hasil/daftar_bentrok.csv).

![Bentrok dan preferensi](grafik/04_bentrok_preferensi.png)

*Gambar 2. Baris yang terlibat bentrok dan rata-rata skor preferensi menurut periode.*

### 4.4 Kapasitas ruang

Sebanyak **182 dari 600 jadwal** (30,33%) memiliki jumlah mahasiswa lebih banyak daripada kapasitas ruang. Sebagai contoh, `JDW0004` mencatat **37 mahasiswa** pada ruang berkapasitas **25**.

![Jumlah mahasiswa dan kapasitas ruang](grafik/05_kapasitas.png)

*Gambar 3. Titik di atas garis diagonal menunjukkan jumlah mahasiswa melebihi kapasitas ruang.*

### 4.5 Kecocokan preferensi

| Ukuran | Hasil | Jumlah baris yang dihitung |
|---|---:|---:|
| Preferensi dosen sesuai | 38,52% | 553 baris valid |
| Preferensi kelompok mahasiswa sesuai | 35,02% | 554 baris valid |
| Rata-rata skor gabungan | 37,40 / 100 | 512 baris lengkap |

**Skor gabungan simulasi:** 50 poin jika periode mulai cocok dengan preferensi dosen, ditambah 50 poin jika cocok dengan preferensi kelompok. Skor hanya dihitung saat kedua preferensi tersedia. Bobot 50:50 merupakan **asumsi**, bukan hasil kesepakatan atau survei.

### 4.6 Pencilan dan korelasi

- Sebanyak **27 jadwal 2 SKS** ditandai sebagai pencilan statistik karena mayoritas jadwal memiliki 3 SKS. Nilai 2 SKS tetap **dipertahankan** karena valid dalam desain data.
- Korelasi Pearson antara SKS dan durasi adalah **1,00**, karena durasi memang dihitung dengan rumus `50 × SKS`. Ini adalah hubungan akibat desain data, **bukan penemuan sebab-akibat**.
- Statistik dihitung per jadwal; dosen, kelompok, dan ruang dapat muncul berulang, sehingga baris bukan sampel individu yang sepenuhnya independen.

---

## 5. Pengujian Aplikasi

Pada pengujian yang disertakan, **6 dari 6 uji logika lulus**. Pengujian mencakup:

- Bentrok dengan interval beririsan dan interval yang hanya bersentuhan.
- Pemeriksaan waktu tidak valid dan preferensi kosong.
- Konsistensi 600 baris dan contoh pasangan bentrok.
- Contoh kapasitas ruang dan perhitungan skor preferensi.
- Uji dashboard otomatis dengan **Streamlit AppTest**, termasuk filter hari Senin.

Bukti eksekusi: [`hasil/hasil_pengujian.txt`](hasil/hasil_pengujian.txt) dan [`hasil/hasil_pengujian.json`](hasil/hasil_pengujian.json). Ini merupakan pengujian terbatas, bukan jaminan sistem bebas kesalahan, bukan uji seluruh fitur unggah, dan bukan uji hasil optimasi.

---

## 6. Struktur Proyek

```text
jadwal_eda/
├── data/
│   └── jadwal_dummy_600.csv
├── grafik/                    # Grafik hasil EDA
├── hasil/                     # Ringkasan dan keluaran audit/pengujian
├── app.py                     # Dashboard Streamlit
├── analisis.py                # Analisis dan audit data
├── buat_data.py               # Generator dataset dummy
├── test_analisis.py           # Uji logika
├── verifikasi.py              # Uji logika dan AppTest
├── buat_laporan.py            # Generator laporan Word
├── buat_presentasi.py         # Generator presentasi
├── requirements.txt           # Pustaka Python
├── Laporan_EDA_Penjadwalan.docx
├── Presentasi_EDA_Penjadwalan.pptx
└── README.md
```

- [Laporan EDA (Word)](Laporan_EDA_Penjadwalan.docx)
- [Presentasi EDA (PPT)](Presentasi_EDA_Penjadwalan.pptx)
- [Dataset dummy (CSV)](data/jadwal_dummy_600.csv)
- [Hasil audit per jadwal](hasil/jadwal_hasil_cek.csv)



---

## 7. Keterbatasan dan Pengembangan

### Keterbatasan

- Seluruh data dan identitas dibuat secara sintetis dan tidak mewakili kampus tertentu.
- Preferensi mahasiswa masih diwakili kelompok, bukan preferensi setiap individu.
- Belum mencakup ketersediaan aktual dosen/ruang, fasilitas laboratorium, kalender, atau mahasiswa lintas kelompok.
- Bobot preferensi dan asumsi 1 SKS = 50 menit belum disesuaikan dengan peraturan institusi.
- Belum ada algoritma optimasi, pembandingan solusi sebelum–sesudah, atau sertifikat optimalitas.

### Rencana tahap selanjutnya

1. Mengumpulkan data nyata secara sah dan menjaga privasi.
2. Menetapkan ketersediaan, kapasitas, aturan, serta bobot preferensi bersama pemangku kepentingan.
3. Mengembangkan kandidat model **CP-SAT atau mixed-integer linear programming**.
4. Menguji kendala keras, skor preferensi, pemerataan antarkelompok, waktu komputasi, dan status solusi.
5. Membandingkan jadwal awal dengan hasil optimasi pada data dan aturan yang sama.

---

## 8. Daftar Pustaka

[1] S. Ceschia, L. Di Gaspero, dan A. Schaerf, “Educational timetabling: Problems, benchmarks, and state-of-the-art results,” *European Journal of Operational Research*, vol. 308, no. 1, pp. 1–18, 2023. [https://doi.org/10.1016/j.ejor.2022.07.011](https://doi.org/10.1016/j.ejor.2022.07.011).

[2] A. Ozkan, A. Ulucan, C. Dirik, dan K. B. Atici, “University course timetabling with multi-section courses, room stability and lecturer preferences: an application in a business school,” *Computational Management Science*, vol. 22, art. 3, 2025. [https://doi.org/10.1007/s10287-025-00529-2](https://doi.org/10.1007/s10287-025-00529-2).

[3] R. Lewis, “A survey of metaheuristic-based techniques for university timetabling problems,” *OR Spectrum*, vol. 30, pp. 167–190, 2008. [https://doi.org/10.1007/s00291-007-0097-0](https://doi.org/10.1007/s00291-007-0097-0).

[4] J. A. C. Sterne et al., “Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls,” *BMJ*, vol. 338, b2393, 2009. [https://doi.org/10.1136/bmj.b2393](https://doi.org/10.1136/bmj.b2393).

[5] S. Kapoor dan A. Narayanan, “Leakage and the reproducibility crisis in machine-learning-based science,” *Patterns*, vol. 4, no. 9, 100804, 2023. [https://doi.org/10.1016/j.patter.2023.100804](https://doi.org/10.1016/j.patter.2023.100804).

[6] M. L. Waskom, “seaborn: statistical data visualization,” *Journal of Open Source Software*, vol. 6, no. 60, 3021, 2021. [https://doi.org/10.21105/joss.03021](https://doi.org/10.21105/joss.03021).

---

---

## 9. Tutorial Menjalankan Aplikasi

### Persiapan

- Python **3.10 atau lebih baru** dan koneksi internet untuk menginstal pustaka.
- Visual Studio Code atau terminal/Command Prompt.
- Salinan proyek yang sudah diekstrak dari ZIP atau diunduh dari GitHub.

### A. Windows — VS Code / Command Prompt

1. Buka folder proyek di VS Code, lalu buka **Terminal → New Terminal**.
2. Masuk ke folder yang berisi `app.py` dan `requirements.txt`. Jika terminal berada pada folder induknya:

```cmd
cd jadwal_eda
```

3. Buat dan aktifkan lingkungan virtual **sekali saja untuk pembuatan**:

```cmd
python -m venv .venv
.venv\Scripts\activate
```

4. Instal pustaka:

```cmd
python -m pip install -r requirements.txt
```

5. Jalankan aplikasi:

```cmd
python -m streamlit run app.py
```

6. Buka alamat yang muncul di terminal, biasanya **http://localhost:8501**. Untuk menghentikan aplikasi, tekan **Ctrl + C** di terminal.

> Jika sudah memiliki `.venv` yang aktif—ditandai `(.venv)` pada terminal—tidak perlu membuatnya lagi. Pastikan terminal tetap berada di folder yang berisi `app.py` dan `requirements.txt`.

### B. macOS / Linux

Dari folder proyek yang berisi `app.py`:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### C. Cara memakai dashboard

1. **Data awal:** aplikasi langsung memuat 600 jadwal dummy; unggah CSV hanya jika ingin mencoba data lain.
2. **Filter:** pilih hari dan periode pada panel kiri. Filter mengubah jadwal yang ditampilkan, bukan menghapus data.
3. **Total seluruh jadwal:** menunjukkan jumlah seluruh baris dataset, tidak dipengaruhi filter.
4. **Jadwal ditampilkan:** menunjukkan jumlah baris yang cocok dengan filter. Contoh: Senin–Kamis menghasilkan 484 baris, sementara total tetap 600.
5. **Data & kualitas:** lihat tabel dan unduh hasil yang terfilter.
6. **Daftar bentrok:** melihat dan mengunduh pasangan bentrok **seluruh dataset**. Deteksi bentrok dilakukan sebelum filter; suatu jadwal dapat ditandai bentrok dengan jadwal yang tersembunyi oleh filter.

> **Penting:** metrik bentrok, kapasitas, dan skor di bagian atas mengikuti baris yang ditampilkan; hanya **total seluruh jadwal** yang tidak berubah karena filter. Jika mengunggah dataset lain, total mengikuti jumlah baris dataset tersebut.

### D. Menjalankan analisis dan pengujian secara manual

Dari folder yang berisi `analisis.py`:

```bash
python analisis.py
python -m unittest -v test_analisis
```

Perintah pertama menulis ulang keluaran EDA di `hasil/` dan grafik di `grafik/`. Tes unit tambahan dapat dijalankan melalui `python verifikasi.py`, termasuk AppTest; hasilnya disimpan pada `hasil/hasil_pengujian.json` dan `.txt`.

**Hati-hati:** `python buat_data.py` membuat ulang dataset dummy; `python buat_laporan.py` dan `python buat_presentasi.py` membuat ulang dokumen dan dapat menimpa perubahan manual. Salin hasil Anda sebelum menjalankan perintah-perintah tersebut.

### Jika terjadi error

| Masalah | Yang perlu diperiksa |
|---|---|
| `can't open file ... app.py` | Terminal harus berada di folder yang berisi `app.py`: gunakan `cd jadwal_eda` jika berada satu tingkat di atasnya. |
| `Could not open requirements file` | Pastikan `requirements.txt` ada di folder terminal saat ini. |
| `No module named streamlit` | Aktifkan lingkungan yang benar, lalu jalankan `python -m pip install -r requirements.txt`. |
| Browser tidak terbuka | Buka alamat yang dicetak Streamlit di terminal, biasanya `http://localhost:8501`. |
| Total tampak berkurang | Lihat perbedaan **total seluruh jadwal** dan **jadwal ditampilkan**; periksa filter hari dan periode. |

---

### E. Menjalankan di Google Colab

Notebook [`EDA_Penjadwalan_Colab.ipynb`](../EDA_Penjadwalan_Colab.ipynb) menyediakan langkah menjalankan proyek melalui Colab:

1. Unggah file ZIP proyek bernama `Proyek_EDA_Penjadwalan.zip` ke folder utama **Drive Saya**.
2. Buka notebook di [Google Colab](https://colab.research.google.com/) melalui **File → Buka notebook → Upload**.
3. Jalankan sel secara berurutan dan izinkan akses Google Drive.
4. Ekstrak proyek, instal pustaka, kemudian jalankan analisis dan pengujian.
5. Ikuti sel penyimpanan hasil agar keluaran disalin kembali ke Drive.

Notebook ini **belum langsung mengambil data dari GitHub**: ZIP tetap diperlukan di Google Drive. Struktur ZIP yang diharapkan memiliki folder `jadwal_eda` langsung di dalam ZIP. Jika ZIP memiliki folder tambahan di atasnya, sesuaikan lokasi folder sebelum menjalankan analisis. Tampilan Streamlit di iframe Colab dapat bergantung pada sesi dan browser; menjalankannya secara lokal di VS Code adalah alternatif.

Runtime Colab bersifat sementara. Salin hasil ke Google Drive sebelum sesi berakhir dan berhati-hati saat membagikan data riil.

---

**Identitas penyusun:** Hilyah Haula Salsabiila, 26MA41D010, DATA SCIENCE, MAGISTER ILMU KOMPUTER, dan UNIVERSITAS AMIKOM PURWOKERTO.
