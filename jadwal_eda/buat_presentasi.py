from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent
m=json.loads((ROOT/'hasil/ringkasan.json').read_text(encoding='utf-8'))
v=json.loads((ROOT/'hasil/hasil_pengujian.json').read_text(encoding='utf-8'))
assert m['baris']==600 and v['unittest_returncode']==0
prs=Presentation();prs.slide_width=Inches(13.333);prs.slide_height=Inches(7.5)
BLANK=prs.slide_layouts[6]
NAVY='112C39'; DEEP='0A222D'; TEAL='007E80'; AQUA='D7EEEA'; MINT='EFF8F6'; WHITE='FFFFFF'; BG='F7F9F8'; INK='192F39'; MUTED='5E737A'; AMBER='D89241'; PALE='FFF2E2'; RED='B45355'; LIGHT='E5EEEB'; GREY='C5D3D0'

def rgb(c):return RGBColor.from_string(c)
def box(sl,x,y,w,h,fill, radius=False, line=None):
    shape=sl.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid();shape.fill.fore_color.rgb=rgb(fill)
    shape.line.fill.background() if line is None else None
    if line:shape.line.color.rgb=rgb(line)
    if radius:
        try:shape.adjustments[0]=0.12
        except:pass
    return shape

def txt(sl,text,x,y,w,h,size=16,color=INK,bold=False,align='left',valign=MSO_ANCHOR.TOP,font='Aptos',margin=0):
    sh=sl.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h));tf=sh.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_left=tf.margin_right=Inches(margin);tf.margin_top=tf.margin_bottom=0;tf.vertical_anchor=valign
    for i,line in enumerate(text.split('\n')):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph();p.text=line;p.alignment={'left':PP_ALIGN.LEFT,'center':PP_ALIGN.CENTER,'right':PP_ALIGN.RIGHT}[align];p.space_before=Pt(0);p.space_after=Pt(0);p.font.name=font;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=rgb(color)
    return sh

def slide(title,kicker,sub=None):
    s=prs.slides.add_slide(BLANK);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb(BG)
    txt(s,kicker.upper(),.65,.32,11.5,.25,10,TEAL,True)
    txt(s,title,.65,.70,12.0,.62,27,INK,True)
    if sub:txt(s,sub,.67,1.38,11.9,.5,13,MUTED)
    box(s,.65,7.12,12.03,.012,LIGHT);txt(s,'EDA PENJADWALAN  •  DATA SINTETIS',.67,7.18,9,.18,8,MUTED,True);txt(s,f'{len(prs.slides):02}',12.0,7.16,.65,.2,9,MUTED,align='right')
    return s

def notes(s,t):s.notes_slide.notes_text_frame.text=t

def card(sl,x,y,w,h,label,value,desc,accent=TEAL):
    box(sl,x,y,w,h,WHITE,True);box(sl,x,y,.06,h,accent)
    txt(sl,label,x+.2,y+.18,w-.4,.3,11,MUTED,True)
    txt(sl,value,x+.2,y+.53,w-.4,.6,28,accent,True)
    txt(sl,desc,x+.2,y+1.2,w-.4,h-1.28,12,INK)

def bullet(sl,x,y,w,text, size=16,color=INK):
    box(sl,x,y+.10,.085,.085,TEAL,True);txt(sl,text,x+.25,y,w-.25,.62,size,color)

def smalltag(sl,text,x,y,w,fill=AQUA,color=TEAL):
    box(sl,x,y,w,.36,fill,True);txt(sl,text,x+.08,y+.06,w-.16,.22,10,color,True,align='center')

def bar(sl,x,y,w,label,value,maxv,display,color=TEAL):
    txt(sl,label,x,y,w*.30,.25,13,INK,True)
    box(sl,x+w*.30,y+.03,w*.53,.16,LIGHT,True)
    if value:box(sl,x+w*.30,y+.03,w*.53*value/maxv,.16,color,True)
    txt(sl,display,x+w*.84,y-.02,w*.16,.3,13,INK,True,align='right')

# 1 cover
s=prs.slides.add_slide(BLANK);s.background.fill.solid();s.background.fill.fore_color.rgb=rgb(DEEP)
box(s,9.5,0,3.833,7.5,NAVY);box(s,.7,.72,1.23,.07,TEAL)
txt(s,'PROYEK EDA  /  SAINS DATA',.72,1.05,8,.3,12,'8BD3C9',True)
txt(s,'Penjadwalan\nmata kuliah',.68,1.58,8.5,1.55,41,WHITE,True)
txt(s,'Dengan pertimbangan preferensi\ndosen dan mahasiswa',.72,3.35,8.2,.85,21,'CBE2DD')
smalltag(s,'600 JADWAL SINTETIS',.72,4.67,2.5,'1D4C4F','A7E3D9')
txt(s,'Nama / NIM  :  ................................................',.72,5.55,8,.33,14,WHITE)
txt(s,'Program Studi  :  ................................................',.72,6.05,8,.33,14,WHITE)
txt(s,'01',12.0,7.16,.6,.2,9,'A7C2BE',align='right')
# abstract timetable decorative
for i,c in enumerate(['3AB3A4','D89045','3AB3A4','80AFA9','D89045']):
    xx=10.0+(i%2)*1.08; yy=1.45+(i//2)*1.07
    box(s,xx,yy,.85,.82,c,True)
txt(s,'MEMAHAMI DATA\nSEBELUM OPTIMASI',9.99,5.10,2.8,.65,13,'B9D7D2',True)
notes(s,'Pembuka: Presentasi ini membahas EDA sebagai tahap awal penelitian penjadwalan mata kuliah. Seluruh data adalah dummy sehingga tidak menunjukkan kondisi nyata kampus, dan solusi optimasi belum dibuat.')

#2
s=slide('Masalah dan tujuan penelitian','01 / memahami masalah','Penjadwalan yang baik harus layak sekaligus mempertimbangkan preferensi.')
box(s,.65,2.1,5.8,3.85,NAVY,True)
txt(s,'PERMASALAHAN',.97,2.43,4.6,.3,12,'8BD3C9',True)
txt(s,'Bagaimana menyusun jadwal yang tidak bentrok dan lebih sesuai bagi dosen serta mahasiswa?',.97,2.95,5.03,1.65,23,WHITE,True)
txt(s,'Jenis masalah: optimasi kombinatorial berbatas [1].',.97,5.28,5.0,.4,12,'BDD9D3')
txt(s,'TUJUAN EDA',7.0,2.23,5.2,.3,12,TEAL,True)
bullet(s,7.0,2.8,5.35,'Memahami struktur dan kualitas data.')
bullet(s,7.0,3.63,5.35,'Memetakan bentrok dan kapasitas ruang.')
bullet(s,7.0,4.46,5.35,'Mengukur kesesuaian preferensi yang tersedia.')
bullet(s,7.0,5.29,5.35,'Menyiapkan kebutuhan untuk tahap optimasi.')
notes(s,'Penjadwalan harus memenuhi sejumlah kendala keras, misalnya dosen dan ruang tidak boleh bentrok. Preferensi dipandang sebagai tujuan lunak. Fokus saat ini bukan mengklaim jadwal sudah optimal, melainkan memahami data.')

#3
s=slide('Dataset: satu baris adalah satu jadwal','02 / memahami data','Semua entitas dan nilai merupakan simulasi untuk satu minggu perkuliahan.')
for i,(label,num,desc) in enumerate([('JADWAL','600','baris / pertemuan'),('MATA KULIAH','18','jenis mata kuliah'),('DOSEN','72','identitas fiktif'),('KELOMPOK','60','kelompok mahasiswa'),('RUANG','35','ruang fiktif')]):
    card(s,.65+i*2.48,2.15,2.28,2.18,label,num,desc)
box(s,.65,4.75,12.05,1.35,MINT,True)
txt(s,'14 KOLOM AWAL',.92,5.00,2.3,.27,12,TEAL,True)
txt(s,'Identitas kelas • dosen • kelompok • ruang • kapasitas • hari & jam • preferensi',3.05,4.98,9.15,.65,16,INK)
notes(s,'Ada 600 penugasan atau pertemuan mingguan, bukan 600 mahasiswa. Identitas dosen, kelompok dan ruang fiktif. Masing-masing dosen dan kelompok mempunyai preferensi periode yang sama pada baris-baris yang terkait dengannya.')

#4
s=slide('Alur EDA dan pemeriksaan','03 / metode','Analisis dilakukan dengan Python; setiap tahap menghasilkan keluaran yang dapat ditinjau ulang.')
steps=[('01','MUAT DATA','Baca CSV dan periksa\nstruktur 600 × 14.'),('02','KUALITAS','Periksa nilai kosong,\nduplikat dan format.'),('03','EKSPLORASI','Ringkas distribusi,\nkorelasi dan pencilan.'),('04','AUDIT','Deteksi bentrok,\nkapasitas & preferensi.'),('05','KOMUNIKASI','Sajikan grafik, hasil uji\ndan rekomendasi.')]
for i,(n,h,d) in enumerate(steps):
 x=.65+i*2.46;box(s,x,2.62,2.24,2.5,WHITE,True);txt(s,n,x+.18,2.82,1,.5,24,TEAL,True);txt(s,h,x+.18,3.5,1.95,.35,12,INK,True);txt(s,d,x+.18,4.04,1.95,.65,12,MUTED)
smalltag(s,'PANDAS  +  NUMPY  +  SEABORN  +  STREAMLIT',3.65,5.72,5.95)
notes(s,'Proses EDA dimulai dari pembacaan data, dilanjutkan pemeriksaan kualitas, analisis deskriptif, pemeriksaan kendala, lalu pelaporan. Seluruh kode dan output tersedia dalam paket proyek.')

#5
s=slide('Kualitas data: preferensi belum lengkap','04 / kualitas data','Nilai kosong dipertahankan sebagai tidak diketahui, bukan otomatis dianggap tidak cocok [4].')
card(s,.65,2.04,3.66,2.11,'PREFERENSI DOSEN KOSONG','47','baris  •  7,83% dari 600',AMBER)
card(s,4.53,2.04,3.66,2.11,'PREFERENSI MAHASISWA KOSONG','46','baris  •  7,67% dari 600',AMBER)
card(s,8.41,2.04,4.27,2.11,'KEDUA PREFERENSI LENGKAP','512','baris  •  untuk skor gabungan',TEAL)
box(s,.65,4.55,12.03,1.45,WHITE,True)
txt(s,'0',.98,4.78,1,.5,26,TEAL,True);txt(s,'duplikat penuh',1.65,4.9,2.4,.3,14,INK)
txt(s,'0',4.62,4.78,1,.5,26,TEAL,True);txt(s,'waktu invalid',5.3,4.9,2.4,.3,14,INK)
txt(s,'0',8.13,4.78,1,.5,26,TEAL,True);txt(s,'durasi tidak sesuai SKS',8.81,4.9,3.4,.55,14,INK)
notes(s,'Preferensi dosen hilang di 47 baris dan mahasiswa di 46 baris. Karena bisa saling tumpang tindih, hanya 88 baris yang kehilangan minimal satu preferensi dan 512 lengkap. Tidak ada imputasi; hitungan kecocokan memakai penyebut yang tersedia.')

#6
s=slide('Distribusi jadwal menurut hari dan waktu','05 / analisis univariat','Setiap batang menunjukkan jumlah baris, bukan jumlah individu mahasiswa.')
box(s,.65,2.03,6.05,4.55,WHITE,True);txt(s,'HARI PERKULIAHAN',.95,2.34,4.7,.3,12,MUTED,True)
for i,(k,num) in enumerate(m['hari'].items()):bar(s,.98,2.92+i*.59,5.2,k,num,150,str(num))
box(s,6.9,2.03,5.78,4.55,WHITE,True);txt(s,'PERIODE MULAI',7.2,2.34,4.7,.3,12,MUTED,True)
for i,(k,num) in enumerate(m['periode'].items()):bar(s,7.22,2.95+i*.71,4.95,k,num,350,str(num),AMBER if k=='Sore' else TEAL)
txt(s,'Pagi <12.00  |  Siang 12.00–14.59\nSore ≥15.00',7.21,5.41,4.95,.75,13,MUTED)
notes(s,'Hari dengan jadwal terbanyak adalah Kamis 129. Berdasarkan jam mulai terdapat 310 jadwal pagi, 191 siang, dan 99 sore. Klasifikasi berdasarkan jam mulai, meskipun suatu kelas melewati batas periode.')

#7
s=slide('Bentrok ditemukan pada 530 jadwal','06 / audit kendala keras','88,33% dari 600 baris terlibat sedikitnya satu jenis bentrok pada jadwal awal acak.')
box(s,.65,2.08,5.48,3.88,NAVY,True);txt(s,'530',1.0,2.45,3.2,1.03,49,WHITE,True);txt(s,'baris terlibat bentrok',1.0,3.55,4.55,.4,19,'BFE2D9',True);txt(s,'Satu baris dapat terlibat dalam beberapa jenis bentrok.',1.0,4.43,4.45,.75,15,WHITE)
box(s,6.35,2.08,6.33,3.88,WHITE,True);txt(s,'JENIS BENTROK',6.68,2.40,4.7,.35,12,MUTED,True)
for i,(k,name) in enumerate([('dosen','Dosen'),('kelompok','Kelompok'),('ruang','Ruang')]):bar(s,6.70,3.0+i*.65,5.4,name,m['bentrok_baris'][k],450,str(m['bentrok_baris'][k]))
txt(s,'Pasangan: dosen 161  •  kelompok 211  •  ruang 377',6.70,5.34,5.34,.43,12,MUTED)
notes(s,'Bentrok berarti berbagi sumber daya yang sama pada hari yang sama dan interval waktunya beririsan. Nilai 252, 305, dan 420 adalah jumlah baris per jenis dan tidak boleh dijumlahkan menjadi total unik. Pasangan bentrok berbeda dengan jumlah baris.')

#8
s=slide('Ruang dan durasi: cek kelayakan dasar','07 / audit kapasitas','Kapasitas kurang terjadi jika jumlah mahasiswa melebihi kapasitas ruang.')
card(s,.65,2.15,3.5,2.3,'RUANG KURANG KAPASITAS','182','baris  •  30,33% dari 600',RED)
box(s,4.4,2.15,8.28,2.3,WHITE,True);txt(s,'CONTOH NYATA DALAM DATA DUMMY',4.72,2.44,7.1,.3,12,MUTED,True)
txt(s,'JDW0004',4.72,3.0,2.0,.48,21,TEAL,True);txt(s,'37 mahasiswa  >  25 kursi',7.0,3.0,5.2,.48,21,INK,True)
box(s,.65,4.80,12.03,1.15,MINT,True);txt(s,'ASUMSI DURASI',.98,5.12,2.55,.3,12,TEAL,True);txt(s,'1 SKS = 50 menit; semua durasi sesuai asumsi simulasi.',3.45,5.07,8.8,.45,16,INK)
notes(s,'Pada jadwal JDW0004, jumlah mahasiswa 37 sedangkan ruang hanya memuat 25. Penelitian menganggap satu SKS setara 50 menit untuk simulasi ini; aturan riil harus mengikuti ketentuan kampus.')

#9
s=slide('Preferensi: kesesuaian masih terbatas','08 / kendala lunak','Kecocokan dihitung dari periode mulai dan hanya pada preferensi yang tersedia.')
card(s,.65,2.10,3.72,2.45,'DOSEN','38,52%','213 cocok dari 553 baris valid')
card(s,4.57,2.10,3.72,2.45,'KELOMPOK MAHASISWA','35,02%','194 cocok dari 554 baris valid',AMBER)
card(s,8.50,2.10,4.18,2.45,'SKOR GABUNGAN','37,40 / 100','rata-rata pada 512 baris lengkap')
box(s,.65,4.92,12.03,1.17,WHITE,True)
txt(s,'SKOR SIMULASI',.98,5.23,2.48,.3,12,TEAL,True);txt(s,'50 poin jika dosen cocok + 50 poin jika kelompok cocok.',3.48,5.16,8.74,.58,16,INK)
notes(s,'Penyebut dosen dan mahasiswa berbeda karena preferensi yang kosong tidak dihitung. Skor gabungan hanya tersedia jika keduanya diketahui; bobot 50:50 adalah asumsi, bukan survei atau nilai kepuasan nyata.')

#10
s=slide('Pencilan dan korelasi perlu konteks','09 / interpretasi EDA','Hasil statistik tidak boleh langsung dianggap kesalahan atau hubungan sebab-akibat.')
box(s,.65,2.15,5.83,3.8,WHITE,True);smalltag(s,'PENCILAN STATISTIK',.95,2.48,2.2,PALE,RED)
txt(s,'27 kelas',.98,3.06,4.8,.6,28,INK,True)
txt(s,'2 SKS terdeteksi oleh IQR, tetapi tetap valid dan dipertahankan.',.98,3.83,4.75,1.0,17,INK)
box(s,6.7,2.15,5.98,3.8,WHITE,True);smalltag(s,'KORELASI PEARSON',7,2.48,2.35)
txt(s,'r = 1,00',7.03,3.06,4.8,.6,28,TEAL,True)
txt(s,'SKS dan durasi berkorelasi sempurna karena durasi = 50 × SKS.',7.03,3.83,4.92,1.0,17,INK)
notes(s,'Sebanyak 27 kelas dua SKS ditandai pencilan karena IQR sama dengan nol pada variabel yang mayoritas tiga SKS. Semua tetap valid. Korelasi sempurna SKS dan durasi terjadi karena rumus pembuatan data, bukan temuan empiris independen.')

#11
s=slide('Aplikasi Python dan hasil pengujian','10 / reproduksi & validasi','Uji otomatis dilakukan terhadap kode audit dan komponen dashboard pada data dummy.')
box(s,.65,2.13,5.8,3.95,WHITE,True);txt(s,'APLIKASI STREAMLIT',.96,2.47,5.15,.35,12,TEAL,True)
bullet(s,.98,3.02,5.0,'Filter berdasarkan hari dan periode.',15)
bullet(s,.98,3.76,5.0,'Lihat hasil audit dan pasangan bentrok.',15)
bullet(s,.98,4.50,5.0,'Unduh hasil pemeriksaan sebagai CSV.',15)
box(s,6.7,2.13,5.98,3.95,NAVY,True);txt(s,'HASIL UJI YANG DIJALANKAN',7.02,2.47,5.2,.34,12,'90D6CC',True)
txt(s,'6 / 6',7.03,2.94,3.5,.72,32,WHITE,True);txt(s,'uji logika lulus',7.03,3.68,4.5,.35,16,WHITE)
txt(s,'AppTest: 0 error; filter Senin menampilkan 124 jadwal.',7.03,4.50,5.2,.85,15,'C7E3DE')
notes(s,'Pengujian unit mencakup irisan waktu, batas waktu yang bersentuhan, data invalid, preferensi kosong, serta contoh data. AppTest menguji tampilan awal dan filter Senin secara otomatis; pengujian unggah CSV dan uji visual manual tidak termasuk.')

#12
s=slide('Rancangan tahap optimasi berikutnya','11 / rekomendasi','CP-SAT atau mixed-integer linear programming dapat dipertimbangkan [1], [2].')
box(s,.65,2.08,5.82,3.93,WHITE,True);smalltag(s,'HARD CONSTRAINTS',.98,2.42,2.25)
bullet(s,.99,3.00,4.9,'Setiap kelas mendapatkan satu jadwal.',15)
bullet(s,.99,3.76,4.9,'Tidak ada bentrok dosen, kelompok, ruang.',15)
bullet(s,.99,4.52,4.9,'Kapasitas dan ketersediaan terpenuhi.',15)
box(s,6.71,2.08,5.97,3.93,WHITE,True);smalltag(s,'SOFT CONSTRAINTS',7.03,2.42,2.25,PALE,RED)
bullet(s,7.05,3.00,4.92,'Maksimalkan kecocokan preferensi.',15)
bullet(s,7.05,3.76,4.92,'Perhatikan pemerataan antarkelompok.',15)
bullet(s,7.05,4.52,4.92,'Bandingkan dengan jadwal awal.',15)
notes(s,'Tahap selanjutnya adalah memformulasikan variabel keputusan yang memilih waktu dan ruang untuk setiap kelas. Kendala keras dipenuhi terlebih dahulu, sedangkan preferensi menjadi tujuan lunak. Solusi harus dilaporkan bersama status solver dan metrik perbandingan.')

#13
s=slide('Kesimpulan dan batasan','12 / penutup','EDA menghasilkan baseline audit, belum menghasilkan jadwal optimal.')
box(s,.65,2.05,7.45,4.0,WHITE,True)
txt(s,'TEMUAN UTAMA',.98,2.42,6.2,.3,12,TEAL,True)
bullet(s,1.00,3.01,6.48,'530 baris memiliki setidaknya satu bentrok.',17)
bullet(s,1.00,3.91,6.48,'182 jadwal melebihi kapasitas ruang.',17)
bullet(s,1.00,4.81,6.48,'Skor preferensi gabungan 37,40 / 100.',17)
box(s,8.34,2.05,4.34,4.0,NAVY,True);txt(s,'BATASAN',8.67,2.42,3.6,.3,12,'90D6CC',True)
txt(s,'Data acak, preferensi kelompok, dan asumsi waktu belum mewakili kondisi kampus sebenarnya.',8.67,3.00,3.55,1.85,17,WHITE)
txt(s,'Langkah lanjut: kumpulkan data nyata + bangun model optimasi.',8.67,5.03,3.55,.72,13,'BFE2D9')
notes(s,'Kesimpulan harus selalu dibaca dalam konteks data acak. Nilai bentrok yang tinggi tidak menggambarkan institusi sebenarnya. Selanjutnya dibutuhkan data valid, kesepakatan preferensi, dan implementasi model optimasi yang diuji.')

#14
s=slide('Daftar pustaka','13 / referensi','Artikel jurnal yang menjadi landasan masalah, metode, dan visualisasi.')
refs=[
'[1] Ceschia, S., Di Gaspero, L., & Schaerf, A. (2023). Educational timetabling: Problems, benchmarks, and state-of-the-art results. European Journal of Operational Research, 308(1), 1–18. doi:10.1016/j.ejor.2022.07.011',
'[2] Ozkan, A., Ulucan, A., Dirik, C., & Atici, K. B. (2025). University course timetabling with multi-section courses, room stability and lecturer preferences. Computational Management Science, 22, 3. doi:10.1007/s10287-025-00529-2',
'[3] Lewis, R. (2008). A survey of metaheuristic-based techniques for university timetabling problems. OR Spectrum, 30, 167–190. doi:10.1007/s00291-007-0097-0',
'[4] Sterne, J. A. C., et al. (2009). Multiple imputation for missing data in epidemiological and clinical research: potential and pitfalls. BMJ, 338, b2393. doi:10.1136/bmj.b2393',
'[5] Kapoor, S., & Narayanan, A. (2023). Leakage and the reproducibility crisis in machine-learning-based science. Patterns, 4(9), 100804. doi:10.1016/j.patter.2023.100804',
'[6] Waskom, M. L. (2021). seaborn: statistical data visualization. Journal of Open Source Software, 6(60), 3021. doi:10.21105/joss.03021']
for i,ref in enumerate(refs):
 x=.8 if i<3 else 6.85; y=2.05+(i%3)*1.46
 txt(s,ref,x,y,5.62,1.3,11,INK)
notes(s,'Enam referensi jurnal ini mendukung konteks penjadwalan, penggunaan preferensi, penanganan data hilang, kebocoran data, dan visualisasi. Daftar lengkap juga tersedia dalam laporan Word.')

out=ROOT/'Presentasi_EDA_Penjadwalan.pptx';prs.save(out);print(f'{out} • {len(prs.slides)} slides')
