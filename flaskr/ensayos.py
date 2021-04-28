import DataBaseConnection
db = DataBaseConnection
id='2225655'
correo='admin'
birth='2002-03-30'
address='lolazo'
pssw='admin'
q = 'select * from usuario'
print(db.sql_query(q))