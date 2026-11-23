"""Membuat data fiktif yang dapat direproduksi: 600 kelas/penugasan."""
from pathlib import Path
import itertools
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
rng = np.random.default_rng(20261123)
hari = ['Senin','Selasa','Rabu','Kamis','Jumat']
mulai = [420, 520, 620, 780, 880, 980]
slot = lambda m: 'Pagi' if m < 720 else 'Siang' if m < 900 else 'Sore'
waktu = lambda m: f'{m//60:02d}:{m%60:02d}'
matkul = ['Algoritma dan Pemrograman','Basis Data','Struktur Data','Statistika','Kalkulus','Aljabar Linear','Rekayasa Perangkat Lunak','Jaringan Komputer','Sistem Operasi','Kecerdasan Buatan','Data Mining','Pembelajaran Mesin','Pemrograman Web','Keamanan Informasi','Interaksi Manusia Komputer','Analisis dan Desain Sistem','Komputer Vision','Sains Data']
sks = [3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,3,3,3]
dosen = [f'DSN{i:03}' for i in range(1,73)]
kelompok = [f'KLP{i:03}' for i in range(1,61)]
ruang = [f'R{i:02}' for i in range(1,36)]
kapasitas = {r:int(rng.choice([25,30,35,40,45,50,60])) for r in ruang}
jumlah = {k:int(rng.integers(20,51)) for k in kelompok}
preferensi = ['Pagi','Siang','Sore']
pdosen = {d:rng.choice(preferensi,p=[.50,.35,.15]) for d in dosen}
pmahasiswa = {k:rng.choice(preferensi,p=[.35,.45,.20]) for k in kelompok}
for d in rng.choice(dosen, 5, replace=False): pdosen[d] = None
for k in rng.choice(kelompok, 4, replace=False): pmahasiswa[k] = None
# Mata kuliah mempunyai 4 dosen pengampu kandidat; kombinasi matkul-kelompok unik.
semua = list(itertools.product(range(len(matkul)),kelompok))
pilih = rng.choice(len(semua),size=600,replace=False)
rows = []
for i,p in enumerate(pilih,1):
    c,k = semua[p]; d = rng.choice(dosen[4*c:4*c+4]); r = rng.choice(ruang)
    start = int(rng.choice(mulai)); end = start + sks[c]*50
    rows.append(dict(id_jadwal=f'JDW{i:04}',kode_matakuliah=f'MK{c+1:02}',nama_matakuliah=matkul[c],sks=sks[c],id_dosen=d,id_kelompok=k,jumlah_mahasiswa=jumlah[k],id_ruang=r,kapasitas_ruang=kapasitas[r],hari=rng.choice(hari),jam_mulai=waktu(start),jam_selesai=waktu(end),preferensi_dosen=pdosen[d],preferensi_mahasiswa=pmahasiswa[k]))
df = pd.DataFrame(rows)
(ROOT/'data').mkdir(exist_ok=True)
df.to_csv(ROOT/'data/jadwal_dummy_600.csv',index=False,encoding='utf-8-sig')
print('Data dibuat:', df.shape)
