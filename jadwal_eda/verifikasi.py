"""Menjalankan uji aktual dan menyimpan hasil untuk lampiran laporan."""
from pathlib import Path
import subprocess,sys,hashlib,json,platform,importlib.metadata
from datetime import datetime
from zoneinfo import ZoneInfo
from streamlit.testing.v1 import AppTest
ROOT=Path(__file__).resolve().parent
p=subprocess.run([sys.executable,'-m','unittest','-v','test_analisis'],cwd=ROOT,capture_output=True,text=True)
app=AppTest.from_file(str(ROOT/'app.py'),default_timeout=30).run()
if app.exception or app.error: raise RuntimeError('Gagal menjalankan dashboard: '+str(list(app.exception)))
metrics={x.label:x.value for x in app.metric}
expected={'Total seluruh jadwal':'600','Jadwal ditampilkan':'600','Baris terlibat bentrok':'530','Ruang kurang kapasitas':'182','Skor keselarasan rata-rata':'37.4/100'}
if metrics != expected: raise AssertionError(f'Metrik dashboard tidak sesuai: {metrics}')
app.multiselect[0].set_value(['Senin']).run()
if app.exception or app.error: raise RuntimeError('Gagal pada filter hari')
filtered={x.label:x.value for x in app.metric}
if filtered['Jadwal ditampilkan'] != '124' or filtered['Total seluruh jadwal'] != '600': raise AssertionError(f"Filter atau total tidak sesuai: {filtered}")
versions={n:importlib.metadata.version(n) for n in ['numpy','pandas','matplotlib','seaborn','streamlit','python-docx']}
results={'timestamp_jakarta':datetime.now(ZoneInfo('Asia/Jakarta')).isoformat(timespec='seconds'),'python':platform.python_version(),'platform':platform.platform(),'versions':versions,'dataset_sha256':hashlib.sha256((ROOT/'data/jadwal_dummy_600.csv').read_bytes()).hexdigest(),'unittest_returncode':p.returncode,'unittest_log':(p.stdout+p.stderr).strip(),'dashboard_error_count':len(app.error),'dashboard_exception_count':len(app.exception),'dashboard_default_metrics':metrics,'dashboard_filter_senin_metrics':filtered}
(ROOT/'hasil/hasil_pengujian.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
if p.returncode: sys.exit(p.returncode)
