# Añade estas líneas para que Django use PyMySQL
import pymysql

pymysql.version_info = (1, 4, 6, "final", 0)  # Fija una versión para compatibilidad
pymysql.install_as_MySQLdb()
