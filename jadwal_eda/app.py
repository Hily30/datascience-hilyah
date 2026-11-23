"""Dashboard pengecekan jadwal; jalankan streamlit run app.py."""
from pathlib import Path
import pandas as pd
import streamlit as st
from analisis import load_data, cek_dan_tambah, HARI, PERIODE

st.set_page_config(page_title='Audit Jadwal Kuliah',page_icon='📚',layout='wide')
st.title('📚 Audit Jadwal Kuliah')
st.caption('Eksplorasi dan pemeriksaan kendala — data default adalah simulasi, bukan data kampus riil.')
file=st.sidebar.file_uploader('Unggah CSV dengan kolom seperti dataset contoh',type=['csv'])
try:
    raw=pd.read_csv(file,dtype={'jam_mulai':'string','jam_selesai':'string'}) if file else load_data()
    if raw.empty: st.error('Dataset kosong.');st.stop()
    df,pairs=cek_dan_tambah(raw)
except Exception as e:
    st.error(f'Gagal membaca atau memeriksa data: {e}');st.stop()
st.sidebar.info('Bentrok dihitung pada seluruh data sebelum filter diterapkan. Preferensi kosong tidak dihitung sebagai cocok atau tidak cocok.')
with st.sidebar:
    hari=st.multiselect('Hari',HARI,default=HARI)
    period=st.multiselect('Periode mulai',PERIODE,default=PERIODE)
    only=st.checkbox('Hanya baris dengan bentrok')
f=df[df.hari.isin(hari)&df.periode.isin(period)].copy()
if only: f=f[f.ada_bentrok]
st.caption(f'Total dataset tetap {len(df)} jadwal. Saat ini {len(f)} jadwal ditampilkan sesuai filter; data asli tidak dihapus.')
total,shown,conflict,capacity,preference=st.columns(5)
total.metric('Total seluruh jadwal',len(df),help='Jumlah seluruh jadwal dalam dataset, tanpa filter.')
shown.metric('Jadwal ditampilkan',len(f),help='Jumlah jadwal yang cocok dengan filter hari, periode, dan bentrok.')
conflict.metric('Baris terlibat bentrok',int(f.ada_bentrok.sum()))
capacity.metric('Ruang kurang kapasitas',int(f.kapasitas_kurang.fillna(False).sum()))
score=f.skor_keselarasan.mean(); preference.metric('Skor keselarasan rata-rata',f'{score:.1f}/100' if pd.notna(score) else 'Belum tersedia')
st.caption('Total seluruh jadwal tidak dipengaruhi filter. Metrik lainnya mengikuti jadwal yang ditampilkan.')
st.caption('Skor keselarasan hanya untuk baris yang memiliki kedua preferensi: dosen cocok 50 poin + kelompok cocok 50 poin. Bukan hasil optimasi.')
tabs=st.tabs(['Ringkasan EDA','Data & kualitas','Daftar bentrok','Panduan'])
with tabs[0]:
    x,y=st.columns(2)
    with x:
        st.subheader('Jumlah jadwal per hari');st.bar_chart(f.hari.value_counts().reindex(HARI,fill_value=0))
        st.subheader('Kecocokan preferensi')
        for col,label in [('cocok_dosen','Dosen'),('cocok_mahasiswa','Kelompok mahasiswa')]:
            valid=f[col].dropna(); text=f'{valid.astype(bool).mean()*100:.1f}% dari {len(valid)} baris valid' if len(valid) else 'Tidak tersedia'
            st.write(f'**{label}:** {text}')
    with y:
        st.subheader('Jadwal per periode mulai');st.bar_chart(f.periode.value_counts().reindex(PERIODE,fill_value=0))
        st.subheader('Baris terlibat bentrok per jenis')
        st.bar_chart(pd.Series({k:int(f['bentrok_'+k].sum()) for k in ['dosen','kelompok','ruang']}))
        st.caption('Satu baris dapat masuk lebih dari satu jenis. Bukan jumlah pasangan bentrok.')
with tabs[1]:
    st.subheader('Ringkasan kualitas data lengkap (sebelum filter)')
    st.write({'Nilai kosong per kolom':raw.isna().sum().to_dict(),'Duplikat baris penuh':int(raw.duplicated().sum()),'Duplikat ID jadwal':int(raw.id_jadwal.duplicated().sum()),'Waktu tidak valid':int((~df.status_waktu_valid).sum()),'Durasi tidak sesuai SKS':int((~df.status_durasi_sks_valid).sum()),'Jumlah atau kapasitas tidak valid':int((~df.status_kapasitas_valid).sum())})
    st.subheader('Tabel hasil pemeriksaan')
    st.dataframe(f,use_container_width=True)
    st.download_button('Unduh hasil terfilter',f.to_csv(index=False).encode('utf-8-sig'),'hasil_cek_terfilter.csv','text/csv')
with tabs[2]:
    st.subheader('Pasangan bentrok — seluruh dataset')
    st.caption('Dua jadwal bentrok jika hari dan sumber daya sama serta interval waktunya bertumpang tindih. Ujung waktu yang sama tidak dianggap bentrok.')
    st.dataframe(pairs,use_container_width=True)
    st.download_button('Unduh pasangan bentrok',pairs.to_csv(index=False).encode('utf-8-sig'),'pasangan_bentrok.csv','text/csv')
with tabs[3]:
    st.markdown('''**Jenis pemeriksaan:** bentrok dosen, kelompok mahasiswa, ruang, kapasitas ruang, kesesuaian durasi dan preferensi.
    \n**Batasan:** sistem ini tidak menyusun ulang jadwal; tidak memeriksa libur, ketersediaan aktual, fasilitas, atau mahasiswa lintas kelompok. Data simulasi tidak mewakili kondisi nyata. Lihat README.md untuk format CSV dan panduan menjalankan.''')
