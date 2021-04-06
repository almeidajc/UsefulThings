SELECT U.* FROM [part].[PBIMetricas_Usuarios] U 
LEFT JOIN [part].[PBIMetricas] M ON M.USERID = U.MAIL AND DATEPART(m, M.CreationTime) = DATEPART(m, DATEADD(m, -1, getdate())) AND DATEPART(yyyy, M.CreationTime) = DATEPART(yyyy, DATEADD(m, -1, getdate()))
WHERE U.TipoLicencia = 'Power BI Pro' AND M.USERID IS NULL