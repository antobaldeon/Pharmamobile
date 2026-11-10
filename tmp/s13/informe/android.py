import subprocess,xml.etree.ElementTree as E,re,sys,time
from pathlib import Path
A=['C:/Users/tania/AppData/Local/Android/Sdk/platform-tools/adb.exe','-s','emulator-5554']
def run(*x):return subprocess.run(A+list(x),capture_output=True,check=True).stdout
def tree():
 run('shell','uiautomator','dump','/sdcard/s13.xml');run('pull','/sdcard/s13.xml','tmp/s13/informe/ui.xml');return E.parse('tmp/s13/informe/ui.xml')
def tap_text(t):
 r=tree();ns=[n for n in r.iter('node') if n.get('text')==t]
 if not ns:raise Exception('No text '+t)
 tap(ns[0])
def tap(n):
 v=list(map(int,re.findall(r'\d+',n.get('bounds'))));run('shell','input','tap',str((v[0]+v[2])//2),str((v[1]+v[3])//2))
def fill(index,value):
 ns=[n for n in tree().iter('node') if n.get('class')=='android.widget.EditText'];tap(ns[index]);run('shell','input','text',value);run('shell','input','keyevent','4')
def snap(name):
 run('shell','screencap','-p','/sdcard/s13.png');run('pull','/sdcard/s13.png','docs/captura/s13/'+name+'.png')
if __name__=='__main__':
 if sys.argv[1]=='login':fill(0,'admin');fill(1,'Admin123');tap_text('Ingresar')
 elif sys.argv[1]=='tap':tap_text(sys.argv[2])
 elif sys.argv[1]=='snap':snap(sys.argv[2])
 elif sys.argv[1]=='tree':
  for n in tree().iter('node'):
   if n.get('text'):print(n.get('text').encode('ascii','backslashreplace').decode(),n.get('bounds'))
