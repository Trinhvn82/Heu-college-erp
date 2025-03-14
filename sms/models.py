#from asyncio.windows_events import NULL
from cProfile import label
from xml.etree.ElementTree import tostring
from django.db import models
from simple_history.models import HistoricalRecords
from info.models import User

# Create your models here.
tl_choice = (
    ("Photo", "Photo"),
    ("Công chứng", "Công chứng"),
    ("Bản sao", "Bản sao"),
    ("Có xác nhận", "Có xác nhận"),
    ("Chưa xác nhận", "Chưa xác nhận"),
)
st_choice = (
    ("Thiếu", "Thiếu"),
    ("Đủ", "Đủ"),
)
td_choice = (
    ("Cử nhân", "Cử nhân"),
    ("Thạc sĩ", "Thạc sĩ"),
    ("Tiến sĩ", "Tiến sĩ"),
    ("Giáo sư", "Giáo sư"),
)
pl_choice = (
    ("Lập kế hoạch", "Lập kế hoạch"),
    ("Đã hoàn thành", "Đã hoàn thành"),
)

class TeacherDeptInfo(models.Model):
    dept_name = models.CharField(max_length=50)

    def __str__(self):
        return self.dept_name

class TeacherSubInfo(models.Model):
    sub_name = models.CharField(max_length=50)

    def __str__(self):
        return self.sub_name

class TeacherInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender_choice = (
        ("male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    #teacher_img = models.ImageField(default=NULL)
    passing_year = models.CharField(max_length=100)
    joining_date = models.DateField()
    dept_type = models.ForeignKey(TeacherDeptInfo, on_delete=models.CASCADE)
    sub_type = models.ForeignKey(TeacherSubInfo, on_delete=models.CASCADE)
    salary = models.IntegerField()

    def __str__(self):
        return self.name
class HocphiStatus(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten

class Hocky(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=20)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten

class Monhoc(models.Model):
    ma = models.CharField(max_length=100)
    ten = models.CharField(max_length=100)
    chuongtrinh = models.CharField(max_length=100)
    sotinchi = models.IntegerField()
    sogio_lt = models.IntegerField(null=True)
    sogio_th = models.IntegerField(null=True)
    sogio_kt = models.IntegerField(null=True)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
        ordering = ["-id"]

    def __str__(self):
        #return self.ten
        return self.chuongtrinh +': ' + self.ma + '-' + self.ten

class SvStatus(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten
        
class Ctdt(models.Model):
    ten = models.CharField(max_length=100)
    khoa = models.CharField(max_length=100)
    khoahoc = models.IntegerField()
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Danh mục CTĐT"
        verbose_name_plural = "Danh mục CTĐT"
        ordering = ["-id"]

    def __str__(self):
        return self.ten

class Trungtam(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
 
    def __str__(self):
        return self.ten

class Phong(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
 
    def __str__(self):
        return self.ten

class Lop(models.Model):
    ma = models.CharField(max_length=100)
    ten = models.CharField(max_length=100)
    #trungtam = models.CharField(max_length=100)
    trungtam = models.ForeignKey(Trungtam, on_delete=models.CASCADE)
    ctdt = models.ForeignKey(Ctdt, on_delete=models.CASCADE)
    # mhs = models.ManyToManyField(Monhoc, default= None , blank= True)
    history = HistoricalRecords()
    def __str__(self):
        return self.ma


class Hssv(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    msv = models.CharField(max_length=100, blank=True, default='TC0001')
    hoten = models.CharField(max_length=100)
    #image = models.FileField(blank=True)
    #image = models.ImageField(upload_to='uploads/',blank=True)
    #image_data = models.BinaryField(null=True)
    #lop = models.CharField(max_length=100)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE, blank=True, null=True)
    #gender = models.CharField(choices=gender_choice, max_length=10)
    #status = models.CharField(choices=st_choice, max_length=50)
    status = models.ForeignKey(SvStatus, on_delete=models.CASCADE, default=1)
    #status = models.IntegerField(choices=st_choice, default= 1)
    namsinh = models.DateField(null=True)
    gioitinh = models.CharField(max_length=30, blank=True, null=True)
    dantoc = models.CharField(max_length=30, blank=True, null=True)
    noisinh = models.CharField(max_length=200, blank=True, null=True)
    quequan = models.CharField(max_length=200, blank=True, null=True)
    diachi = models.CharField(max_length=200, blank=True, null=True)
    xa = models.CharField(max_length=100, blank=True, null=True)
    huyen = models.CharField(max_length=100, blank=True, null=True)
    tinh = models.CharField(max_length=100, blank=True, null=True)
    cccd = models.CharField(max_length=100, blank=True, null=True)
    hotenbo = models.CharField(max_length=200, blank=True, null=True)
    hotenme = models.CharField(max_length=200, blank=True, null=True)
    sdths = models.CharField(max_length=100, blank=True, null=True)
    sdtph = models.CharField(max_length=100, blank=True, null=True)
    hs_syll = models.BooleanField(default= False)
    hs_pxt = models.BooleanField(default= False)
    hs_btn = models.BooleanField(default= False)
    hs_gcntttt = models.BooleanField(default= False)
    hs_hbthcs = models.BooleanField(default= False)
    hs_cccd = models.BooleanField(default= False)
    hs_gks = models.BooleanField(default= False)
    hs_shk = models.BooleanField(default= False)
    hs_a34 = models.BooleanField(default= False)
    hs_status = models.CharField(choices=st_choice, max_length=50, blank=True)

    ghichu = models.CharField(max_length=500, blank=True, null=True)

    history = HistoricalRecords()
    def __str__(self):
        return self.hoten


class Hsgv(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ma = models.CharField(max_length=100)
    hoten = models.CharField(max_length=100)
    namsinh = models.DateField(blank=True, null=True)
    cccd = models.CharField(max_length=100, null=True)
    ngaycap = models.DateField(blank=True, null=True)
    noicap = models.CharField(max_length=100, blank=True, null=True)
    diachi = models.CharField(max_length=100, null=True)
    sdt = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, null=True)
    mst = models.CharField(max_length=100, blank=True, null=True)
    bhxh = models.CharField(max_length=100, blank=True, null=True)
    dongbhxh = models.CharField(max_length=100, blank=True, null=True)
    stk = models.CharField(max_length=100, blank=True, null=True)
    nh = models.CharField(max_length=100, blank=True, null=True)
    cn = models.CharField(max_length=100, blank=True, null=True)

    #gender = models.CharField(choices=gender_choice, max_length=10)
    trinhdo = models.CharField(choices=td_choice, max_length=50, blank=True, null=True)
    truongtn = models.CharField(max_length=100, blank=True, null=True)
    nganhtn = models.CharField(max_length=100, blank=True, null=True)
    shdtg = models.CharField(max_length=100, blank=True, null=True)
    ngayky = models.DateField(blank=True, null=True)
    ngayhh = models.DateField(blank=True, null=True)
    #namsinh = models.DateField()
    hs_btn = models.BooleanField(default= False)
    hs_bd = models.BooleanField(default= False)
    hs_cc = models.BooleanField(default= False)
    hs_syll = models.BooleanField(default= False)
    hs_ccta = models.BooleanField(default= False)
    hs_ccth = models.BooleanField(default= False)
    hs_status = models.CharField(choices=st_choice, max_length=50, blank=True)
    ghichu = models.CharField(max_length=500, blank=True, null=True)
    history = HistoricalRecords()
 
    def __str__(self):
        return self.hoten

class Hsns(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ma = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    hoten = models.CharField(max_length=100)
    diachi = models.CharField(max_length=100, blank=True, null=True)
    quequan = models.CharField(max_length=100, blank=True, null=True)
    #namsinh = models.DateField()
    sdt = models.CharField(max_length=100, blank=True, null=True)
    gioitinh = models.CharField(max_length=100, blank=True, null=True)
    cccd = models.CharField(max_length=100, blank=True, null=True)
    ghichu = models.CharField(max_length=500, blank=True, null=True)
    phong = models.ForeignKey(Phong, on_delete=models.CASCADE, null=True, blank=True)
    history = HistoricalRecords()
 
    def __str__(self):
        return self.hoten
    
    
class CtdtMonhoc(models.Model):
    #ten = models.CharField(max_length=100)
    hocky = models.IntegerField()
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    ctdt = models.ForeignKey(Ctdt, on_delete=models.CASCADE)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Chương trình đào tạo môn học"
        verbose_name_plural = "Chương trình đào tạo môn học"
        ordering = ["id"]

    def __str__(self):
        return self.ctdt.ten
    
class NsLop(models.Model):
    ns = models.ForeignKey(Hsns, on_delete=models.CASCADE)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    def __str__(self):
        return self.lop.ten
    
class LopMonhoc(models.Model):
    #ten = models.CharField(max_length=100)
    ngaystart = models.DateField(blank= True, null=True)
    ngayend = models.DateField(blank= True, null=True)
    #gender = models.CharField(choices=gender_choice, max_length=10)
    status = models.CharField(choices=pl_choice, max_length=50)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    hsdt = models.CharField(max_length=500, default= "", blank= True, null=True)
    hsdt1 = models.BooleanField(default= False)
    hsdt2 = models.BooleanField(default= False)
    hsdt3 = models.BooleanField(default= False)     
    hsdt4 = models.BooleanField(default= False)
    history = HistoricalRecords()
    def __str__(self):
        return self.monhoc.ten

class Lichhoc(models.Model):
    #ten = models.CharField(max_length=100)
    trungtam = models.CharField(max_length=100, blank= True, null=True)
    diadiem = models.CharField(max_length=100, blank= True, null=True)
    thoigian = models.DateTimeField()
    #tgbd = models.DateTimeField()
    #tgkt = models.DateTimeField()
    sotiet = models.IntegerField(default= 1)
    status = models.CharField(choices=pl_choice, max_length=50)
    ghichu = models.TextField(default= "", max_length=500,blank= True, null=True)
    #TenTT = models.IntegerField()
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    giaovien = models.ForeignKey(Hsgv, on_delete=models.CASCADE, blank= True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.lop.ten + "-" + self.monhoc.ten


class Hocphi(models.Model):
    hk = models.IntegerField()
    thoigian = models.DateField(default= None, blank= True)
    sotien = models.IntegerField(default= 0, blank= True)
    hpstatus = models.IntegerField(default= 1)
    ghichu = models.TextField(default= "", max_length=500,blank= True)
    status = models.IntegerField(default= 0)
    #TenTT = models.IntegerField()
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return self.lop.ten + "-" + self.sv.hoten

class Hp81(models.Model):
    #TenTT = models.IntegerField()
    #status = models.IntegerField(choices=st_choice1, default= 1)
    status = models.ForeignKey(HocphiStatus, on_delete=models.CASCADE)
    thoigian = models.DateField(default= None, blank= True, null=True)
    sotien1 = models.IntegerField(default= 0, blank= True, null=True)
    sotien2 = models.IntegerField(default= 0, blank= True, null=True)
    hk = models.ForeignKey(Hocky, on_delete=models.CASCADE)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    ghichu = models.TextField(default= "", max_length=500,blank= True, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.hk.ten

class Hs81(models.Model):
    #hk = models.IntegerField()
    status = models.CharField(choices=st_choice, max_length=20)
    thoigian = models.DateField(default= None, blank= True, null=True)
    ddn = models.BooleanField(default= False)
    cntn = models.BooleanField(default= False)
    btn = models.BooleanField(default= False)
    xnct = models.BooleanField(default= False)
    cccd = models.BooleanField(default= False)
    cccdbo = models.BooleanField(default= False)
    cccdme = models.BooleanField(default= False)
    gks = models.BooleanField(default= False)
    ghichu = models.TextField(max_length=500,blank= True, null=True)
    hk = models.ForeignKey(Hocky, on_delete=models.CASCADE)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return self.hk.ten


class Diemdanh(models.Model):
    status = models.IntegerField(default=1)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    lichhoc = models.ForeignKey(Lichhoc, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return self.sv.hoten

class DiemdanhAll(models.Model):
    ten = models.CharField(max_length=100)
    sdt = models.CharField(max_length=100)
    diachi = models.CharField(max_length=300)
    status = models.IntegerField()
    def __str__(self):
        return self.ten

class LogDiem(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    capnhat_at = models.DateTimeField(default=None, blank = True, null=True)
    def __str__(self):
        return self.created_at

class Loaidiem(models.Model):
    ma = models.IntegerField(default= 1)
    trunglap = models.IntegerField(default= 1)
    heso = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100, null=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten



class Diemthanhphan(models.Model):
    #ghichu = models.CharField(max_length=300)
    diem = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.IntegerField(default= 0)
    tp = models.ForeignKey(Loaidiem, on_delete=models.CASCADE)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    log = models.ForeignKey(LogDiem, on_delete=models.CASCADE, null= True)
    history = HistoricalRecords()
    def __str__(self):
        return self.sv.hoten + "-" + self.monhoc.ten + "-" + self.tp.ten

class LopHk(models.Model):
    start_hk = models.DateField(default= None,blank= True, null=True)
    end_hk = models.DateField(default= None,blank= True, null=True)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    hk = models.ForeignKey(Hocky, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Ttgv(models.Model):
    sotien1 = models.IntegerField(default= 0, blank= True, null=True)
    sotien2 = models.IntegerField(default= 0, blank= True, null=True)
    ghichu = models.TextField(default= "", max_length=500,blank= True, null=True)
    lopmh = models.ForeignKey(LopMonhoc, on_delete=models.CASCADE)
    gv = models.ForeignKey(Hsgv, on_delete=models.CASCADE)
    history = HistoricalRecords()

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    mota = models.CharField(max_length=100)
    history = HistoricalRecords()
    def __str__(self):
        return self.file.name
    
class Giayto_hs81(models.Model):
    ten = models.CharField(max_length=100)
    format = models.CharField(choices=tl_choice, max_length=50, blank=True, null = True)
    soluong = models.IntegerField(default= 0)
    status = models.CharField(choices=st_choice, max_length=50, blank=True, null = True)
    hs81 = models.ForeignKey(Hs81, on_delete=models.CASCADE)
    softfile = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, blank=True, null = True)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten