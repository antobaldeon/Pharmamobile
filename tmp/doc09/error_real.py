from pathlib import Path
import subprocess
p=Path('shared/src/androidMain/kotlin/pe/edu/upeu/pharmamobile/platform/Formato.android.kt')
original=p.read_bytes()
try:
 p.write_text('package pe.edu.upeu.pharmamobile.platform\n// actual temporalmente retirado para el punto de control S09\n',encoding='utf-8')
 r=subprocess.run(['cmd','/c','gradlew.bat',':shared:compileAndroidMain','--console=plain'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 Path('docs/evidencias_s09/04_error_actual.txt').write_bytes(r.stdout)
 print(r.stdout.decode('utf-8',errors='replace')[-5500:]);print('exit',r.returncode)
finally:
 p.write_bytes(original)
 print('Archivo actual restaurado')
