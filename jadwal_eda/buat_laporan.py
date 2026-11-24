from pathlib import Path
import json
import numpy as np
import pandas as pd
from docx import Document
from docx.shared import Inches,Pt,RGBColor,Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from analisis import load_data,cek_dan_tambah

R=Path(__file__).resolve().parent
m=json.loads((R/'hasil/ringkasan.json').read_text(encoding='utf-8'))
raw=load_data(); df,pairs=cek_dan_tambah(raw)
doc=Document();sec=doc.sections[0];sec.top_margin=Cm(2.25);sec.bottom_margin=Cm(2.15);sec.left_margin=Cm(2.8);sec.right_margin=Cm(2.4)
style=doc.styles['Normal'];style.font.name='Calibri';style.font.size=Pt(10.5);style.paragraph_format.space_after=Pt(5);style.paragraph_format.line_spacing=1.15
for st in ['Title','Heading 1','Heading 2']:
 doc.styles[st].font.name='Calibri';doc.styles[st].font.color.rgb=RGBColor.from_string('15545B')
footer=sec.footer.paragraphs[0];footer.alignment=WD_ALIGN_PARAGRAPH.RIGHT
footer.add_run('EDA PENJADWALAN • DATA SINTETIS  |  ')
fld=OxmlElement('w:fldSimple');fld.set(qn('w:instr'),'PAGE');footer._p.append(fld)
def p(s='',bold=False):
 q=doc.add_paragraph();q.add_run(s).bold=bold;return q
def heading(s,l=1):doc.add_heading(s,level=l)
def table(headers,rows):
 t=doc.add_table(rows=1,cols=len(headers));t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for c,v in zip(t.rows[0].cells,headers):c.text=str(v)
 for row in rows:
  for c,v in zip(t.add_row().cells,row):c.text=str(v)
 for row in t.rows:
  for cell in row.cells:
   for para in cell.paragraphs:
    for run in para.runs:run.font.size=Pt(9)
 doc.add_paragraph()
def fig(name,caption):
 doc.add_picture(str(R/'grafik'/name),width=Inches(6.15)); q=doc.add_paragraph(caption);q.alignment=WD_ALIGN_PARAGRAPH.CENTER
 for r in q.runs:r.italic=True;r.font.size=Pt(9)
def bullet(s):doc.add_paragraph(s,style='List Bullet')
def fmt(x):return f'{x:,.2f}'.replace(',','X').replace('.',',').replace('X','.')

doc.add_paragraph('\n\n')
q=doc.add_paragraph();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=q.add_run('LAPORAN\nEXPLORATORY DATA ANALYSIS');r.bold=True;r.font.size=Pt(23);r.font.color.rgb=RGBColor.from_string('15545B')
q=doc.add_paragraph('Optimasi Penjadwalan Mata Kuliah dengan Pertimbangan Preferensi Dosen dan Mahasiswa');q.alignment=WD_ALIGN_PARAGRAPH.CENTER
for x in q.runs:x.bold=True;x.font.size=Pt(16)
p('\n')
q=doc.add_paragraph('PROTOTIPE PENELITIAN • 600 JADWAL SINTETIS');q.alignment=WD_ALIGN_PARAGRAPH.CENTER
q=doc.add_paragraph('Nama: ........................................................\nNIM: ............................................................\nProgram Studi: ...............................................\nInstitusi: .........................................................\nTahun: 2026');q.alignment=WD_ALIGN_PARAGRAPH.CENTER
p('\nCatatan: Seluruh data, entitas, hasil dan angka dalam laporan ini adalah simulasi. Tidak menggambarkan kondisi kampus tertentu dan belum merupakan hasil optimasi.',True)
doc.add_page_break()
heading('Ringkasan Eksekutif')
p(f"Analisis mengevaluasi {m['baris']} jadwal mingguan fiktif yang mencakup {m['mata_kuliah']} mata kuliah, {m['dosen']} dosen, {m['kelompok']} kelompok mahasiswa, dan {m['ruang']} ruang. Jadwal dibentuk secara acak sebagai baseline yang belum layak, sehingga bentrok dan kelebihan kapasitas memang mungkin terjadi.")
p(f"Sebanyak {m['bentrok_baris_total']} baris ({fmt(m['bentrok_baris_total']/6)}%) terlibat dalam sedikitnya satu bentrok; {m['kapasitas_kurang']} baris ({fmt(m['kapasitas_kurang']/6)}%) memiliki mahasiswa lebih banyak daripada kapasitas ruang. Kecocokan preferensi dosen {fmt(m['cocok_dosen_persen'])}% dari {m['preferensi_dosen_valid_n']} baris valid dan mahasiswa {fmt(m['cocok_mahasiswa_persen'])}% dari {m['preferensi_mahasiswa_valid_n']} baris valid. Skor rata-rata gabungan {fmt(m['rata_skor_keselarasan'])}/100 dihitung pada {m['preferensi_keduanya_valid_n']} baris dengan kedua preferensi terisi.")
p('Laporan ini mendokumentasikan EDA dan audit aturan, bukan pembangunan atau pembuktian solusi optimal. Tahap berikutnya adalah mengumpulkan data nyata yang sah, memformulasikan kendala, dan menguji algoritma optimasi.')
heading('Bab 1. Pendahuluan dan Memahami Masalah')
heading('1.1 Latar belakang dan tujuan',2)
p('Penjadwalan mata kuliah harus mempertemukan kebutuhan dosen, kelompok mahasiswa, ruang, dan waktu. Penempatan acak dapat menimbulkan jadwal bertumpuk, ruang yang terlalu kecil, dan waktu yang tidak sesuai dengan preferensi. Penelitian ini mengkaji data jadwal contoh sebelum merancang sistem optimasi penjadwalan.')
p('Tujuan EDA: memeriksa struktur dan kualitas data, mengidentifikasi potensi pelanggaran sumber daya dan kapasitas, mengukur kecocokan preferensi yang tersedia, serta merumuskan kebutuhan data dan metrik optimasi.')
heading('1.2 Tipe masalah',2)
p('Permasalahan utama adalah optimasi kombinatorial berbatas (constraint-based timetabling), bukan otomatis klasifikasi, regresi, atau klasterisasi [1], [3]. EDA menggunakan perhitungan deskriptif dan aturan audit; klasifikasi atau regresi dapat menjadi studi tambahan bila ada target dan alasan yang tepat. Penelitian penjadwalan universitas juga mempertimbangkan preferensi waktu dosen bersama aturan kelas dan ruang [2].')
heading('1.3 Metrik keberhasilan',2)
bullet('Kendala keras: target 0 pasangan bentrok dosen, kelompok, dan ruang; 0 penugasan ruang yang tidak mencukupi; semua durasi/waktu valid. Target ini baru dinilai setelah ada solusi jadwal.')
bullet('Kendala lunak: memaksimalkan persentase kecocokan dosen dan mahasiswa dan/atau skor preferensi gabungan. Bobot 50:50 adalah asumsi simulasi, bukan kesepakatan pemangku kepentingan.')
bullet('Laporkan cakupan preferensi yang diketahui, jumlah baris dan pasangan bentrok, waktu komputasi, serta pemerataan per kelompok; bandingkan baseline dan hasil optimasi pada aturan serta data yang sama.')
heading('Bab 2. Memahami Data')
heading('2.1 Pengumpulan dan sumber data',2)
p('Dataset dibuat menggunakan Python (NumPy dan pandas), dengan seed 20261123, dan disimpan sebagai data/jadwal_dummy_600.csv. Kombinasi mata kuliah dan kelompok diambil tanpa pengulangan; dosen kandidat ditetapkan per mata kuliah; setiap kelompok, ruang dan dosen memiliki atribut tetap. Hari, waktu, dosen kandidat dan ruang dipilih secara acak. Tidak ada data eksternal, survei, maupun data kampus riil.')
p('Unit analisis adalah satu pertemuan mingguan kelas, bukan 600 mahasiswa dan bukan 600 semester. Seluruh baris diasumsikan dalam minggu yang sama. Kelompok mewakili kelas mahasiswa yang sama pada semua mata kuliah; keterlibatan mahasiswa lintas kelompok belum direpresentasikan.')
heading('2.2 Struktur dan kamus data',2)
p(f"Dataset mentah memiliki {m['baris']} baris dan {m['kolom_awal']} kolom, disimpan sebagai CSV UTF-8. Contoh lima baris dapat dilihat di aplikasi atau pada berkas CSV mentah.")
table(['Kolom','Makna / tipe'],[
('id_jadwal','ID unik jadwal; teks'),('kode_matakuliah, nama_matakuliah','Identitas dan nama mata kuliah; teks'),('sks','Bobot SKS; bilangan bulat, 2 atau 3'),('id_dosen, id_kelompok','ID dosen dan kelompok mahasiswa; teks'),('jumlah_mahasiswa','Jumlah anggota kelompok; bilangan bulat'),('id_ruang, kapasitas_ruang','ID dan kapasitas ruang; teks dan bilangan bulat'),('hari, jam_mulai, jam_selesai','Hari kerja dan waktu 24 jam HH:MM'),('preferensi_dosen, preferensi_mahasiswa','Periode pilihan Pagi/Siang/Sore; boleh kosong')])
heading('2.3 Peninjauan kualitas dan eksplorasi awal',2)
p(f"Preferensi dosen kosong {m['missing']['preferensi_dosen']} baris ({fmt(m['missing']['preferensi_dosen']/6)}%); preferensi mahasiswa kosong {m['missing']['preferensi_mahasiswa']} baris ({fmt(m['missing']['preferensi_mahasiswa']/6)}%). Semua kolom lain lengkap. Tidak terdapat duplikat baris penuh, ID jadwal duplikat, atau kombinasi mata kuliah–kelompok duplikat. Tidak ada waktu invalid atau durasi yang melanggar asumsi 50 menit per SKS.")
p(f"Kapasitas kurang pada {m['kapasitas_kurang']} dari 600 baris; ini adalah pelanggaran terhadap kendala, bukan nilai hilang. Bentrok dihitung melalui interval aktual, bukan sekadar jam mulai sama. Distribusi dan grafik hubungan disajikan pada Bab 5–7.")
heading('2.4 Penyelarasan kebutuhan',2)
p('Data sudah memadai untuk simulasi audit sederhana, tetapi belum untuk penerapan nyata. Diperlukan ketersediaan dosen per hari dan slot, pendaftaran mahasiswa individual, kapasitas dan fasilitas ruang, kalender akademik, aturan jam istirahat, kebutuhan laboratorium, waktu perjalanan, serta bobot preferensi yang disepakati. Privasi dan izin penggunaan data harus dipastikan.')
heading('Bab 3. Memuat dan Memeriksa Data')
heading('3.1 Library dan proses',2)
p('Python menggunakan pandas untuk pembacaan dan pengolahan, NumPy untuk simulasi dan perhitungan, matplotlib/seaborn untuk grafik [6], serta Streamlit untuk aplikasi. Contoh pemuatan:')
q=doc.add_paragraph('import pandas as pd\ndf = pd.read_csv("data/jadwal_dummy_600.csv")\nprint(df.shape, df.dtypes, df.head())');q.style='Normal'
for x in q.runs:x.font.name='Consolas';x.font.size=Pt(9)
heading('3.2 Dimensi, tipe, dan pemeriksaan awal',2)
p(f"Hasil pemeriksaan: df.shape = ({m['baris']}, {m['kolom_awal']}); nilai SKS, jumlah dan kapasitas dibaca sebagai numerik; ID, nama, hari, waktu serta preferensi sebagai teks. Waktu dikonversi secara ketat ke menit untuk audit, tanpa mengasumsikan pergantian hari. Tidak ada pembagian train/test karena belum ada model prediktif atau optimasi yang dilatih.")
heading('Bab 4. Penanganan Data yang Hilang')
heading('4.1 Identifikasi',2)
table(['Kolom','Jumlah kosong','Persentase'],[(k,v,f'{fmt(v/6)}%') for k,v in m['missing'].items() if v])
p('Sebanyak 88 baris kehilangan minimal satu preferensi; 512 baris memiliki keduanya. Nilai kosong muncul karena 5 ID dosen dan 4 kelompok dibuat tanpa preferensi; beberapa jadwal mewarisi nilai kosong dari ID yang sama.')
fig('03_missing_korelasi.png','Gambar 1. Nilai kosong per kolom dan korelasi Pearson variabel numerik.')
heading('4.2 Mekanisme dan strategi',2)
p('Dalam simulasi, ID yang preferensinya dikosongkan dipilih secara acak dengan seed tetap. Nilai hilang berkelompok menurut entitas, sehingga baris tidak independen. Pada data nyata, mekanisme MCAR/MAR/MNAR tidak dapat dipastikan hanya dengan observasi; perlu menyelidiki proses pengumpulan data.')
p('Tidak ada baris atau kolom yang dihapus dan tidak ada imputasi preferensi. Preferensi kosong dianggap tidak diketahui, bukan tidak cocok atau skor nol. Skor gabungan hanya dihitung untuk pasangan preferensi lengkap. Alternatif seperti modus dapat mengarang preferensi orang; lebih baik menghubungi responden. Jika imputasi dipertimbangkan untuk model prediktif, buat indikator hilang, uji sensitivitas, dan pelajari imputasi dari data latih saja. Literatur tentang data hilang menekankan pentingnya mempertimbangkan asumsi, ketidakpastian dan potensi bias [4].')
heading('Bab 5. Eksplorasi Karakteristik Data')
heading('5.1 Statistik deskriptif',2)
rows=[]
for k in ['sks','jumlah_mahasiswa','kapasitas_ruang','durasi_menit']:
 s=m['statistik'][k]; rows.append((k,*[fmt(s[x]) for x in ['mean','median','mode','std','var','min','q1','q3','max']]))
table(['Variabel','Mean','Median','Modus','SD','Var','Min','Q1','Q3','Maks'],rows)
p('Statistik dihitung per baris jadwal; satu kelompok dan ruang dapat muncul berulang. Dengan demikian angka bukan statistik independen tingkat mahasiswa, dosen, atau ruang. Terdapat 573 jadwal 3 SKS dan 27 jadwal 2 SKS.')
heading('5.2 Bentuk distribusi',2)
s=m['statistik']['jumlah_mahasiswa'];p(f"Jumlah mahasiswa memiliki skewness {fmt(s['skew'])} dan excess kurtosis {fmt(s['kurtosis_excess'])}; sebaran agak condong ke kanan dan lebih datar/ekor lebih ringan dibanding acuan normal (excess kurtosis = 0). Ringkasan ini tidak membuktikan normalitas. Ukuran bersifat deskriptif dan berasal dari data simulasi.")
fig('02_mahasiswa.png','Gambar 2. Histogram jumlah mahasiswa dan boxplot menurut periode.')
heading('Bab 6. Transformasi Data')
heading('6.1 Distribusi dan skala',2)
logskew=np.log1p(df.jumlah_mahasiswa).skew()
p(f"Sebagai perbandingan eksplorasi, log1p(jumlah_mahasiswa) menghasilkan skewness {fmt(logskew)} dibanding {fmt(s['skew'])} sebelum transformasi. Transformasi ini tidak diterapkan pada data operasional: jumlah asli diperlukan untuk memeriksa kapasitas, dan normalitas fitur bukan syarat universal regresi linear. Penskalaan standardisasi (x − mean) / SD atau min–max bisa digunakan pada model yang sensitif skala; tidak diperlukan untuk aturan bentrok.")
heading('6.2 Encoding dan fitur turunan',2)
p('Variabel hari, ruang, dan periode merupakan kategori nominal: one-hot dapat dipertimbangkan untuk model. Urutan hari dapat direpresentasikan khusus jika benar-benar relevan. Fitur hasil audit yang dibuat: menit mulai/selesai, durasi, periode mulai, kapasitas kurang, kecocokan masing-masing pihak, skor 0/50/100, serta tanda bentrok. File hasil/jadwal_hasil_cek.csv memuat fitur tersebut. One-hot, standardisasi dan imputasi tidak diterapkan pada dataset operasional ini.')
p('Jika kelak dibuat model prediktif, pisahkan data dahulu dengan mempertimbangkan waktu dan kelompok; fit transformasi dan imputasi hanya pada data latih untuk menghindari kebocoran. Jangan memasukkan informasi yang baru tersedia setelah keputusan jadwal dibuat. Kebocoran data dapat menyebabkan evaluasi model terlalu optimistis [5].')
heading('Bab 7. Visualisasi Hubungan Data')
heading('7.1 Analisis univariat',2)
p('Distribusi berdasarkan hari: '+', '.join(f'{k} {v}' for k,v in m['hari'].items())+'. Distribusi berdasarkan periode mulai: '+', '.join(f'{k} {v}' for k,v in m['periode'].items())+'. Jadwal dengan mulai sebelum pukul 12.00 dikategorikan pagi, 12.00–14.59 siang, dan mulai pukul 15.00 sore; kelas yang melintasi batas periode tetap diklasifikasikan menurut waktu mulainya.')
fig('01_distribusi.png','Gambar 3. Jumlah jadwal menurut hari dan periode mulai.')
heading('7.2 Analisis bivariat dan multivariat',2)
p(f"Kecocokan dosen: 213 dari 553 baris dengan preferensi dosen diketahui; kecocokan kelompok: 194 dari 554 baris dengan preferensi kelompok diketahui. Untuk 512 baris lengkap, skor 0 = 196, skor 50 = 249, dan skor 100 = 67. Skor adalah 50 poin untuk setiap pihak yang cocok; bukan nilai kepuasan hasil survei atau ukuran efektivitas sistem.")
fig('04_bentrok_preferensi.png','Gambar 4. Baris terlibat bentrok per sumber daya dan rata-rata skor preferensi menurut periode.')
fig('05_kapasitas.png','Gambar 5. Sebaran kapasitas ruang dan jumlah mahasiswa; titik di atas garis diagonal melebihi kapasitas.')
heading('7.3 Korelasi dan asosiasi',2)
p('Korelasi Pearson antara SKS dan durasi = 1,000 karena durasi sengaja dihitung 50 × SKS. Ini hubungan deterministik akibat desain data, bukan penemuan empiris. Korelasi jumlah mahasiswa dengan skor keselarasan = 0,097 pada baris skor yang tersedia; hubungan linear ini sangat lemah dan bukan bukti sebab-akibat. Variabel kategori tidak dapat diinterpretasi dengan Pearson tanpa pengkodean yang tepat.')
heading('Bab 8. Penanganan Pencilan dan Audit Kendala')
heading('8.1 Deteksi pencilan',2)
p('Metode IQR: nilai di bawah Q1 − 1,5 × IQR atau di atas Q3 + 1,5 × IQR ditandai. Z-score: nilai dengan |z| > 3 ditandai; perhitungannya bergantung pada rata-rata dan simpangan baku serta sensitif pada bentuk distribusi.')
table(['Variabel','Batas IQR','Jumlah IQR','Jumlah |Z| > 3'],[(k,f"{fmt(m['statistik'][k]['lower_iqr'])} – {fmt(m['statistik'][k]['upper_iqr'])}",m['statistik'][k]['iqr_outlier'],m['statistik'][k]['z_outlier']) for k in ['sks','jumlah_mahasiswa','kapasitas_ruang','durasi_menit']])
p('Aturan IQR dan Z-score menandai 27 kelas 2 SKS dan durasi 100 menit karena mayoritas kelas berdurasi 150 menit. Keduanya valid menurut aturan domain; IQR = 0 untuk variabel ini sehingga hasil penandaan harus diinterpretasikan hati-hati. Tidak ada baris yang dihapus atau dibatasi semata-mata berdasarkan tanda statistik.')
heading('8.2 Audit bentrok dan kapasitas',2)
p('Sepasang jadwal bentrok jika pada hari yang sama berbagi dosen, kelompok, atau ruang dan interval waktunya beririsan. Interval digunakan dalam bentuk [mulai, selesai), sehingga satu kelas yang dimulai tepat setelah kelas lain selesai tidak bentrok. Data invalid tidak dapat dievaluasi dengan aman dan perlu diperbaiki sebelum optimasi.')
table(['Sumber daya','Baris terlibat','Pasangan bentrok'],[(k.capitalize(),m['bentrok_baris'][k],m['bentrok_pasangan'][k]) for k in ['dosen','kelompok','ruang']])
p(f"Total {m['bentrok_baris_total']} baris terlibat setidaknya satu jenis bentrok. Total tiga kategori tidak boleh dijumlahkan sebagai baris unik, karena satu baris dapat terkena lebih dari satu jenis. Tabel pasangan terperinci tersedia pada hasil/daftar_bentrok.csv. Temuan ini disebabkan penetapan jadwal secara acak dan tidak menggambarkan performa kampus tertentu.")
heading('Bab 9. Kesimpulan dan Temuan Utama')
heading('9.1 Ringkasan temuan',2)
bullet(f"Dataset berisi 600 jadwal sintetis; 530 baris terlibat bentrok dan 182 baris kelebihan kapasitas ruang.")
bullet(f"Kecocokan dosen {fmt(m['cocok_dosen_persen'])}% dan kelompok {fmt(m['cocok_mahasiswa_persen'])}% menggunakan denominator yang berbeda. Skor lengkap rata-rata {fmt(m['rata_skor_keselarasan'])}/100 pada 512 baris.")
bullet('Nilai 2 SKS/durasi 100 menit terdeteksi pencilan statistik namun tetap dipertahankan karena sah menurut desain.')
heading('9.2 Keterbatasan',2)
p('Data dan preferensi sepenuhnya sintetis, pembagian waktu dan bobot 50:50 merupakan asumsi, belum mengukur preferensi individual mahasiswa, belum memperhitungkan ketersediaan/fasilitas, dan tidak merepresentasikan satu institusi atau semester nyata. Jadwal acak sengaja tidak dijamin layak; ketidaksesuaian tidak membuktikan bahwa optimasi akan mencapai skor tertentu. Dataset berisi pengulangan entitas sehingga observasi tidak independen.')
heading('9.3 Rekomendasi pengembangan optimasi',2)
p('Gunakan CP-SAT (misalnya OR-Tools) atau mixed-integer linear programming sebagai kandidat, bukan classifier sebagai pengganti optimasi. Studi penjadwalan telah menggunakan pemrograman bilangan bulat untuk memasukkan preferensi dosen dan kebutuhan kelas/ruang [2]; survei metode metaheuristik memberikan alternatif pembanding [3]. Definisikan variabel keputusan x[c,s,r] = 1 jika kelas c ditempatkan pada slot s dan ruang r. Hard constraints: setiap kelas tepat satu penempatan, tidak ada irisan dosen/kelompok/ruang, kapasitas memadai, durasi dan ketersediaan terpenuhi. Tujuan lunak: memaksimalkan total bobot kesesuaian preferensi dosen dan mahasiswa yang diketahui; dapat ditambah penalti sebaran jam yang tidak merata.')
p('Bandingkan baseline acak dan solusi pada data serta metrik identik; laporkan jumlah pelanggaran, skor beserta cakupan data, fairness antar kelompok, waktu komputasi, status solver (feasible/optimal/infeasible), batas waktu dan gap bila tersedia. Jika tidak feasible, kaji kendala dan sumber daya; jangan mengklaim optimal tanpa bukti solver. Penggunaan machine learning hanya opsional untuk memperkirakan preferensi atau durasi berdasarkan data yang sesuai.')
heading('Daftar Pustaka — Artikel Jurnal')
for ref in [
 '[1] S. Ceschia, L. Di Gaspero, dan A. Schaerf, “Educational timetabling: Problems, benchmarks, and state-of-the-art results,” European Journal of Operational Research, vol. 308, no. 1, pp. 1–18, 2023. https://doi.org/10.1016/j.ejor.2022.07.011',
 '[2] A. Ozkan, A. Ulucan, C. Dirik, dan K. B. Atici, “University course timetabling with multi-section courses, room stability and lecturer preferences: an application in a business school,” Computational Management Science, vol. 22, art. 3, 2025. https://doi.org/10.1007/s10287-025-00529-2',
 '[3] R. Lewis, “A survey of metaheuristic-based techniques for university timetabling problems,” OR Spectrum, vol. 30, no. 1, pp. 167–190, 2008. https://doi.org/10.1007/s00291-007-0097-0',
 '[4] J. A. C. Sterne, I. R. White, J. B. Carlin, M. Spratt, P. Royston, M. G. Kenward, A. M. Wood, dan J. R. Carpenter, “Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls,” BMJ, vol. 338, art. b2393, 2009. https://doi.org/10.1136/bmj.b2393',
 '[5] S. Kapoor dan A. Narayanan, “Leakage and the reproducibility crisis in machine-learning-based science,” Patterns, vol. 4, no. 9, art. 100804, 2023. https://doi.org/10.1016/j.patter.2023.100804',
 '[6] M. L. Waskom, “seaborn: statistical data visualization,” Journal of Open Source Software, vol. 6, no. 60, art. 3021, 2021. https://doi.org/10.21105/joss.03021']:
 p(ref)

doc.add_page_break()
heading('Lampiran A. Hasil Reproduksi dan Pengujian')
v=json.loads((R/'hasil/hasil_pengujian.json').read_text(encoding='utf-8'))
assert v['unittest_returncode']==0 and 'Ran 6 tests' in v['unittest_log'] and v['dashboard_error_count']==0 and v['dashboard_exception_count']==0
p('Lampiran ini memuat hasil yang benar-benar dihasilkan dari eksekusi Python, bukan ilustrasi hasil yang diharapkan. Pemeriksaan dilakukan pada dataset sintetis yang disertakan; waktu eksekusi dan versi dapat berbeda ketika dijalankan ulang.')
heading('A.1 Lingkungan dan identitas data',2)
table(['Komponen','Hasil pengujian'],[('Waktu eksekusi (WIB)',v['timestamp_jakarta']),('Python',v['python']),('Sistem',v['platform']),('Versi pustaka',', '.join(f'{k} {val}' for k,val in v['versions'].items())),('Jumlah data','600 baris, 14 kolom'),('Seed data','20261123')])
p('SHA-256 dataset CSV (identitas berkas): '+v['dataset_sha256'])
heading('A.2 Hasil pengujian otomatis logika audit',2)
p('Perintah yang dijalankan: python -m unittest -v test_analisis. Enam pengujian selesai dengan status OK dan kode keluar 0; ringkasan hasilnya sebagai berikut:')
table(['Kasus uji','Hasil aktual','Status'],[
 ('Konsistensi dataset','600 baris, 600 ID unik; 530 baris bentrok dan 749 pasangan','Lulus'),
 ('Bentrok dan batas waktu','A 08:00–09:40 tumpang tindih B 09:00–10:40 pada 3 sumber daya; B berakhir tepat saat C mulai 10:40, sehingga B–C tidak bentrok','Lulus'),
 ('Waktu invalid & preferensi kosong','xx:xx dinyatakan tidak valid; preferensi dan skor gabungan tidak dihitung','Lulus'),
 ('Preferensi kosong pada waktu valid','Waktu tetap valid; kecocokan dosen dan skor gabungan kosong','Lulus'),
 ('Contoh pasangan pada data dummy','Pasangan dosen, kelompok dan ruang sesuai contoh pada Tabel A.3','Lulus'),
 ('Contoh kapasitas & preferensi','JDW0004: 37 mahasiswa > 25 kursi; skor preferensi 100','Lulus')])
p('Catatan: enam skenario di atas adalah pemeriksaan terbatas, bukan jaminan sistem bebas kesalahan. Hasil 749 adalah total pasangan per jenis (161 dosen + 211 kelompok + 377 ruang); pasangan yang berbagi lebih dari satu jenis dapat tercatat lebih dari sekali.')
heading('A.3 Contoh hasil audit pada data 600 baris',2)
table(['Jenis','ID/sumber daya','Hasil aktual dan interpretasi'],[
 ('Bentrok dosen','DSN025','JDW0001 dan JDW0458: Jumat 10:20–12:50; sumber daya dan waktunya sama.'),
 ('Bentrok kelompok','KLP016','JDW0001 dan JDW0475: Jumat 10:20–12:50; kelompok dan waktunya sama.'),
 ('Bentrok ruang','R14','JDW0331 08:40–11:10 dan JDW0001 10:20–12:50 pada Jumat; beririsan 10:20–11:10.'),
 ('Kapasitas dan skor','JDW0004','37 mahasiswa pada ruang berkapasitas 25; dosen dan kelompok memilih Siang, sesuai jadwal mulai 13:00; skor 100/100.')])
heading('A.4 Hasil pemeriksaan aplikasi Python',2)
p('Aplikasi diuji dengan Streamlit AppTest pada input bawaan, kemudian filter hari diubah menjadi Senin. Kedua eksekusi menghasilkan 0 exception dan 0 pesan error. Ini adalah uji aplikasi otomatis, bukan uji visual manual atau uji unggah CSV.')
table(['Metrik aplikasi','Seluruh data','Filter Senin'],[(k,v['dashboard_default_metrics'][k],v['dashboard_filter_senin_metrics'][k]) for k in ['Jadwal ditampilkan','Baris terlibat bentrok','Ruang kurang kapasitas','Skor keselarasan rata-rata']])
p('Bentrok dihitung atas keseluruhan dataset sebelum filter; metrik kemudian diringkas untuk baris yang ditampilkan. Data contoh hasil audit per baris ada pada hasil/jadwal_hasil_cek.csv dan seluruh pasangan pada hasil/daftar_bentrok.csv.')
heading('A.5 Keluaran aktual dan cara reproduksi',2)
q=doc.add_paragraph(v['unittest_log']);
for r in q.runs:r.font.name='Consolas';r.font.size=Pt(8)
p('Dari folder proyek: pip install -r requirements.txt; python analisis.py; python verifikasi.py; python buat_laporan.py. Gunakan streamlit run app.py untuk membuka dashboard. Keluaran uji disimpan di hasil/hasil_pengujian.json dan hasil/hasil_pengujian.txt. Berkas versi ini mencatat hasil pada lingkungan di atas; jalankan ulang untuk mendapatkan bukti dari lingkungan Anda sendiri.')
p('Pengujian ini memverifikasi contoh dan aturan audit yang dipilih, bukan hasil optimasi. Belum ada pembandingan sebelum dan sesudah optimasi, pengujian performa, pengujian penggunaan nyata, atau sertifikat optimalitas.')
doc.save(R/'Laporan_EDA_Penjadwalan.docx')
print('Laporan dibuat')
