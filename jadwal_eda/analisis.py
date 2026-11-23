"""Analisis EDA dan validasi awal jadwal. Jalankan: python analisis.py"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA = ROOT/'data/jadwal_dummy_600.csv'
HARI = ['Senin','Selasa','Rabu','Kamis','Jumat']
PERIODE = ['Pagi','Siang','Sore']

def load_data(path=DATA):
    df = pd.read_csv(path, dtype={'jam_mulai':'string','jam_selesai':'string'})
    return df

def cek_dan_tambah(df):
    df = df.copy().reset_index(drop=True)
    required = ['id_jadwal','kode_matakuliah','nama_matakuliah','sks','id_dosen','id_kelompok','jumlah_mahasiswa','id_ruang','kapasitas_ruang','hari','jam_mulai','jam_selesai','preferensi_dosen','preferensi_mahasiswa']
    absent = [c for c in required if c not in df.columns]
    if absent: raise ValueError('Kolom wajib tidak tersedia: '+', '.join(absent))
    # Parsing ketat HH:MM; data invalid diberi tanda dan tidak dihitung sebagai bentrok.
    def menit(s):
        s = s.astype('string')
        valid = s.str.fullmatch(r'(?:[01]\d|2[0-3]):[0-5]\d', na=False)
        parts = s.where(valid).str.split(':', expand=True)
        if parts.shape[1] < 2: return pd.Series(np.nan,index=s.index)
        return pd.to_numeric(parts[0],errors='coerce')*60 + pd.to_numeric(parts[1],errors='coerce')
    df['mulai_menit'] = menit(df.jam_mulai); df['selesai_menit'] = menit(df.jam_selesai)
    for c in ['sks','jumlah_mahasiswa','kapasitas_ruang']:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['periode'] = np.select([df.mulai_menit < 720,df.mulai_menit < 900,df.mulai_menit >= 900],PERIODE,default='Tidak valid')
    df['durasi_menit'] = df.selesai_menit-df.mulai_menit
    df['status_waktu_valid'] = df.hari.isin(HARI) & df.mulai_menit.notna() & df.selesai_menit.notna() & (df.durasi_menit > 0)
    df['status_durasi_sks_valid'] = df.status_waktu_valid & df.sks.isin([2,3]) & df.durasi_menit.eq(df.sks*50)
    df['status_kapasitas_valid'] = df.jumlah_mahasiswa.notna() & df.kapasitas_ruang.notna() & (df.jumlah_mahasiswa > 0) & (df.kapasitas_ruang > 0)
    df['kapasitas_kurang'] = (df.jumlah_mahasiswa > df.kapasitas_ruang).where(df.status_kapasitas_valid)
    for target,pref in [('cocok_dosen','preferensi_dosen'),('cocok_mahasiswa','preferensi_mahasiswa')]:
        known = df[pref].isin(PERIODE) & df.status_waktu_valid
        df[target] = (df.periode.eq(df[pref])).where(known)
    both = df.cocok_dosen.notna() & df.cocok_mahasiswa.notna()
    df['skor_keselarasan'] = np.nan
    df.loc[both,'skor_keselarasan'] = (df.loc[both,'cocok_dosen'].astype(int)+df.loc[both,'cocok_mahasiswa'].astype(int))*50
    # Conflict pair = same day, same entity, strict interval overlap. A row may have many pairs.
    pair_rows=[]
    for typ,key in [('dosen','id_dosen'),('kelompok','id_kelompok'),('ruang','id_ruang')]:
        flags = np.zeros(len(df),dtype=bool)
        eligible=df[df.status_waktu_valid & df[key].notna() & df[key].astype(str).str.strip().ne('')]
        for (_,entity), group in eligible.groupby(['hari',key],sort=False):
            rec = list(group.sort_values('mulai_menit').itertuples())
            for i,a in enumerate(rec):
                for b in rec[i+1:]:
                    if b.mulai_menit >= a.selesai_menit: break
                    if a.mulai_menit < b.selesai_menit and b.mulai_menit < a.selesai_menit:
                        flags[a.Index]=flags[b.Index]=True
                        pair_rows.append({'jenis':typ,'id_sumber_daya':entity,'hari':a.hari,'id_jadwal_1':a.id_jadwal,'id_jadwal_2':b.id_jadwal,'rentang_1':f'{a.jam_mulai}-{a.jam_selesai}','rentang_2':f'{b.jam_mulai}-{b.jam_selesai}'})
        df[f'bentrok_{typ}'] = flags
    df['ada_bentrok'] = df[['bentrok_dosen','bentrok_kelompok','bentrok_ruang']].any(axis=1)
    return df, pd.DataFrame(pair_rows,columns=['jenis','id_sumber_daya','hari','id_jadwal_1','id_jadwal_2','rentang_1','rentang_2'])

def ringkasan(raw, df, pairs):
    def rate(x):
        v=x.dropna(); return round(float(v.astype(bool).mean()*100),2) if len(v) else None
    n=len(df)
    data={'baris':n,'kolom_awal':len(raw.columns),'mata_kuliah':int(raw.kode_matakuliah.nunique()),'dosen':int(raw.id_dosen.nunique()),'kelompok':int(raw.id_kelompok.nunique()),'ruang':int(raw.id_ruang.nunique()),'missing':{str(k):int(v) for k,v in raw.isna().sum().items()},'duplikat_penuh':int(raw.duplicated().sum()),'duplikat_id_jadwal':int(raw.id_jadwal.duplicated().sum()),'duplikat_matkul_kelompok':int(raw.duplicated(['kode_matakuliah','id_kelompok']).sum()),'waktu_invalid':int((~df.status_waktu_valid).sum()),'durasi_sks_invalid':int((~df.status_durasi_sks_valid).sum()),'kapasitas_invalid':int((~df.status_kapasitas_valid).sum()),'kapasitas_kurang':int(df.kapasitas_kurang.fillna(False).sum()),'preferensi_dosen_valid_n':int(df.cocok_dosen.notna().sum()),'preferensi_mahasiswa_valid_n':int(df.cocok_mahasiswa.notna().sum()),'preferensi_keduanya_valid_n':int(df.skor_keselarasan.notna().sum()),'cocok_dosen_persen':rate(df.cocok_dosen),'cocok_mahasiswa_persen':rate(df.cocok_mahasiswa),'rata_skor_keselarasan':round(float(df.skor_keselarasan.mean()),2),'bentrok_baris_total':int(df.ada_bentrok.sum()),'bentrok_baris':{k:int(df['bentrok_'+k].sum()) for k in ['dosen','kelompok','ruang']},'bentrok_pasangan':{k:int((pairs.jenis==k).sum()) for k in ['dosen','kelompok','ruang']},'hari':{k:int((df.hari==k).sum()) for k in HARI},'periode':{k:int((df.periode==k).sum()) for k in PERIODE}}
    numerical=['sks','jumlah_mahasiswa','kapasitas_ruang','durasi_menit']
    data['statistik']={}
    for c in numerical:
        s=df[c].dropna(); q1,q3=s.quantile(.25),s.quantile(.75); lo=q1-1.5*(q3-q1); hi=q3+1.5*(q3-q1)
        data['statistik'][c]={'mean':round(float(s.mean()),2),'median':round(float(s.median()),2),'mode':round(float(s.mode().iloc[0]),2),'std':round(float(s.std()),2),'var':round(float(s.var()),2),'min':round(float(s.min()),2),'q1':round(float(q1),2),'q3':round(float(q3),2),'max':round(float(s.max()),2),'skew':round(float(s.skew()),3),'kurtosis_excess':round(float(s.kurt()),3),'iqr_outlier':int(((s<lo)|(s>hi)).sum()),'z_outlier':int((((s-s.mean())/s.std()).abs()>3).sum()) if s.std()>0 else 0,'lower_iqr':round(float(lo),2),'upper_iqr':round(float(hi),2)}
    cor=df[['sks','jumlah_mahasiswa','kapasitas_ruang','durasi_menit','skor_keselarasan']].corr(numeric_only=True)
    data['korelasi']=cor.round(3).fillna(0).to_dict()
    return data

def plots(raw,df):
    sns.set_theme(style='whitegrid',font_scale=.95)
    p=ROOT/'grafik';p.mkdir(exist_ok=True)
    fig,ax=plt.subplots(1,2,figsize=(11,4)); sns.countplot(data=df,x='hari',order=HARI,ax=ax[0],color='#287b83'); sns.countplot(data=df,x='periode',order=PERIODE,ax=ax[1],color='#dd9b54');ax[0].set_title('Distribusi jadwal per hari');ax[1].set_title('Distribusi waktu mulai');fig.tight_layout();fig.savefig(p/'01_distribusi.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(1,2,figsize=(11,4));sns.histplot(data=df,x='jumlah_mahasiswa',bins=12,ax=ax[0],color='#287b83');sns.boxplot(data=df,x='periode',y='jumlah_mahasiswa',order=PERIODE,ax=ax[1],color='#a5d0c9');ax[0].set_title('Distribusi jumlah mahasiswa');ax[1].set_title('Jumlah mahasiswa menurut periode');fig.tight_layout();fig.savefig(p/'02_mahasiswa.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(1,2,figsize=(11,4)); null=raw.isna().sum();null=null[null>0];ax[0].barh(null.index,null.values,color='#dd9b54');ax[0].set_title('Nilai kosong per kolom');sns.heatmap(df[['sks','jumlah_mahasiswa','kapasitas_ruang','durasi_menit','skor_keselarasan']].corr(),annot=True,fmt='.2f',vmin=-1,vmax=1,cmap='vlag',ax=ax[1]);ax[1].set_title('Korelasi Pearson');fig.tight_layout();fig.savefig(p/'03_missing_korelasi.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(1,2,figsize=(11,4)); counts=[int(df['bentrok_'+x].sum()) for x in ['dosen','kelompok','ruang']]; ax[0].bar(['Dosen','Kelompok','Ruang'],counts,color=['#287b83','#e0a35f','#ac5970']); ax[0].set_title('Jumlah baris terlibat bentrok'); c=df.groupby('periode',observed=False)['skor_keselarasan'].mean().reindex(PERIODE);ax[1].bar(c.index,c.values,color='#287b83');ax[1].set_ylim(0,100);ax[1].set_title('Rata-rata skor (preferensi lengkap)');fig.tight_layout();fig.savefig(p/'04_bentrok_preferensi.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(7,4));sns.scatterplot(data=df,x='kapasitas_ruang',y='jumlah_mahasiswa',hue='kapasitas_kurang',alpha=.6,ax=ax);ax.plot([20,60],[20,60],color='black',linestyle='--',label='Kapasitas = jumlah');ax.set_title('Kapasitas ruang dan jumlah mahasiswa');ax.legend();fig.tight_layout();fig.savefig(p/'05_kapasitas.png',dpi=150);plt.close(fig)

def main():
    (ROOT/'hasil').mkdir(exist_ok=True)
    raw=load_data(); df,pairs=cek_dan_tambah(raw); m=ringkasan(raw,df,pairs)
    df.to_csv(ROOT/'hasil/jadwal_hasil_cek.csv',index=False,encoding='utf-8-sig'); pairs.to_csv(ROOT/'hasil/daftar_bentrok.csv',index=False,encoding='utf-8-sig')
    (ROOT/'hasil/ringkasan.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
    df.select_dtypes(include='number').describe().to_csv(ROOT/'hasil/statistik_deskriptif.csv',encoding='utf-8-sig')
    plots(raw,df)
    print(json.dumps(m,indent=2,ensure_ascii=False))
if __name__ == '__main__': main()
