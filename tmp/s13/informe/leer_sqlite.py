import subprocess,sqlite3,json
from pathlib import Path
A=['C:/Users/tania/AppData/Local/Android/Sdk/platform-tools/adb.exe','-s','emulator-5554']
o=Path('tmp/s13/informe')
for n in ['pharma.db','pharma.db-wal','pharma.db-shm']:
 r=subprocess.run(A+['exec-out','run-as','pe.edu.upeu.pharmamobile','cat','databases/'+n],capture_output=True)
 if r.returncode==0:(o/n).write_bytes(r.stdout)
c=sqlite3.connect(o/'pharma.db')
rows=c.execute('select id,nombre,pendiente,intentos,ultimoError from producto').fetchall()
(o/'sqlite.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')
print('FILAS',len(rows),'PENDIENTES',sum(x[2] for x in rows),'INTENTOS',[x[3] for x in rows])
