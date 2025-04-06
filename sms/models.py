#from asyncio.windows_events import NULL
from cProfile import label
from xml.etree.ElementTree import tostring
from django.db import models
from simple_history.models import HistoricalRecords
from info.models import User
from django.db.models.functions import StrIndex, Reverse, Right, Concat, Substr
from django.core.validators import FileExtensionValidator
#from sms.formatChecker import ContentTypeRestrictedFileField


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

yn_choice = (
    ("Có", "Có"),
    ("Không", "Không"),
)

gender_choice = (
    ("Nam", "Nam"),
    ("Nữ", "Nữ"),
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
    dept_type = models.ForeignKey(TeacherDeptInfo, on_delete=models.RESTRICT)
    sub_type = models.ForeignKey(TeacherSubInfo, on_delete=models.RESTRICT)
    salary = models.IntegerField()

    def __str__(self):
        return self.name
class HocphiStatus(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Trạng thái Học phí"
        verbose_name_plural = "Danh mục Trạng thái Học phí"
        unique_together = ('ma',)
        ordering = ["id"]
    def __str__(self):
        return self.ten

class Hocky(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=20)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Học kỳ"
        verbose_name_plural = "Danh mục Học kỳ"
        unique_together = ('ma',)
        ordering = ["id"]

    def __str__(self):
        return self.ten

class HeDT(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=20)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Hệ đào tạo"
        verbose_name_plural = "Danh mục Hệ đào tạo"
        unique_together = ('ma',)
        ordering = ["id"]

    def __str__(self):
        return self.ten

class Khoahoc(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=20)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Khóa học"
        verbose_name_plural = "Danh mục Khóa học"
        unique_together = ('ma',)
        ordering = ["id"]

    def __str__(self):
        return self.ten

class Nganh(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=20)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Ngành đào tạo"
        verbose_name_plural = "Danh mục Ngành đào tạo"
        unique_together = ('ma',)
        ordering = ["id"]

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
        verbose_name_plural = "Danh mục Môn học"
        unique_together = ('ma','ten','chuongtrinh')
        ordering = ["-id"]

    def __str__(self):
        return self.ten

class SvStatus(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Trạng thái học viên"
        verbose_name_plural = "Danh mục Trạng thái học viên"
        ordering = ["id"]
        unique_together = ('ma',)

    def __str__(self):
        return self.ten
        
class Ctdt(models.Model):
    ten = models.CharField(max_length=100)
    khoa = models.CharField(max_length=100)
    khoahoc = models.IntegerField()
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Chương trinh đào tạo"
        verbose_name_plural = "Danh mục CTĐT"
        unique_together = ('ten',)
        ordering = ["-id"]

    def __str__(self):
        return self.ten

class Trungtam(models.Model):
    ma = models.IntegerField(default= 1,verbose_name="Mã Trung tâm")
    ten = models.CharField(max_length=100,verbose_name="Tên Trung tâm")
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Trung tâm"
        verbose_name_plural = "Danh mục Trung tâm"
        ordering = ["id"]
        unique_together = ('ma',)
    def __str__(self):
        return self.ten

class Phong(models.Model):
    ma = models.IntegerField(default= 1)
    ten = models.CharField(max_length=100)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Phòng"
        verbose_name_plural = "Danh mục Phòng"
        ordering = ["id"]
        unique_together = ('ma',)

    def __str__(self):
        return self.ten

class Lop(models.Model):
    ma = models.CharField(max_length=100,verbose_name="Mã Lớp")
    ten = models.CharField(max_length=100,verbose_name="Tên Lớp")
    #trungtam = models.CharField(max_length=100)
    trungtam = models.ForeignKey(Trungtam, on_delete=models.RESTRICT,verbose_name="Trung tâm")
    ctdt = models.ForeignKey(Ctdt, on_delete=models.RESTRICT,verbose_name="Chương trình đào tạo")
    # mhs = models.ManyToManyField(Monhoc, default= None , blank= True)
    history = HistoricalRecords()

    class Meta:
        permissions = (
            ('assign_lop', 'can assign lop'),
        )        
        verbose_name = "Lớp"
        verbose_name_plural = "Danh sác Lớp"
        unique_together = ('ma',)
        ordering = ["-id"]

    def __str__(self):
        return self.ten


class Hssv(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, null=True)
    msv = models.CharField(max_length=100, default='TC0001')
    hoten = models.CharField(max_length=100)
    #image = models.FileField(blank=True)
    #image = models.ImageField(upload_to='uploads/',blank=True)
    #image_data = models.BinaryField(null=True)
    #lop = models.CharField(max_length=100)
    lop = models.ForeignKey(Lop, on_delete=models.RESTRICT, blank=True, null=True)
    #gender = models.CharField(choices=gender_choice, max_length=10)
    #status = models.CharField(choices=st_choice, max_length=50)
    status = models.ForeignKey(SvStatus, on_delete=models.RESTRICT, default=1)
    #status = models.IntegerField(choices=st_choice, default= 1)
    namsinh = models.DateField( blank=True, null=True)
    gioitinh = models.CharField(choices=gender_choice, blank=True, null=True)
    dantoc = models.CharField(max_length=30, blank=True, null=True)
    noisinh = models.CharField(max_length=200, blank=True, null=True)
    quequan = models.CharField(max_length=200, blank=True, null=True)
    diachi = models.CharField(max_length=200, blank=True, null=True)
    xa = models.CharField(max_length=100, blank=True, null=True)
    huyen = models.CharField(max_length=100, blank=True, null=True)
    tinh = models.CharField(max_length=100, blank=True, null=True)
    cccd = models.CharField(max_length=100, blank=True, null=True)
    ngaycap = models.DateField(blank=True, null=True, verbose_name = "Ngày cấp")
    noicap = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Nơi cấp")
    stk = models.CharField(max_length=100, blank=True, null=True, verbose_name = "STK")
    nh = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Ngân Hàng")
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

    ghichu = models.TextField(max_length=500, blank=True, null=True)

    # ten = models.GeneratedField(
    #         expression = Concat(Right(hoten, StrIndex(Reverse(hoten), " ")-1), " ",Substr(hoten, 1, StrIndex(hoten, " ")-1)),
    #         output_field = models.TextField(),
    #         db_persist = True
    #     )
    
    history = HistoricalRecords()
    @property
    def ten(self):
        return self.hoten.split()[-1] + " " + self.hoten.split()[0]
    

    class Meta:
        verbose_name = "Học viên"
        verbose_name_plural = "Danh sách học viên"
        ordering = ["msv",]
        unique_together = ('msv',)

    def __str__(self):
        return self.hoten


class Hsgv(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, null=True)
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
    ghichu = models.TextField(max_length=500, blank=True, null=True)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Giáo viên"
        verbose_name_plural = "Danh sách Giáo viên"
        ordering = ["ma",]
        unique_together = ('ma',)

    def __str__(self):
        return self.ma + "|" + self.hoten

class Hsns(models.Model):
    tddt_choice = (
        ("Nghiệp vụ", "Nghiệp vụ"),
        ("Trung cấp", "Trung cấp"),
        ("Cao đẳng", "Cao đẳng"),
        ("Cử nhân", "Cử nhân"),
        ("Thạc sĩ", "Thạc sĩ"),
        ("Tiến sĩ", "Tiến sĩ"),
        ("Giáo sư", "Giáo sư"),
    )
    xldt_choice = (
        ("Xuất sắc", "Xuất sắc"),
        ("Giỏi", "Giỏi"),
        ("Khá", "Khá"),
        ("Trung bình khá", "Trung bình khá"),
        ("Trung bình", "Trung bình"),
    )
    cdcv_choice = (
        ("Nhân viên", "Nhân viên"),
        ("Chuyên viên", "Chuyên viên"),
        ("Phó phòng", "Phó phòng"),
        ("Trưởng phòng", "Trưởng phòng"),
        ("Cố vấn", "Cố vấn"),
        ("Kế toán trưởng", "Kế toán trưởng"),
        ("Phó Hiệu trưởng", "Phó Hiệu trưởng"),
        ("Hiệu trưởng", "Hiệu trưởng"),
        ("Thành viên HĐQT", "Thành viên HĐQT"),
        ("Chủ tịch HĐQT", "Chủ tịch HĐQT"),
    )
    vtcv_choice = (
        ("Hành chính", "Hành chính"),
        ("Nhân sự", "Nhân sự"),
        ("Tạp vụ", "Tạp vụ"),
        ("Khác", "Khác"),
    )
    tthd_choice = (
        ("Đang làm việc", "Đang làm việc"),
        ("Đã nghỉ việc", "Đã nghỉ việc"),
        ("Nghỉ không lương", "Nghỉ không lương"),
        ("Nghỉ thai sản", "Nghỉ thai sản"),
    )

    tcld_choice = (
        ("Chính thức", "Chính thức"),
        ("Thử việc", "Thử việc"),
        ("DV", "DV"),
    )

    loaihd_choice = (
        ("Thời vụ", "Thời vụ"),
        ("Học việc", "Học việc"),
        ("Thử việc", "Thử việc"),
        ("Xác định thời hạn", "Xác định thời hạn"),
        ("Không xác định thời hạn", "Không xác định thời hạn"),
        ("Dịch vụ", "Dịch vụ"),
    )
    user = models.OneToOneField(User, on_delete=models.RESTRICT, null=True)
    ma = models.CharField(max_length=100, verbose_name = "Mã Nhân sự")
    email = models.CharField(max_length=100, verbose_name = "Email")
    hoten = models.CharField(max_length=100, verbose_name = "Họ tên")
    #namsinh = models.DateField()
    gioitinh = models.CharField(choices=gender_choice, blank=True, null=True, verbose_name = "Giới tính")
    namsinh = models.DateField(blank=True, null=True, verbose_name = "năm sinh")
    dantoc = models.CharField(max_length=30, blank=True, null=True, verbose_name = "dân tộc")
    tongiao = models.CharField(max_length=30, blank=True, null=True, verbose_name = "dân tộc")
    quoctich = models.CharField(max_length=30, blank=True, null=True, verbose_name = "dân tộc")
    quequan = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Nguyên quán")
    diachi1 = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Địa chỉ tạm trú")
    diachi2 = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Địa chỉ thường trú")      
    sdt = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Số điện thoại")
    cccd = models.CharField(max_length=100, blank=True, null=True, verbose_name = "CCCD")
    ngaycap = models.DateField(blank=True, null=True, verbose_name = "Ngày cấp")
    noicap = models.DateField(blank=True, null=True, verbose_name = "Ngày cấp")
    mst = models.CharField(max_length=100, blank=True, null=True, verbose_name = "MS Thuế cá nhân")


    tddt = models.CharField(choices=tddt_choice, blank=True, null=True, verbose_name = "Trình độ đào tạo")
    noidt = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Nơi đào tạo")
    kdt = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Khoa đào tạo")
    cndt = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Chuyên ngành")
    namtn = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Năm tốt nghiệp")
    xldt = models.CharField(choices=xldt_choice, blank=True, null=True, verbose_name = "Xếp loại")
    cdcv = models.CharField(choices=cdcv_choice, blank=True, null=True, verbose_name = "Chức danh công việc")
    vtcv = models.CharField(choices=vtcv_choice, blank=True, null=True, verbose_name = "Vị trí công việc")
    shd = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Số hợp đồng")
    ngayky = models.DateField(max_length=100, blank=True, null=True, verbose_name = "Ngày kí")
    ngayhh = models.DateField(blank=True, null=True, verbose_name = "Ngày hết hạn")
    trangthaihd = models.CharField(choices=tthd_choice, blank=True, null=True, verbose_name = "Trạng thái")
    tcld = models.CharField(choices=tcld_choice, blank=True, null=True, verbose_name = "Tính chất lao động")

    loaihd = models.CharField(choices=loaihd_choice, blank=True, null=True, verbose_name = "Loại hợp đồng")
    ngaylv = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Ngày vào làm việc")
    tgcd = models.CharField(choices=yn_choice, blank=True, null=True, verbose_name = "Tham gia công đoàn")
    tgbhxh = models.CharField(choices=yn_choice, blank=True, null=True, verbose_name = "Tham gia BHXH")
    ssbhxh = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Số sổ BHXH")

    tongluong = models.IntegerField(blank=True, null=True, verbose_name = "Tổng lương")
    luongcb = models.IntegerField(blank=True, null=True, verbose_name = "Lương cơ bản (BHXH)")
    stk = models.CharField(max_length=100, blank=True, null=True, verbose_name = "STK")
    nh = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Ngân Hàng")
    chinhanh = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Chi nhánh")

    hs_btn = models.BooleanField(default= False, verbose_name = "Bằng tốt nghiệp")
    hs_bd = models.BooleanField(default= False, verbose_name = "Bảng điểm")
    hs_cc = models.BooleanField(default= False, verbose_name = "Chứng chỉ NVSP/dạy nghề")
    hs_syll = models.BooleanField(default= False, verbose_name = "Sơ yếu lý lịch")
    hs_ccta = models.BooleanField(default= False, verbose_name = "Chứng chỉ tiếng Anh")
    hs_ccth = models.BooleanField(default= False, verbose_name = "Chứng chỉ tin học")
    hs_khac = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Giấy tờ khác")
    hs_status = models.CharField(choices=st_choice, max_length=50, blank=True, verbose_name = "Tình trạng hồ sơ")

    ghichu = models.TextField(max_length=500, blank=True, null=True, verbose_name = "Ghi chú")
    #phong = models.ForeignKey(Phong, on_delete=models.RESTRICT, null=True, blank=True)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Nhân sự"
        verbose_name_plural = "Danh sách Nhân sự"
        ordering = ["ma",]
        unique_together = ('ma',)

    def __str__(self):
        return self.hoten
    
    
class CtdtMonhoc(models.Model):
    #ten = models.CharField(max_length=100)
    #hocky = models.IntegerField()
    monhoc = models.ForeignKey(Monhoc, on_delete=models.RESTRICT)
    ctdt = models.ForeignKey(Ctdt, on_delete=models.RESTRICT)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Chương trình đào tạo môn học"
        verbose_name_plural = "Chương trình đào tạo môn học"
        unique_together = ('ctdt','monhoc',)
        ordering = ['ctdt','-monhoc',]

    def __str__(self):
        return self.ctdt.ten
    
class NsLop(models.Model):
    ns = models.ForeignKey(Hsns, on_delete=models.RESTRICT)
    lop = models.ForeignKey(Lop, on_delete=models.RESTRICT)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Nhân sự lớp"
        verbose_name_plural = "Danh sác Nhân sự lớp"
        unique_together = ('ns','lop',)
        ordering = ["-id"]

    def __str__(self):
        return self.lop.ten
    
class GvLop(models.Model):
    gv = models.ForeignKey(Hsgv, on_delete=models.RESTRICT)
    lop = models.ForeignKey(Lop, on_delete=models.RESTRICT)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Gíao viên lớp"
        verbose_name_plural = "Danh sác Giao viên lớp"
        unique_together = ('gv','lop',)
        ordering = ["-id"]

    def __str__(self):
        return self.lop.ten

class GvMonhoc(models.Model):
    gv = models.ForeignKey(Hsgv, on_delete=models.RESTRICT)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.RESTRICT)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Gíao viên Môn học   "
        verbose_name_plural = "Danh sác Giao viên Môn học"
        unique_together = ('gv','monhoc',)
        ordering = ["-id"]

    def __str__(self):
        return self.lop.ten

class NsPhong(models.Model):
    ns = models.ForeignKey(Hsns, on_delete=models.RESTRICT)
    phong = models.ForeignKey(Phong, on_delete=models.RESTRICT)
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Nhân sự phòng"
        verbose_name_plural = "Danh sác Nhân sự phòng"
        unique_together = ('ns','phong',)
        ordering = ["-id"]
    def __str__(self):
        return self.phong.ten

class LopMonhoc(models.Model):
    #ten = models.CharField(max_length=100)
    ngaystart = models.DateField(blank= True, null=True, verbose_name="Ngày bắt đầu")
    ngayend = models.DateField(blank= True, null=True, verbose_name="Ngày kết thúc")
    #gender = models.CharField(choices=gender_choice, max_length=10)
    status = models.CharField(choices=pl_choice, max_length=50)
    hk = models.ForeignKey(Hocky, on_delete=models.RESTRICT, default= 1)
    monhoc = models.ForeignKey(Monhoc, on_delete=models.RESTRICT)
    lop = models.ForeignKey(Lop, on_delete=models.RESTRICT)
    hsdt = models.TextField(max_length=500, default= "", blank= True, null=True, verbose_name="Ghi chú Xác nhận giảng dạy")
    hsdt1 = models.BooleanField(default= False, verbose_name="Tiến độ, kế hoạch, CTĐT")
    hsdt2 = models.BooleanField(default= False, verbose_name="Phiếu báo giảng")
    hsdt3 = models.BooleanField(default= False, verbose_name="Giáo án")   
    hsdt4 = models.BooleanField(default= False, verbose_name="Sổ tay giảng viên")
    hsdt5 = models.BooleanField(default= False, verbose_name="Danh sách học sinh ký thi")
    hsdt6 = models.BooleanField(default= False, verbose_name="Bài thi")   
    hsdt7 = models.BooleanField(default= False, verbose_name="Đề thi/đáp án")
    history = HistoricalRecords()

    class Meta:
        permissions = (
            ('assign_lopmonhoc', 'can assign lopmonhoc'),
        )        
        verbose_name = "Lớp môn học"
        verbose_name_plural = "Lớp môn học"
        ordering = ["-id","-ngaystart"]
        unique_together = ('lop', 'monhoc',)
    def __str__(self):
        return self.lop.ten + "-" + self.monhoc.ten
    
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
    #lop = models.ForeignKey(Lop, on_delete=models.RESTRICT)
    lmh = models.ForeignKey(LopMonhoc, on_delete=models.RESTRICT, default=1)
    giaovien = models.ForeignKey(Hsgv, on_delete=models.RESTRICT, blank= True, null=True)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Lịch học"
        verbose_name_plural = "Danh sách Lịch học"      
        ordering = ["thoigian",]

    def __str__(self):
        return self.lmh.monhoc.ten


class Hocphi(models.Model):
    hk = models.IntegerField()
    thoigian = models.DateField(default= None, blank= True)
    sotien = models.IntegerField(default= 0, blank= True)
    hpstatus = models.IntegerField(default= 1)
    ghichu = models.TextField(default= "", max_length=500,blank= True)
    status = models.IntegerField(default= 0)
    #TenTT = models.IntegerField()
    lop = models.ForeignKey(Lop, on_delete=models.RESTRICT)
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    history = HistoricalRecords()
    def __str__(self):
        return self.lop.ten + "-" + self.sv.hoten

class Hp81(models.Model):
    #TenTT = models.IntegerField()
    #status = models.IntegerField(choices=st_choice1, default= 1)
    status = models.ForeignKey(HocphiStatus, on_delete=models.RESTRICT)
    thoigian = models.DateField(default= None, blank= True, null=True)
    sotien1 = models.IntegerField(default= 0, blank= True, null=True)
    sotien2 = models.IntegerField(default= 0, blank= True, null=True)
    hk = models.ForeignKey(Hocky, on_delete=models.RESTRICT)
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    ghichu = models.TextField(default= "", max_length=500,blank= True, null=True)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Học phí 81"
        verbose_name_plural = "Danh sách Học phí 81"
        ordering = ["-sv","-hk"]
        unique_together = ('sv', 'hk',)
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
    hk = models.ForeignKey(Hocky, on_delete=models.RESTRICT)
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Hồ sơ 81"
        verbose_name_plural = "Danh sách Hồ sơ 81"
        ordering = ["-sv","-hk"]
        unique_together = ('sv', 'hk',)
    def __str__(self):
        return self.hk.ten


class Diemdanh(models.Model):
    status = models.IntegerField(default=1)
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    lichhoc = models.ForeignKey(Lichhoc, on_delete=models.RESTRICT)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Điểm danh"
        verbose_name_plural = "Danh sách Điểm danh"
        unique_together = ('sv', 'lichhoc',)

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
    ten = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return str(self.id)

class Loaidiem(models.Model):
    ma = models.CharField(default= "KTTX")
    trunglap = models.IntegerField(default= 1, verbose_name="Số lần cho điểm")
    heso = models.IntegerField(default= 1, verbose_name="Hệ số")
    ten = models.CharField(max_length=100, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Điểm thành phần"
        verbose_name_plural = "Danh mục Điểm thành phần"
        ordering = ["-id",]
        unique_together = ('ma',)

    def __str__(self):
        return self.ten



class Diemthanhphan(models.Model):
    #ghichu = models.CharField(max_length=300)
    diem = models.DecimalField(max_digits=5, decimal_places=1, verbose_name="Điểm")
    status = models.IntegerField(default= 0)
    tp = models.ForeignKey(Loaidiem, on_delete=models.RESTRICT, verbose_name="Điểm Thành phần")
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT, verbose_name="Học viên")
    monhoc = models.ForeignKey(Monhoc, on_delete=models.RESTRICT, verbose_name="Môn học")    
    log = models.ForeignKey(LogDiem, on_delete=models.RESTRICT, null= True, verbose_name="ID Log")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Điểm thành phần"
        verbose_name_plural = "Kết quả điểm thành phần"
        ordering = ["sv","monhoc","tp"]

    def __str__(self):
        return str(self.diem)

class LopHk(models.Model):
    start_hk = models.DateField(default= None,blank= True, null=True, verbose_name="Ngày bắt đầu")
    end_hk = models.DateField(default= None,blank= True, null=True, verbose_name="Ngày kết thúc")
    lop = models.ForeignKey(Lop, on_delete=models.PROTECT)
    hk = models.ForeignKey(Hocky, on_delete=models.PROTECT, verbose_name="Học kỳ")
    class Meta:
        verbose_name = "Lớp Học kỳ"
        verbose_name_plural = "Lớp Học kỳ"
        ordering = ["hk",]
        unique_together = ('lop','hk',)

    history = HistoricalRecords()

    def __str__(self): 
        return self.lop.ten + "-" + self.hk.ten


class Ttgv(models.Model):
    sotiet = models.IntegerField(default= 0, blank= True, null=True)
    sotien1 = models.IntegerField(default= 0, blank= True, null=True)
    sotien2 = models.IntegerField(default= 0, blank= True, null=True)
    ghichu = models.TextField(default= "", max_length=500,blank= True, null=True)
    lopmh = models.ForeignKey(LopMonhoc, on_delete=models.RESTRICT)
    gv = models.ForeignKey(Hsgv, on_delete=models.RESTRICT)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Thanh toán giáo viên"
        verbose_name_plural = "Danh sách Thanh toán giáo viên"
        ordering = ["-gv","-lopmh"]
        unique_together = ('gv', 'lopmh',)
    def __str__(self):
        return self.gv.hoten

class GvLmh(models.Model):
    lopmh = models.ForeignKey(LopMonhoc, on_delete=models.RESTRICT, verbose_name="Lớp môn học")
    gv = models.ForeignKey(Hsgv, on_delete=models.RESTRICT, verbose_name="Giáo viên")
    status = models.IntegerField(default= 0)
    history = HistoricalRecords()
    class Meta:
        verbose_name = "Giáo viên lớp môn học"
        verbose_name_plural = "Giáo viên lớp môn học"
        ordering = ["-gv","-lopmh"]
        unique_together = ('gv', 'lopmh',)


    def kick(self):
        self.status = 0
        self.save()

    def hug(self):
        self.status = 1
        self.save()

    def __str__(self):
        return self.lopmh.lop.ten + "|" + self.lopmh.monhoc.ma + "|" + self.lopmh.monhoc.ten

def upload_directory_name(instance, filename):
    import os
    user = getattr(instance, 'user', None)
    if user:
        name = user.username
    else:
        name=str(instance)
    model_name = instance._meta.verbose_name.replace(' ', '-')
    return str(os.path.pathsep).join(["uploads/",model_name, "/" ,filename])

class UploadedFile(models.Model):
    #file = models.FileField(upload_to='uploads/')

    
    file = models.FileField(upload_to="uploads/files/%Y/%m/%d")

    #file = ContentTypeRestrictedFileField(upload_to="uploads/files/%Y/%m/%d", content_types=['image/gif', 'image/jpeg', 'image/png', ],max_upload_size=5242880,blank=True, null=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.CharField(max_length=100, blank=True, null = True)
    mota = models.CharField(max_length=100)
    lopmh = models.ForeignKey(LopMonhoc, on_delete=models.RESTRICT, blank=True, null = True)
    user = models.ForeignKey(User, on_delete=models.RESTRICT, blank=True, null = True)
    history = HistoricalRecords()
    def __str__(self):
        return self.file.name
    
class Giayto_hs81(models.Model):
    ten = models.CharField(max_length=100)
    format = models.CharField(choices=tl_choice, max_length=50, blank=True, null = True)
    soluong = models.IntegerField(default= 0)
    status = models.CharField(choices=st_choice, max_length=50, blank=True, null = True)
    hs81 = models.ForeignKey(Hs81, on_delete=models.RESTRICT)
    softfile = models.ForeignKey(UploadedFile, on_delete=models.RESTRICT, blank=True, null = True)
    history = HistoricalRecords()
    def __str__(self):
        return self.ten