import os
import datetime
from zipfile import ZipFile

#
# Author - Anurag Rana
# anuragrana31189 at gmail dot com
# place in home directory. schedule with task tab on pythonanywhere server.
# https://www.pythoncircle.com/post/360/how-to-backup-database-periodically-on-pythonanywhere-server/
#

BACKUP_DIR_NAME = "pg_backups"
DAYS_TO_KEEP_BACKUP = 3
FILE_PREFIX = "my_db_backup_"
FILE_SUFFIX_DATE_FORMAT = "%Y%m%d%H%M%S"
USERNAME = "trinhvn72"
DBNAME = USERNAME+"$sms"


# get today's date and time
timestamp = datetime.datetime.now().strftime(FILE_SUFFIX_DATE_FORMAT)
backup_filename = BACKUP_DIR_NAME+"/"+FILE_PREFIX+timestamp+".dump"
#os.system("pg_dump -U super -h TrinhVN72-4242.postgres.pythonanywhere-services.com -p 14242 sms > dump.sql")
os.system("pg_dump --host=localhost --port=5432 --username=postgres --format=c --file=heu-backup.dump temp4")

#pg_dump --host=TrinhVN72-4242.postgres.pythonanywhere-services.com --port=14242 --username=super --format=c --file=pgbackup`date +%F-%H%M`.dump sms
# restoring backup
# mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com 'yourusername$dbname'  < db-backup.sql

# reference
# https://help.pythonanywhere.com/pages/MySQLBackupRestore/
