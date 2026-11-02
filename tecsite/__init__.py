# PyMySQL reemplaza a mysqlclient: no necesita compilar librerías de C.
import pymysql

pymysql.install_as_MySQLdb()
