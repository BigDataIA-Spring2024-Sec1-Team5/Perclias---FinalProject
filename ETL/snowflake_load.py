import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import os

def load_data_to_snowflake(file_path):
   snowflake_user = os.getenv('snowflake_user')
   snowflake_password = os.getenv('snowflake_password')
   snowflake_account = os.getenv('snowflake_account')
   snowflake_database = os.getenv('snowflake_database')
   snowflake_schema = os.getenv('snowflake_schema')

   conn = snowflake.connector.connect(
       user=snowflake_user,
       password=snowflake_password,
       account=snowflake_account,
       database=snowflake_database,
       schema=snowflake_schema
   )

   cur = conn.cursor()
   data = pd.read_csv(file_path)
   data.columns = ['TITLE', 'CONTENT']
   table_name = 'SCRAPPED_DATA1'
   success, nchunks, nrows, _ = snowflake.connector.pandas_tools.write_pandas(conn, data, table_name)
   print(f"Success: {success}, Number of chunks: {nchunks}, Number of rows inserted: {nrows}")
   conn.commit()
   conn.close()

def fetch_data_from_snowflake():
   snowflake_user = os.getenv('snowflake_user')
   snowflake_password = os.getenv('snowflake_password')
   snowflake_account = os.getenv('snowflake_account')
   snowflake_database = os.getenv('snowflake_database')
   snowflake_schema = os.getenv('snowflake_schema')
   table_name = os.getenv('table_name')

   ctx = snowflake.connector.connect(
       user=snowflake_user,
       password=snowflake_password,
       account=snowflake_account,
       database=snowflake_database,
       schema=snowflake_schema
   )
   cur = ctx.cursor()
   try:
       cur.execute(f"SELECT TITLE, CONTENT FROM {table_name}")
       rows = cur.fetchall()
       return [(row[0], row[1]) for row in rows]
   finally:
       cur.close()
       ctx.close()