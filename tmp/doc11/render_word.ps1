$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
 $doc = $word.Documents.Open('C:\Users\tania\AndroidStudioProjects\PharmaMobil\output\doc\S11_Entregable_Offline_First_Editable.docx', $false, $true)
 $doc.ExportAsFixedFormat('C:\Users\tania\AndroidStudioProjects\PharmaMobil\tmp\doc11\verificacion.pdf',17)
 Write-Output "PAGES=$($doc.ComputeStatistics(2))"
 $doc.Close(0)
} finally { $word.Quit() }
