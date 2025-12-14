import pandas as pd

data = [
    {
        'ma': 'R001',
        'hoten': 'Nguyen Van A',
        'email': 'nguyenvana@example.com',
        'sdt': '0912345678',
        'cccd': '123456789',
        'ngaycap': '2020-01-01',
        'noicap': 'Ha Noi',
        'mst': '123456789',
        'ghichu': 'Note 1',
        'init_pwd': 'matkhau1',
    },
    {
        'ma': 'R002',
        'hoten': 'Tran Thi B',
        'email': 'tranthib@example.com',
        'sdt': '0987654321',
        'cccd': '987654321',
        'ngaycap': '2021-02-02',
        'noicap': 'TP HCM',
        'mst': '987654321',
        'ghichu': 'Note 2',
        'init_pwd': 'matkhau2',
    },
]

df = pd.DataFrame(data)
df.to_excel('tools/renter_import_template.xlsx', index=False)
print('Đã tạo file tools/renter_import_template.xlsx')
