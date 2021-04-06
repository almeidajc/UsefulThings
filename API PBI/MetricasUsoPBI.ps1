$User = "#{usuario}#"
$Pass = ConvertTo-SecureString -String "#{contraseña}#" -AsPlainText -Force
$Credenciales = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $Pass

 

Login-PowerBI -Credential $Credenciales
 

#Simpre inicio con las 24 horas de un mismo d�a
$Comienzo = '2020-09-20T00:00:00.000'
$Fin = '2020-09-20T23:59:59.000'
 #Recorro la cantidad de d�as que quiero, por defecto reccorremos 1 d�as posteriores a la fecha de comienzo
For ($i=0; $i -le 2; $i++) {

 

[datetime]$Comienzo = $Comienzo
$Comienzo.AddDays($i)

 

[datetime]$Fin = $Fin
$Fin.AddDays($i)

 


$Results = Get-PowerBIActivityEvent -StartDateTime $Comienzo.AddDays($i).ToString("yyyy-MM-ddTHH:mm:ss.000") -EndDateTime $Fin.AddDays($i).ToString("yyyy-MM-ddTHH:mm:ss.000") -ActivityType 'ViewReport'

 

$ResultsDashboard = Get-PowerBIActivityEvent -StartDateTime $Comienzo.AddDays($i).ToString("yyyy-MM-ddTHH:mm:ss.000") -EndDateTime $Fin.AddDays($i).ToString("yyyy-MM-ddTHH:mm:ss.000") -ActivityType 'ViewDashboard'

 

$ComienzoRuta = "'"
$ComienzoRuta += $Comienzo.AddDays($i).ToString("yyyy-MM-ddTHH:mm:ss.000")
$ComienzoRuta += "'"

 

#Aca poner la ruta destino del Csv
$Ruta = '#{rutaorigen}#'
$Ruta += '\LogsPowerBIViewReport_'
$Ruta += $ComienzoRuta.Substring(1,10)
$Ruta += '.Csv'

 

($Results | ConvertFrom-Json).data.attributes | Export-Csv -Path $Ruta -NoTypeInformation


 

#Lo mismo para las metricas de Dashboard
$Ruta = '#{rutaorigen}#'
$Ruta += '\LogsPowerBIViewDashboard_'
$Ruta += $ComienzoRuta.Substring(1,10)
$Ruta += '.Csv'

 

$ResultsDashboard | Export-Csv -Path $Ruta -NoTypeInformation -Append
}

exit