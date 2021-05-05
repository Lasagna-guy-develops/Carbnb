import DataBaseConnection
db = DataBaseConnection
tag='HGW537'
model='spark'
year='2015'
id=1
price='75000'
cars = db.sql_query('select * from carro;')
