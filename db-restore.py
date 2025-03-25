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
#psql -U postgres -d sms -f " D:\Coding\Python ANW\dump.sql" --run this from command line for file backup-ed from Python Anywhere
#pg_restore -U username -d dbname -1 filename.dump
os.system("pg_restore --host=localhost --port=5432 --username=postgres -d temp20 sms-backup2024-12-26-0610.dump")
#os.system("psql -U postgres -d sms -f " D:\Coding\Python ANW\dump.sql"")
#psql -d newdb -f db.sql
#pg_restore -U username -d dbname /path/to/dumpfile
#pg_dump --host=TrinhVN72-4242.postgres.pythonanywhere-services.com --port=14242 --username=super --format=c --file=pgbackup`date +%F-%H%M`.dump sms
# restoring backup
# mysql -u yourusername -h yourusername.mysql.pythonanywhere-services.com 'yourusername$dbname'  < db-backup.sql

# reference
# https://help.pythonanywhere.com/pages/MySQLBackupRestore/
