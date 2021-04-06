$User = "#{usuario}#"
$Pass = ConvertTo-SecureString -String "#{contraseña}#" -AsPlainText -Force
$Credenciales = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $Pass

Connect-MsolService -Credential $Credenciales
$Results = Get-MsolUser -ALL | Where-Object {($_.licenses).AccountSkuId -match "POWER_BI_PRO"} | SELECT UserPrincipalName

$Results | Export-Csv -Path "#{rutaPBIPro.csv}#"


$ResultsE = Get-MsolUser -ALL | Where-Object {($_.licenses).AccountSkuId -match "ENTERPRISEPREMIUM"} | SELECT UserPrincipalName

$ResultsE | Export-Csv -Path "#{rutaE5.csv}#"

exit