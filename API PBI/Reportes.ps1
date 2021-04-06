$User = "#{usuario}#"
$Pass = ConvertTo-SecureString -String "#{contraseña}#" -AsPlainText -Force
$Credenciales = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $User, $Pass

 

Login-PowerBI -Credential $Credenciales

Invoke-PowerBIRestMethod -Url "https://api.powerbi.com/v1.0/myorg/admin/Groups?%24top=5000&%24expand=reports" -Method Get | ConvertTo-Json | Out-File -FilePath '#{rutaorigen.json}#' 

Invoke-PowerBIRestMethod -Url "https://api.powerbi.com/v1.0/myorg/admin/Groups?%24top=5000&%24expand=dashboards" -Method Get | ConvertTo-Json | Out-File -FilePath '#{rutaorigen.json}#'


