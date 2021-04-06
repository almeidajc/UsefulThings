/* ACLARACION, LA HORA QUE MANEJA HAY QUE RESTARLE 3 HORAS*/

-- Monitor active queries
SELECT TOP 100 login_name,Query.*
FROM sys.dm_pdw_exec_requests Query
LEFT JOIN sys.dm_pdw_exec_sessions Users ON Query.session_id = Users.session_id
WHERE Query.status not in ('Completed','Failed','Cancelled')
  AND Query.session_id <> session_id()
ORDER BY Query.submit_time DESC;



-- Find top 10 queries longest running queries
SELECT TOP 100 login_name,Query.*
FROM sys.dm_pdw_exec_requests Query
LEFT JOIN sys.dm_pdw_exec_sessions Users ON Query.session_id = Users.session_id
WHERE Query.status = 'Running'
AND Query.session_id <> session_id()
ORDER BY Query.total_elapsed_time DESC;