# Permite usar PyMySQL como MySQLdb (caso mysqlclient não esteja disponível)
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except Exception:
    pass
