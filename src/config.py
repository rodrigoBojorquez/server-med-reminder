class DevelopConfig():
    DEBUG= True
    HOST= "0.0.0.0"
    MYSQL_HOST= "localhost"
    MYSQL_USER= "root"
    MYSQL_PASSWORD= "root"
    MYSQL_DB= "med_reminder"

config = {
    "development": DevelopConfig
}