import psycopg2

conn = psycopg2.connect(database="temp1",
                        host="localhost",
                        user="postgres",
                        password="123654",
                        port="5432")
cursor = conn.cursor()


#Hssv
query = """
ALTER TABLE sms_hssv 
ALTER COLUMN gioitinh DROP NOT NULL,
ALTER COLUMN dantoc DROP NOT NULL,
ALTER COLUMN noisinh DROP NOT NULL,
ALTER COLUMN quequan DROP NOT NULL,
ALTER COLUMN diachi DROP NOT NULL,
ALTER COLUMN xa DROP NOT NULL,
ALTER COLUMN huyen DROP NOT NULL,
ALTER COLUMN tinh DROP NOT NULL,
ALTER COLUMN cccd DROP NOT NULL,
ALTER COLUMN hotenbo DROP NOT NULL,
ALTER COLUMN hotenme DROP NOT NULL,
ALTER COLUMN sdths DROP NOT NULL,
ALTER COLUMN sdtph DROP NOT NULL,
ALTER COLUMN ghichu DROP NOT NULL
"""
cursor.execute(query)

#Hsgv

query = """
ALTER TABLE sms_hsgv 
ALTER COLUMN diachi DROP NOT NULL,
ALTER COLUMN quequan DROP NOT NULL,
ALTER COLUMN sdt DROP NOT NULL,
ALTER COLUMN gioitinh DROP NOT NULL,
ALTER COLUMN cccd DROP NOT NULL,
ALTER COLUMN tthn DROP NOT NULL,
ALTER COLUMN dantoc DROP NOT NULL,
ALTER COLUMN loaihd DROP NOT NULL,
ALTER COLUMN hocham DROP NOT NULL,
ALTER COLUMN hocvi DROP NOT NULL,
ALTER COLUMN stk DROP NOT NULL,
ALTER COLUMN bank DROP NOT NULL,
ALTER COLUMN branch DROP NOT NULL,
ALTER COLUMN thoihanhd DROP NOT NULL,
ALTER COLUMN hsgv DROP NOT NULL
"""
cursor.execute(query)

#LopMonhoc

query = """
ALTER TABLE sms_lopmonhoc 
ALTER COLUMN ngaystart DROP NOT NULL,
ALTER COLUMN ngayend DROP NOT NULL,
ALTER COLUMN hsdt DROP NOT NULL
"""
cursor.execute(query)

#LopMonhoc

query = """
ALTER TABLE sms_lophk 
ALTER COLUMN start_hk DROP NOT NULL,
ALTER COLUMN end_hk DROP NOT NULL
"""
cursor.execute(query)

#Lich hoc

query = """
ALTER TABLE sms_lichhoc 
ALTER COLUMN trungtam DROP NOT NULL,
ALTER COLUMN diadiem DROP NOT NULL,
ALTER COLUMN sotiet DROP NOT NULL,
ALTER COLUMN giaovien_id DROP NOT NULL
"""

cursor.execute(query)

#Hoc phi

query = """
ALTER TABLE sms_hocphi
ALTER COLUMN thoigian DROP NOT NULL,
ALTER COLUMN sotien DROP NOT NULL,
ALTER COLUMN ghichu DROP NOT NULL,
ALTER COLUMN status DROP NOT NULL
"""

cursor.execute(query)

query = """
ALTER TABLE sms_hp81
ALTER COLUMN thoigian DROP NOT NULL,
ALTER COLUMN sotien1 DROP NOT NULL,
ALTER COLUMN sotien2 DROP NOT NULL,
ALTER COLUMN ghichu DROP NOT NULL
"""

cursor.execute(query)

# Historical table
#Hssv
query = """
ALTER TABLE sms_historicalhssv 
ALTER COLUMN gioitinh DROP NOT NULL,
ALTER COLUMN dantoc DROP NOT NULL,
ALTER COLUMN noisinh DROP NOT NULL,
ALTER COLUMN quequan DROP NOT NULL,
ALTER COLUMN diachi DROP NOT NULL,
ALTER COLUMN xa DROP NOT NULL,
ALTER COLUMN huyen DROP NOT NULL,
ALTER COLUMN tinh DROP NOT NULL,
ALTER COLUMN cccd DROP NOT NULL,
ALTER COLUMN hotenbo DROP NOT NULL,
ALTER COLUMN hotenme DROP NOT NULL,
ALTER COLUMN sdths DROP NOT NULL,
ALTER COLUMN sdtph DROP NOT NULL,
ALTER COLUMN ghichu DROP NOT NULL
"""
cursor.execute(query)

#Hsgv

query = """
ALTER TABLE sms_historicalhsgv 
ALTER COLUMN diachi DROP NOT NULL,
ALTER COLUMN quequan DROP NOT NULL,
ALTER COLUMN sdt DROP NOT NULL,
ALTER COLUMN gioitinh DROP NOT NULL,
ALTER COLUMN cccd DROP NOT NULL,
ALTER COLUMN tthn DROP NOT NULL,
ALTER COLUMN dantoc DROP NOT NULL,
ALTER COLUMN loaihd DROP NOT NULL,
ALTER COLUMN hocham DROP NOT NULL,
ALTER COLUMN hocvi DROP NOT NULL,
ALTER COLUMN stk DROP NOT NULL,
ALTER COLUMN bank DROP NOT NULL,
ALTER COLUMN branch DROP NOT NULL,
ALTER COLUMN thoihanhd DROP NOT NULL,
ALTER COLUMN hsgv DROP NOT NULL
"""
cursor.execute(query)

#LopMonhoc

query = """
ALTER TABLE sms_historicallopmonhoc 
ALTER COLUMN ngaystart DROP NOT NULL,
ALTER COLUMN ngayend DROP NOT NULL,
ALTER COLUMN hsdt DROP NOT NULL
"""
cursor.execute(query)

#LopMonhoc

query = """
ALTER TABLE sms_historicallophk 
ALTER COLUMN start_hk DROP NOT NULL,
ALTER COLUMN end_hk DROP NOT NULL
"""
cursor.execute(query)

#Lich hoc

query = """
ALTER TABLE sms_historicallichhoc 
ALTER COLUMN trungtam DROP NOT NULL,
ALTER COLUMN diadiem DROP NOT NULL,
ALTER COLUMN sotiet DROP NOT NULL,
ALTER COLUMN giaovien_id DROP NOT NULL
"""

cursor.execute(query)

#Hoc phi

query = """
ALTER TABLE sms_historicalhocphi
ALTER COLUMN thoigian DROP NOT NULL,
ALTER COLUMN sotien DROP NOT NULL,
ALTER COLUMN ghichu DROP NOT NULL,
ALTER COLUMN status DROP NOT NULL
"""

cursor.execute(query)

query = """
ALTER TABLE sms_historicalhp81
ALTER COLUMN thoigian DROP NOT NULL,
ALTER COLUMN sotien1 DROP NOT NULL,
ALTER COLUMN sotien2 DROP NOT NULL,
ALTER COLUMN ghichu DROP NOT NULL
"""

cursor.execute(query)


cursor.close()

conn.commit()

conn.close()
