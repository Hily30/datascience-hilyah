# Proyek EDA — Penjadwalan Mata Kuliah

Prototipe akademik untuk memeriksa 600 baris jadwal **sintetis**, bukan data riil atau hasil optimasi. Satu baris = satu pertemuan mingguan kelas (satu mata kuliah dan satu kelompok), semua baris dianggap terjadi pada minggu akademik yang sama. Dosen, kelompok, ruang, kapasitas, dan preferensi dibuat fiktif dan konsisten per identitas. Bobot preferensi dosen dan kelompok adalah contoh (50:50). Preferensi mahasiswa diwakili satu preferensi kelompok, bukan survei individu.

## Cara menjalankan

Python 3.10+ dan terminal pada folder ini:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python buat_data.py             # opsional: buat ulang data mentah dengan seed tetap
python analisis.py              # buat hasil, tabel dan grafik
python -m unittest -v test_analisis
python verifikasi.py           # uji logika dan AppTest; simpan hasil aktual
python buat_laporan.py         # buat laporan dari hasil analisis dan pengujian
python buat_presentasi.py      # buat presentasi dan catatan pembicara
streamlit run app.py            # buka URL yang ditampilkan oleh Streamlit
```

Data dapat dibuka melalui menu unggah aplikasi. Dataset pengganti harus berisi semua kolom contoh; hari Senin–Jumat; format waktu HH:MM 24 jam; SKS 2/3 dan satu SKS diasumsikan 50 menit; preferensi Pagi, Siang, Sore atau kosong. Waktu berakhir di hari yang sama. Periode ditentukan dari **jam mulai**: pagi sebelum 12:00, siang 12:00–14:59, sore mulai 15:00. Output default ada di `hasil/` dan grafik di `grafik/`. Jalankan `python analisis.py`, lalu `python verifikasi.py`, kemudian `python buat_laporan.py` untuk membangun ulang laporan. Bukti pengujian aktual tersimpan dalam `hasil/hasil_pengujian.json` dan `hasil/hasil_pengujian.txt`; laporan tidak akan dibuat ulang jika uji gagal atau hasil verifikasi belum ada.

## Definisi pemeriksaan
- Bentrok: interval `[mulai, selesai)` saling tumpang tindih pada hari dan sumber daya yang sama: dosen, kelompok atau ruang. Satu baris bisa terlibat pada beberapa pasangan/jenis; jumlah baris dan jumlah pasangan tidak sama. Filter dashboard tidak mengubah perhitungan bentrok global.
- Kapasitas: `jumlah_mahasiswa > kapasitas_ruang`. Waktu dan kapasitas invalid diberi flag; hasil hitungan bentrok tidak dapat menjamin kelayakan jika input tidak valid.
- Kecocokan preferensi: cocok bila periode mulai sama dengan preferensi. Preferensi hilang tidak diperkirakan atau dianggap tidak cocok. Skor 0/50/100 dihitung hanya jika **kedua** preferensi tersedia; nilai adalah jumlah 50 poin per pihak yang cocok.
- `hasil/daftar_bentrok.csv` mencatat pasangan per jenis; satu pasangan dapat muncul lebih dari sekali jika berbagi beberapa sumber daya.

## Keterbatasan
Data ini diacak tanpa logika penyusunan jadwal layak, sengaja bisa menghasilkan banyak bentrok dan kapasitas kurang. Angka tidak boleh diklaim sebagai temuan universitas mana pun. Preferensi kelompok tidak mewakili setiap mahasiswa dan kelas bersama/mahasiswa lintas kelompok tidak dimodelkan. Tidak ada perhitungan solusi optimum, baseline optimasi, atau uji data aktual. Untuk pengembangan gunakan CP-SAT/MILP dengan pembatas keras dan tujuan lunak sebagaimana dijelaskan dalam laporan. Periksa kerahasiaan dan persetujuan bila menggunakan data nyata. Catat peraturan akademik setempat sebelum menggunakan asumsi SKS.
