import datetime
import logging
import azure.functions as func
import json
import pyodbc
import pandas as pd
import pandas.io.sql
from azure.eventhub import EventHubProducerClient
from azure.eventhub import EventData
import os
from sqlalchemy import create_engine
import urllib

# Conexion con la base de datos
server = os.environ['Synapse01_URL']
database = os.environ['Synapse01_DataBase']
username = os.environ['Synapse01_Usuario']
password = os.environ['Synapse01_Password']
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

# Conexion con la base de datos
driver = r"{ODBC Driver 17 for SQL Server}"
port = "1433"
params = urllib.parse.quote_plus(
        f"Driver={driver};Server={server},{port};Database={database};Uid={username}@{server};Pwd={password};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    )

engine = create_engine(
        f"mssql+pyodbc:///?odbc_connect={params}",
        # echo=True,
        connect_args={"autocommit": True},
    )

def run(producer, event):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.

    event_data_batch = producer.create_batch()
    event_data_batch.add(EventData(event))
    producer.send_batch(event_data_batch)

def tomar_enviar_datos(contexto):
    sql_query = """
        DECLARE @PeriodoDesde DATETIME, @PeriodoHasta DateTime

        SET @PeriodoHasta = DATEADD(Minute, -3, DATEADD(hour, -3, GetUTCdate()))
		
		UPDATE part.F_Streaming_Dia_Prueba
		SET CargadoPBI = NULL
		WHERE NOT EXISTS 
			 (
				SELECT 1 FROM part.F_Stream_Analytics_asa
                WHERE   part.F_Streaming_Dia_Prueba.BRANCHID = part.F_Stream_Analytics_asa.BranchId
             )
		AND part.F_Streaming_Dia_Prueba.FechaHoraAzure <= DATEADD(MINUTE,-15,GETDATE())
		AND part.F_Streaming_Dia_Prueba.CargadoPBI IN (1,2) /* 1 EN EJECUCION, 2 PROCESADO */

        SELECT top 2000 BranchID, CodProductor
        INTO ##BranchesStreaming2
        FROM PART.[F_Streaming_Dia_Prueba]
        WHERE CargadoPBI IS NULL AND 
		FechaHora < @PeriodoHasta
        AND cast(FechaHora AS Date) = cast(DATEADD(hour, -3, GetUTCdate()) AS Date);
		
		UPDATE PART.[F_Streaming_Dia_Prueba] SET CargadoPBI = 1, FechaHoraAzure = getdate() , AzureFunctionID =  

		'""" + contexto + """' WHERE BranchID IN (SELECT BranchID FROM ##BranchesStreaming2)

        SELECT *
        INTO #ProdStreaming2
        FROM D_Productor  d
        WHERE CodProductor in (
				 SELECT CodProductor FROM ##BranchesStreaming2
				 --PART.[F_Streaming_Dia_Prueba] WHERE BranchID in (SELECT BranchID FROM ##BranchesStreaming2)
        ) group by CodProductor
        """

    with engine.connect() as conn:
        conn.execute(sql_query)
        df = pd.read_sql(sql="""
        SELECT #{CAMPOS}#
        FROM PART.[F_Streaming_Dia_Prueba] f
		LEFT JOIN #ProdStreaming2 p ON p.CodProductor = f.CodProductor
		WHERE f.BranchID IN (SELECT BranchID FROM ##BranchesStreaming2);  """, con=conn) #Consulta SQL que genera el dataframe

        conn.execute("""Drop Table #ProdStreaming2;""")  #Elimino tabla temporal

# convierto el dataframe a un archivo csv y llamo a la función sender
    js_results = df.to_csv(index=False) #orient="table"
    connstring = 'Endpoint=#{conexion string del eventhub}#'
    ehname = '#{nombreeventhub}#'
    producer = EventHubProducerClient.from_connection_string(conn_str=connstring, eventhub_name=ehname)

    with producer:
        run(producer, js_results)

def Actualizar_datos()-> None:
    sql_query = """
        UPDATE PART.[F_Streaming_Dia_Prueba] SET CargadoPBI = 2 WHERE BranchID IN (SELECT BranchID FROM ##BranchesStreaming2) AND CargadoPBI = 1;
        Drop Table ##BranchesStreaming2;
        """
    with engine.connect() as conn:
        conn.execute(sql_query)
		
def main(mytimer: func.TimerRequest, context: func.Context) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    tomar_enviar_datos(context.invocation_id)

    Actualizar_datos()

    logging.info('Id de la funcion: %s', context.invocation_id)