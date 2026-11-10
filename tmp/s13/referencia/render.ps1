$ErrorActionPreference='Stop'
$w=New-Object -ComObject Word.Application
$w.Visible=$false;$w.DisplayAlerts=0
try {
 $d=$w.Documents.Open('C:\Users\tania\AndroidStudioProjects\PharmaMobil\output\doc\S13_Practica_Integrador_Baldeon_FormatoReferencia.docx',$false,$true)
 $d.ExportAsFixedFormat('C:\Users\tania\AndroidStudioProjects\PharmaMobil\tmp\s13\referencia\adaptado.pdf',17)
 Write-Output "PAGES=$($d.ComputeStatistics(2))"
 $d.Close(0)
}finally{$w.Quit()}
