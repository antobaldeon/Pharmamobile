import sys,time
sys.path.insert(0,'tmp/s13/informe');import android
for i in range(4):
 android.tap_text('Sincronizar')
 for n in range(15):
  time.sleep(1)
  texts=[x.get('text') for x in android.tree().iter('node')]
  if 'Sincronizar' in texts:break
 else:raise Exception('Sincronizacion no termino')
 print('Reintento',i+2,flush=True)
android.run('shell','input','swipe','500','600','500','2200','500')
android.snap('06_fila_fallida_cinco_intentos')
