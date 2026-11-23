import unittest
import pandas as pd
from analisis import cek_dan_tambah, load_data

class TestAudit(unittest.TestCase):
    def test_overlap_dan_batas(self):
        base={'kode_matakuliah':'MK01','nama_matakuliah':'Tes','sks':2,'id_dosen':'D1','id_kelompok':'K1','jumlah_mahasiswa':30,'id_ruang':'R1','kapasitas_ruang':25,'hari':'Senin','preferensi_dosen':'Pagi','preferensi_mahasiswa':'Siang'}
        data=[dict(base,id_jadwal='A',jam_mulai='08:00',jam_selesai='09:40'),dict(base,id_jadwal='B',jam_mulai='09:00',jam_selesai='10:40'),dict(base,id_jadwal='C',jam_mulai='10:40',jam_selesai='12:20')]
        df,pairs=cek_dan_tambah(pd.DataFrame(data))
        self.assertEqual(len(pairs),3) # A-B untuk tiga jenis; B-C batas sentuh bukan bentrok
        self.assertTrue(df.loc[0,'ada_bentrok']);self.assertFalse(df.loc[2,'ada_bentrok'])
        self.assertTrue(df.loc[0,'kapasitas_kurang']);self.assertEqual(df.loc[0,'skor_keselarasan'],50)
    def test_invalid_dan_missing(self):
        raw=load_data().iloc[:1].copy();raw.loc[raw.index[0],'jam_mulai']='xx:xx';raw.loc[raw.index[0],'preferensi_dosen']=None
        df,p=cek_dan_tambah(raw)
        self.assertFalse(df.loc[0,'status_waktu_valid']);self.assertTrue(pd.isna(df.loc[0,'cocok_dosen']));self.assertTrue(pd.isna(df.loc[0,'skor_keselarasan']))
    def test_dataset(self):
        raw=load_data();df,p=cek_dan_tambah(raw)
        self.assertEqual(len(df),600);self.assertEqual(raw.id_jadwal.nunique(),600)
        self.assertEqual(int(df.ada_bentrok.sum()),530);self.assertEqual(len(p),749)
    def test_contoh_bentrok_data_dummy(self):
        df,p=cek_dan_tambah(load_data())
        for typ,resource,a,b in [('dosen','DSN025','JDW0001','JDW0458'),('kelompok','KLP016','JDW0001','JDW0475'),('ruang','R14','JDW0331','JDW0001')]:
            match=p[(p.jenis==typ)&(p.id_sumber_daya==resource)&(p.id_jadwal_1==a)&(p.id_jadwal_2==b)]
            self.assertEqual(len(match),1)
    def test_contoh_kapasitas_dan_preferensi(self):
        df,_=cek_dan_tambah(load_data()); row=df.set_index('id_jadwal').loc['JDW0004']
        self.assertEqual(row.jumlah_mahasiswa,37);self.assertEqual(row.kapasitas_ruang,25)
        self.assertTrue(row.kapasitas_kurang);self.assertEqual(row.skor_keselarasan,100)
    def test_missing_preferensi_saat_waktu_valid(self):
        raw=load_data().iloc[:1].copy();raw.loc[raw.index[0],'preferensi_dosen']=None
        df,_=cek_dan_tambah(raw)
        self.assertTrue(df.loc[0,'status_waktu_valid']);self.assertTrue(pd.isna(df.loc[0,'cocok_dosen']))
        self.assertTrue(pd.isna(df.loc[0,'skor_keselarasan']))
if __name__=='__main__': unittest.main()
