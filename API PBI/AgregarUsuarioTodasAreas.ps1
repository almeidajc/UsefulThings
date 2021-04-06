Connect-PowerBIServiceAccount

Add-PowerBIWorkspaceUser -Scope Organization -Workspace (Get-PowerBIWorkspace -Scope Organization -All) -UserPrincipalName '#{usuario}#' -AccessRight Member