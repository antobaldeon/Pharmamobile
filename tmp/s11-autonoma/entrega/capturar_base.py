import subprocess,pathlib,sqlite3,json
adb=r'C:/Users/tania/AppData/Local/Android/Sdk/platform-tools/adb.exe'
out=pathlib.Path('tmp/s11-autonoma/entrega')
for name in ['pharma.db','pharma.db-wal','pharma.db-shm']:
 r=subprocess.run([adb,'-s','emulator-5554','exec-out','run-as','pe.edu.upeu.pharmamobile','cat','databases/'+name],capture_output=True)
 if r.returncode==0:(out/name).write_bytes(r.stdout)
try:
 c=sqlite3.connect(out/'pharma.db')
 rows=c.execute('select id,nombre,pendiente from producto order by id').fetchall()
 try:stamp=c.execute('select * from estado_sincronizacion').fetchall()
 except Exception:stamp=[]
 (out/'estado_base.json').write_text(json.dumps({'productos':rows,'sincronizacion':stamp},ensure_ascii=False),encoding='utf-8')
 print('PRODUCTOS',len(rows),'PENDIENTES',sum(x[2] for x in rows),'ULTIMA',stamp)
except Exception as e:print(e)
