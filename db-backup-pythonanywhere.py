import os
import datetime
from zipfile import ZipFile

#
# Author - Anurag Rana
# anuragrana31189 at gmail dot com
# place in home directory. schedule with task tab on pythonanywhere server.
# https://www.pythoncircle.com/post/360/how-to-backup-database-periodically-on-pythonanywhere-server/
#pg_restore -d sms1 -U super -C pgbackup2024-12-15-0610.dump
#pg_dump -U super -f backup.sql sms
#psql -d sms -f backup.sql


BACKUP_DIR_NAME = "pg_backups"
DAYS_TO_KEEP_BACKUP = 3
FILE_PREFIX = "my_db_backup_"
FILE_SUFFIX_DATE_FORMAT = "%Y%m%d%H%M%S"
USERNAME = "trinhvn72"
DBNAME = USERNAME+"$sms"


# get today's date and time
timestamp = datetime.datetime.now().strftime(FILE_SUFFIX_DATE_FORMAT)
backup_filename = BACKUP_DIR_NAME+"/"+FILE_PREFIX+timestamp+".dump"

os.system("pg_dump --host=TrinhVN72-4242.postgres.pythonanywhere-services.com --port=14242 --username=super --format=c --file=" + backup_filename + " sms")

#os.system("mysqldump -u "+USERNAME+" -h "+USERNAME+".mysql.pythonanywhere-services.com '"+DBNAME+"'  > "+backup_filename)


# creating zip file
zip_filename = BACKUP_DIR_NAME+"/"+FILE_PREFIX+timestamp+".zip"
with ZipFile(zip_filename, 'w') as zip:
    zip.write(backup_filename, os.path.basename(backup_filename))

os.remove(backup_filename)

# deleting old files

list_files = os.listdir(BACKUP_DIR_NAME)

back_date = datetime.datetime.now() - datetime.timedelta(days=DAYS_TO_KEEP_BACKUP)
back_date = back_date.strftime(FILE_SUFFIX_DATE_FORMAT)

length = len(FILE_PREFIX)

# deleting files older than DAYS_TO_KEEP_BACKUP days
for f in list_files:
    filename = f.split(".")[0]
    if "zip" == f.split(".")[1]:
        suffix = filename[length:]
        if suffix < back_date:
            print("Deleting file : "+f)
            os.remove(BACKUP_DIR_NAME + "/" + f)



# restoring backup
# mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com 'yourusername$dbname'  < db-backup.sql

# reference
# https://help.pythonanywhere.com/pages/MySQLBackupRestore/
