from sqlalchemy import create_engine, MetaData

db_hostname = 'localhost'
db_database = 'Recursos_Humanos'
db_username = 'postgres'
db_password = '1998Mono940603'
db_port = '5432'

connection_url = f"postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_database}"

try:
    engine = create_engine(connection_url)
    conn = engine.connect()
    meta = MetaData()
except Exception as e:
    print(f"Error al conectar con la base de datos: {e}")
