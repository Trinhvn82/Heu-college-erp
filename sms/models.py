#from asyncio.windows_events import NULL
from cProfile import label
from xml.etree.ElementTree import tostring
from django.db import models
from simple_history.models import HistoricalRecords
from info.models import User

# Create your models here.
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
    sogio_lt = models.IntegerField()
    sogio_th = models.IntegerField()
    sogio_kt = models.IntegerField()
    history = HistoricalRecords()
 
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
    lop = models.CharField(max_length=100)
    malop = models.ForeignKey(Lop, on_delete=models.CASCADE, default=1)
    st_choice = (
        (1, "Bình thường"),
        (2, "Bảo lưu"),
        (3, "Chuyển lớp"),
        (4, "Nghỉ học"),
    )
    #gender = models.CharField(choices=gender_choice, max_length=10)
    #status = models.CharField(choices=st_choice, max_length=50)
    status = models.ForeignKey(SvStatus, on_delete=models.CASCADE, default=1)
    #status = models.IntegerField(choices=st_choice, default= 1)
    namsinh = models.DateField()
    gioitinh = models.CharField(max_length=30, blank=True)
    dantoc = models.CharField(max_length=30, blank=True)
    noisinh = models.CharField(max_length=200, blank=True)
    quequan = models.CharField(max_length=200, blank=True)
    diachi = models.CharField(max_length=200, blank=True)
    xa = models.CharField(max_length=100, blank=True)
    huyen = models.CharField(max_length=100, blank=True)
    tinh = models.CharField(max_length=100, blank=True)
    cccd = models.CharField(max_length=100, blank=True)
    hotenbo = models.CharField(max_length=200, blank=True)
    hotenme = models.CharField(max_length=200, blank=True)
    sdths = models.CharField(max_length=100, blank=True)
    sdtph = models.CharField(max_length=100, blank=True)
    ghichu = models.CharField(max_length=500, blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.hoten


class Hsgv(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ma = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    hoten = models.CharField(max_length=100)
    diachi = models.CharField(max_length=100, blank=True)
    quequan = models.CharField(max_length=100, blank=True)
    #namsinh = models.DateField()
    sdt = models.CharField(max_length=100, blank=True)
    gioitinh = models.CharField(max_length=100, blank=True)
    cccd = models.CharField(max_length=100, blank=True)
    tthn = models.CharField(max_length=100, blank=True)
    dantoc = models.CharField(max_length=100, blank=True)
    loaihd = models.CharField(max_length=100, blank=True)
    hocham = models.CharField(max_length=100, blank=True)
    hocvi = models.CharField(max_length=100, blank=True)
    stk = models.CharField(max_length=100, blank=True)
    bank = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    thoihanhd = models.DateField(default=None, blank=True)
    hsgv = models.CharField(max_length=500, blank=True)
    history = HistoricalRecords()
 
    def __str__(self):
        return self.hoten

class Hsns(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ma = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    hoten = models.CharField(max_length=100)
    diachi = models.CharField(max_length=100, blank=True)
    quequan = models.CharField(max_length=100, blank=True)
    #namsinh = models.DateField()
    sdt = models.CharField(max_length=100, blank=True)
    gioitinh = models.CharField(max_length=100, blank=True)
    cccd = models.CharField(max_length=100, blank=True)
    ghichu = models.CharField(max_length=500, blank=True)
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
    def __str__(self):
        return self.hocky
    
class NsLop(models.Model):
    ns = models.ForeignKey(Hsns, on_delete=models.CASCADE)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    def __str__(self):
        return self.lop.ten
    
class LopMonhoc(models.Model):
    #ten = models.CharField(max_length=100)
    ngaystart = models.DateField(default= None,blank= True)
    ngayend = models.DateField(default= None,blank= True)
    st_choice = (
        ("Lập kế hoạch", "Lập kế hoạch"),
        ("Đã hoàn thành", "Đã hoàn thành"),
    )
    #gender = models.CharField(choices=gender_choice, max_length=10)
    status = models.CharField(choices=st_choice, max_length=50)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    hsdt = models.CharField(max_length=500, default= "", blank= True)
    hsdt1 = models.BooleanField(default= False)
    hsdt2 = models.BooleanField(default= False)
    hsdt3 = models.BooleanField(default= False)     
    hsdt4 = models.BooleanField(default= False)
    history = HistoricalRecords()
    def __str__(self):
        return self.monhoc.ten

class Lichhoc(models.Model):
    #ten = models.CharField(max_length=100)
    st_choice = (
        ("Lập kế hoạch", "Lập kế hoạch"),
        ("Đã hoàn thành", "Đã hoàn thành"),
    )
    trungtam = models.CharField(max_length=100, blank= True)
    diadiem = models.CharField(max_length=100, blank= True)
    thoigian = models.DateTimeField()
    #tgbd = models.DateTimeField()
    #tgkt = models.DateTimeField()
    sotiet = models.IntegerField(default= 1)
    status = models.CharField(choices=st_choice, max_length=50)
    ghichu = models.TextField(default= "", max_length=500,blank= True)
    #TenTT = models.IntegerField()
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    giaovien = models.ForeignKey(Hsgv, on_delete=models.CASCADE, blank= True)
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
    ghichu = models.TextField(default= "", max_length=500,blank= True)
    sotien1 = models.IntegerField(default= 0, blank= True)
    sotien2 = models.IntegerField(default= 0, blank= True)
    #TenTT = models.IntegerField()
    #status = models.IntegerField(choices=st_choice1, default= 1)
    status = models.ForeignKey(HocphiStatus, on_delete=models.CASCADE)
    hk = models.ForeignKey(Hocky, on_delete=models.CASCADE)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return self.hk.ten

class Hs81(models.Model):
    #hk = models.IntegerField()
    tt_choice = (
        ("Thiếu", "Thiếu"),
        ("Đủ", "Đủ"),
    )
    status = models.CharField(choices=tt_choice, max_length=20)
    thoigian = models.DateField(default= None, blank= True)
    ddn = models.BooleanField(default= False)
    cntn = models.BooleanField(default= False)
    btn = models.BooleanField(default= False)
    xnct = models.BooleanField(default= False)
    cccd = models.BooleanField(default= False)
    cccdbo = models.BooleanField(default= False)
    cccdme = models.BooleanField(default= False)
    gks = models.BooleanField(default= False)
    ghichu = models.TextField(default= "", max_length=500,blank= True)
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
    def __str__(self):
        return self.created_at

class Loaidiem(models.Model):
    ma = models.IntegerField(default= 1)
    trunglap = models.IntegerField(default= 1)
    heso = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten



class Diemthanhphan(models.Model):
    #ghichu = models.CharField(max_length=300)
    diem = models.IntegerField()
    status = models.IntegerField(default= 0)
    tp = models.ForeignKey(Loaidiem, on_delete=models.CASCADE)
    sv = models.ForeignKey(Hssv, on_delete=models.CASCADE)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.CASCADE)
    log = models.ForeignKey(LogDiem, on_delete=models.CASCADE, null= True)
    history = HistoricalRecords()
    def __str__(self):
        return self.sv.hoten + "-" + self.monhoc.ten + "-" + self.tp.ten

class LopHk(models.Model):
    start_hk = models.DateField(default= None,blank= True)
    end_hk = models.DateField(default= None,blank= True)
    lop = models.ForeignKey(Lop, on_delete=models.CASCADE)
    hk = models.ForeignKey(Hocky, on_delete=models.CASCADE)
    history = HistoricalRecords()

class Ttgv(models.Model):
    sotien1 = models.IntegerField(default= 0, blank= True)
    sotien2 = models.IntegerField(default= 0, blank= True)
    ghichu = models.TextField(default= "", max_length=500,blank= True)
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