#from asyncio.windows_events import NULL
from cProfile import label
from xml.etree.ElementTree import tostring
from django.db import models
from django.db.models import Sum
from django.utils import timezone
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

class XaPhuong(models.Model):
    ma = models.CharField(max_length=100)
    ten = models.CharField(max_length=100)
    tp = models.CharField(max_length=100)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Xã/Phường"
        verbose_name_plural = "Danh mục Xã/Phường"
        unique_together = ('ma','ten','tp')
        ordering = ["-id"]

    def __str__(self):
        return self.ten + ", " + self.tp

class Location(models.Model):
    chu = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    diachi = models.CharField(max_length=100,verbose_name = "Địa chỉ")
    xp = models.ForeignKey(XaPhuong, on_delete=models.RESTRICT, verbose_name = "Xã/Phường - Tỉnh/Thành phố")
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Vị trí"
        verbose_name_plural = "Vị trí"
        #unique_together = ('us','ten','tp')
        ordering = ["-id"]

    def __str__(self):
        return self.xp.ten + ", " + self.xp.tp

class House(models.Model):
    ln_choice = (
        ("Nguyên căn", "Nguyên căn"),
        ("Căn hộ", "Căn hộ"),
        ("Khác", "Khác"),
    )
    interval_choice = (
        ("1 tháng", "1 tháng"),
        ("3 tháng", "3 tháng"),
        ("6 tháng", "6 tháng"),
        ("12 tháng", "12 tháng"),
        ("Khác", "Khác"),
    )

    loc = models.ForeignKey(Location, on_delete=models.RESTRICT, null=True)
    ten = models.CharField(max_length=100, verbose_name = "Tên nhà trọ")
    loainha = models.CharField(choices=ln_choice, verbose_name = "Loại nhà")
    from django.core.validators import MinValueValidator, MaxValueValidator
    sophong= models.IntegerField(
        default=1,
        verbose_name = "Số phòng"
    )
    dientich = models.IntegerField(
        verbose_name = "Diện tích"
    )
    permonth = models.IntegerField(verbose_name = "Tiền thuê/tháng (VNĐ)")
    interval = models.CharField(choices=interval_choice, max_length=100, verbose_name = "Số tháng/kỳ thanh toán")
    deposit = models.IntegerField(verbose_name = "Tiền đặt cọc (VNĐ)")
    kitchen = models.BooleanField(default= True, verbose_name = "Bếp")
    wc = models.BooleanField(default= True, verbose_name = "Nhà vệ sinh")
    aircondition = models.BooleanField(default= True, verbose_name = "Điều hòa")
    wifi = models.BooleanField(default= True, verbose_name = "Wifi")
    washingmachine = models.BooleanField(default= True, verbose_name = "Máy giặt")
    ghichu = models.TextField(max_length=500, blank=True, null=True, verbose_name = "Ghi chú"   )

    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Nhà trọ"
        verbose_name_plural = "Danh mục Nhà trọ"
        #unique_together = ('us','ten','tp')
        ordering = ["-id"]

    def __str__(self):
        return self.ten

class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.RESTRICT, null=True)
    chu_id = models.BigIntegerField(null=True)
    ma = models.CharField(null=True, verbose_name = "Mã")
    hoten = models.CharField(max_length=100, verbose_name = "Họ tên")
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Email")
    #namsinh = models.DateField()
    sdt = models.CharField(max_length=100, verbose_name = "Số điện thoại",blank=True, null=True)
    cccd = models.CharField(max_length=100, verbose_name = "CCCD", blank=True, null=True)
    ngaycap = models.DateField(blank=True, null=True, verbose_name = "Ngày cấp")
    noicap = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Nơi cấp")
    mst = models.CharField(max_length=100, blank=True, null=True, verbose_name = "MS Thuế cá nhân")
    ghichu = models.TextField(max_length=500, blank=True, null=True, verbose_name = "Ghi chú")
    init_pwd = models.CharField(max_length=100, blank=True, null=True, verbose_name="Mật khẩu khởi tạo") 
    #phong = models.ForeignKey(Phong, on_delete=models.RESTRICT, null=True, blank=True)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Người thuê"
        verbose_name_plural = "Danh sách Người thuê"
        ordering = ["ma",]
        unique_together = ('hoten','chu_id',)

    def __str__(self):
        # Gracefully handle possible None values to avoid TypeError
        hoten = self.hoten or ""  # hoten is required but defensive fallback
        cccd = self.cccd or ""    # cccd may be null
        if cccd:
            return f"{hoten} - {cccd}"
        return hoten

class Landlord(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    ma = models.CharField(null=True, verbose_name = "Mã")
    hoten = models.CharField(max_length=100, verbose_name = "Họ tên")
    email = models.CharField(max_length=100, blank=True, null=True, verbose_name = "Email")
    #namsinh = models.DateField()
    sdt = models.CharField(max_length=100, verbose_name = "Số điện thoại",blank=True, null=True)
    cccd = models.CharField(max_length=100, verbose_name = "CCCD", blank=True, null=True)
    ngaycap = models.DateField(blank=True, null=True, verbose_name = "Ngày cấp")
    noicap = models.DateField(blank=True, null=True, verbose_name = "Ngày cấp")
    mst = models.CharField(max_length=100, blank=True, null=True, verbose_name = "MS Thuế cá nhân")
    ghichu = models.TextField(max_length=500, blank=True, null=True, verbose_name = "Ghi chú")
    #phong = models.ForeignKey(Phong, on_delete=models.RESTRICT, null=True, blank=True)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Chủ nhà"
        verbose_name_plural = "Danh sách Chủ nhà"
        ordering = ["id",]
        unique_together = ('email',)

    def __str__(self):
        return ma

class Hoadon(models.Model):
    st_choice = (
        ('ChuaTT', 'Chưa thanh toán'),
        ('DangTT', 'Đang thanh toán (Công nợ)'), 
        ('DaTT', 'Đã thanh toán'),
        ('QuaHan', 'Quá hạn'),
    )
    house = models.ForeignKey(House, on_delete=models.RESTRICT, null=True)
    renter = models.ForeignKey(Renter, on_delete=models.RESTRICT, blank=True, null=True)
    ten = models.CharField(max_length=100, verbose_name = "Mô tả hóa đơn")
   
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo hóa đơn")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật hóa đơn")
    duedate = models.DateField(verbose_name = "Ngày đến hạn")
    tienthuenha = models.IntegerField(blank=True, null=True, verbose_name = "Tiền thuê/tháng (VNĐ)")
    tiendien = models.IntegerField(blank=True, null=True, verbose_name = "Tiền điện (VNĐ)")
    tiennuoc = models.IntegerField(blank=True, null=True, verbose_name = "Tiền nước (VNĐ)")
    tienkhac = models.IntegerField(blank=True, null=True, verbose_name = "Tiền khác (VNĐ)")

    TONG_CONG = models.IntegerField(blank=True, null=True,  verbose_name="TỔNG CỘNG PHẢI THU")
    SO_TIEN_DA_TRA = models.IntegerField(blank=True, null=True, default=0, verbose_name="Số tiền đã trả")
    CONG_NO = models.IntegerField(blank=True, null=True, default=0, verbose_name="Công nợ")
    status = models.CharField(max_length=10, choices=st_choice, default='ChuaTT', verbose_name="Trạng thái")
    ghichu = models.TextField(max_length=500, blank=True, null=True, verbose_name = "Ghi chú")
    qr_code_image = models.ImageField(upload_to='bill_qr_codes/', blank=True, null=True, verbose_name="QR Code thanh toán")

    history = HistoricalRecords()
 
# ----------------------------------------------------
    # IV. LOGIC TỰ ĐỘNG CẬP NHẬT
    # ----------------------------------------------------
    def is_overdue(self):
        # Kiểm tra quá hạn: Công nợ > 0 và đã qua ngày hết hạn
        return self.CONG_NO > 0 and self.duedate < timezone.now().date()
        
    def save(self, *args, **kwargs):
        from decimal import Decimal
        
        # 1. TÍNH TOÁN LẠI TỔNG CỘNG VÀ CÔNG NỢ (Đảm bảo giá trị là Decimal và không phải None)
        t_nha = int(self.tienthuenha or 0)
        t_dien = int(self.tiendien or 0)
        t_nuoc = int(self.tiennuoc or 0)
        t_khac = int(self.tienkhac or 0)

        self.TONG_CONG = t_nha + t_dien + t_nuoc + t_khac

        self.SO_TIEN_DA_TRA = int(self.SO_TIEN_DA_TRA or 0) # Đảm bảo giá trị an toàn
        self.CONG_NO = self.TONG_CONG - self.SO_TIEN_DA_TRA
        
        # 2. CẬP NHẬT TRẠNG THÁI (Đã sửa logic)
        
        if self.CONG_NO <= 0:
            # ƯU TIÊN 1: Nếu Công nợ bằng 0 hoặc âm (trả thừa), coi là Đã Thanh toán
            self.status = 'DaTT'
        elif self.is_overdue():
            # ƯU TIÊN 2: Nếu chưa trả đủ và đã Quá hạn (is_overdue() phải được định nghĩa)
            self.status = 'QuaHan'
        elif self.SO_TIEN_DA_TRA > 0:
            # ƯU TIÊN 3: Nếu đã trả một phần (nhưng chưa hết và chưa quá hạn)
            self.status = 'DangTT'
        else:
            # CÒN LẠI: Chưa trả đồng nào (Công nợ > 0 và SO_TIEN_DA_TRA = 0)
            self.status = 'ChuaTT'

        super().save(*args, **kwargs)

        class Meta:
            verbose_name = "Hóa đơn"
            verbose_name_plural = "Danh mục Hóa đơn"
            #unique_together = ('us','ten','tp')
            ordering = ["-id"]

        def __str__(self):
            return self.ten

class Thanhtoan(models.Model):
    TT_CHOICES = (
        ('Choxn', 'Chờ xác nhận'),
        ('Daxn', 'Đã xác nhận'),
        ('Huy', 'Đã hủy'),
    )
    # Bổ sung: Người tạo thanh toán
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Người tạo")
    hoadon = models.ForeignKey(Hoadon, on_delete=models.RESTRICT, null=True)
    ten = models.CharField(max_length=100, verbose_name = "Mô tả thanh toán")
    ngay_tao = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo thanh toán")
    ngay_cap_nhat = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật thanh toán")
    tientt = models.IntegerField(blank=True, null=True, verbose_name = "Số tiền (VNĐ)")
    ghichu = models.TextField(max_length=500, blank=True, null=True, verbose_name = "Ghi chú"   )
    status = models.CharField(max_length=10, choices=TT_CHOICES, default='Choxn', verbose_name="Trạng thái TT")
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Thanh toán"
        verbose_name_plural = "Danh mục Thanh toán"
        #unique_together = ('us','ten','tp')
        ordering = ["-id"]

# CHỈNH SỬA LOGIC SAVE (Thay thế logic save() hiện tại)
    def save(self, *args, **kwargs):
        from decimal import Decimal
        
        # 1. Lưu bản ghi ThanhToan hiện tại
        super().save(*args, **kwargs)
        
        # 2. CHỈ CẬP NHẬT HÓA ĐƠN GỐC KHI TRẠNG THÁI LÀ 'Daxn'
        if self.status == 'Daxn':
            if self.hoadon:
                hoa_don_goc = self.hoadon
                
                # Tính tổng số tiền đã thanh toán đã được xác nhận
                tong_da_tra = Thanhtoan.objects.filter(hoadon=hoa_don_goc, status='Daxn').aggregate(Sum('tientt'))['tientt__sum'] or int(0)

                # Cập nhật SO_TIEN_DA_TRA và kích hoạt Hoadon.save()
                hoa_don_goc.SO_TIEN_DA_TRA = tong_da_tra
                hoa_don_goc.save() 
        
    # LOGIC DELETE (Đảm bảo cập nhật khi xóa bản ghi ĐÃ XÁC NHẬN)
    def delete(self, *args, **kwargs):
        if self.hoadon and self.status == 'Daxn':
            hoa_don_goc = self.hoadon
            super().delete(*args, **kwargs) # Xóa trước
            
            # Tính lại tổng chỉ các mục đã xác nhận
            tong_da_tra = Thanhtoan.objects.filter(hoadon=hoa_don_goc, status='Daxn').aggregate(Sum('tientt'))['tientt__sum'] or int(0)
            
            hoa_don_goc.SO_TIEN_DA_TRA = tong_da_tra
            hoa_don_goc.save()
        else:
            super().delete(*args, **kwargs)
    def __str__(self):
        return self.ten

"""NOTE:
Legacy duplicate definitions of Notification and IssueReport removed.
The authoritative versions are defined later in this file (see near bottom
around the Issue tracking section) and match current migrations:
 - sms.migrations.0021_notification_issuereport
Keeping a single source of truth avoids RuntimeWarning: model already registered
and prevents related_name clashes with third-party apps (e.g. django-notifications-hq).
"""

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
    
    
class HouseRenter(models.Model):

    house = models.ForeignKey(House, on_delete=models.RESTRICT, null=True)
    renter = models.ForeignKey(Renter, on_delete=models.RESTRICT, null=True, verbose_name = "Người thuê")
    rent_from = models.DateField(blank=True, null=True, verbose_name = "Thuê từ ngày")
    rent_to = models.DateField(blank=True, null=True, verbose_name = "Thuê đến ngày")
    active = models.BooleanField(default= False, verbose_name = "Người thuê đang ở?")
    ghichu = models.TextField(max_length=200, blank=True, null=True, verbose_name = "Ghi chú")
    #phong = models.ForeignKey(Phong, on_delete=models.RESTRICT, null=True, blank=True)
    history = HistoricalRecords()
 
    class Meta:
        verbose_name = "Người thuê - Nhà trọ"
        verbose_name_plural = "Người thuê - Nhà trọ"
        ordering = ["-id",]
    def __str__(self):
        return self.renter.hoten + " - " + self.house.loc.diachi

# Ensure only one active contract per house at the model layer
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=HouseRenter)
def ensure_single_active_contract(sender, instance: HouseRenter, created, **kwargs):
    """When a contract is saved as active, deactivate all other active contracts of the same house.
    Works on both create and update flows.
    """
    if instance.active and instance.house_id:
        # Deactivate any other active contracts for this house
        HouseRenter.objects.filter(house_id=instance.house_id, active=True).exclude(id=instance.id).update(active=False)

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
    mhdk = models.BooleanField(default= False, verbose_name="Môn học điều kiện")
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
    
class Hoclai(models.Model):
    lmh = models.ForeignKey(LopMonhoc, on_delete=models.RESTRICT)
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT)
    class Meta:
        verbose_name = "Thi lại"
        verbose_name_plural = "Danh sác Thi lại"
        unique_together = ('sv','lmh',)
        ordering = ["-id"]
    def __str__(self):
        return self.sv.hoten + "-" + self.lmh.monhoc.ten

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
    sotien1 = models.TextField(default= "", max_length=11,blank= True, null=True)
    sotien2 = models.TextField(default= "", max_length=11,blank= True, null=True)
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
    diem = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm")
    status = models.IntegerField(default= 0)
    att = models.IntegerField(default= 1)
    tp = models.ForeignKey(Loaidiem, on_delete=models.RESTRICT, verbose_name="Điểm Thành phần")
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT, verbose_name="Học viên")
    monhoc = models.ForeignKey(Monhoc, on_delete=models.RESTRICT, verbose_name="Môn học")    
    lmh = models.ForeignKey(LopMonhoc, on_delete=models.RESTRICT, default= None,blank= True, null=True, verbose_name="Lớp Môn học")    
    log = models.ForeignKey(LogDiem, on_delete=models.RESTRICT, null= True, verbose_name="ID Log")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Điểm thành phần"
        verbose_name_plural = "Kết quả điểm thành phần"
        ordering = ["sv","monhoc","tp"]

    def __str__(self):
        return str(self.diem)


class DiemTk(models.Model):
    #ghichu = models.CharField(max_length=300)
    sv_id = models.IntegerField(default= 0, verbose_name="Mã học viên")
    ma = models.CharField(default= "", max_length=100, verbose_name="Mã học viên")
    ten = models.CharField(default= "", max_length=100, verbose_name="Họ tên học viên")
    hk_id = models.IntegerField(default= 1, verbose_name="Mã lớp môn học")
    lmh_id = models.IntegerField(default= 0, verbose_name="Mã lớp môn học")
    mhdk = models.BooleanField(default= False)
    monhoc_id = models.IntegerField(default= 0, verbose_name="Mã môn học")
    monhoc = models.CharField(default= "", max_length=100, verbose_name="Tên môn học")
    status = models.BooleanField(default= True)
    thilai = models.BooleanField(default= False)
    tc = models.IntegerField(default= 0, verbose_name="Số tín chỉ")
    tbm = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm trung bình môn")
    tbmc = models.CharField(default= "", max_length=5)
    tbm4 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm trung bình môn 4")
    tbmkt = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm trung bình môn kỳ thi")
    kttx1 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTTX 1")
    n_kttx1 = models.BooleanField(default= False)
    kttx2 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTTX 2")
    n_kttx2 = models.BooleanField(default= False)
    kttx3 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTTX 3")
    n_kttx3 = models.BooleanField(default= False)
    ktdk1 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTDK 1")
    n_ktdk1 = models.BooleanField(default= False)
    ktdk2 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTDK 2")
    n_ktdk2 = models.BooleanField(default= False)
    ktdk3 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTDK 3")
    n_ktdk3 = models.BooleanField(default= False)
    ktkt1 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTKT 1")
    n_ktkt1 = models.BooleanField(default= False)
    ktkt2 = models.DecimalField(default= 0, max_digits=5, decimal_places=1, verbose_name="Điểm KTKT 2")
    n_ktkt2 = models.BooleanField(default= False)
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Điểm tổng kết môn học"
        verbose_name_plural = "Điểm tổng kết môn học"
        ordering = ["id",]
        unique_together = ('sv_id','lmh_id',)

    def __str__(self):
        return str(self.ten)

class SvTn(models.Model):
    #ghichu = models.CharField(max_length=300)
    xltn_choice = (
        ("Xuất sắc", "Xuất sắc"),
        ("Giỏi", "Giỏi"),
        ("Khá", "Khá"),
        ("Trung bình", "Trung bình"),
        ("Yếu", "Yếu"),
    )
    sv = models.ForeignKey(Hssv, on_delete=models.RESTRICT,blank= True, null=True)
    status = models.CharField(choices=yn_choice, max_length=50, blank=True, null = True, verbose_name="Đủ điều kiện tốt nghiệp?")
    xltn = models.CharField(choices=xltn_choice, max_length=50, blank=True, null = True, verbose_name="Xếp loại tốt nghiệp")
    tctl = models.BooleanField(default= False, verbose_name="Tích lũy đủ số mô-đun, tín chỉ")
    tbctl = models.BooleanField(default= False, verbose_name="Điểm TBC TL đạt từ 2,0 trở lên")
    ycbb = models.BooleanField(default= False, verbose_name="Hoàn thành các yêu cầu bắt buộc khác")
    ghichu = models.TextField(default= "", max_length=500,blank= True, null=True, verbose_name="Ghi chú")
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Sinh viên tốt nghiệp"
        verbose_name_plural = "Sinh viên tốt nghiệp"
        ordering = ["id",]
        unique_together = ('sv',)

    def __str__(self):
        return str(self.sv.hoten)

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
    sotien1 = models.TextField(default= "", max_length=11,blank= True, null=True)
    sotien2 = models.TextField(default= "", max_length=11,blank= True, null=True)
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
    loc = models.ForeignKey(Location, on_delete=models.RESTRICT, blank=True, null = True)
    house = models.ForeignKey(House, on_delete=models.RESTRICT, blank=True, null = True)
    
    type = models.IntegerField(default= 1)
    link_id = models.BigIntegerField(default= 0)

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


class Notification(models.Model):
    TYPE_CHOICES = [
        ('bill_created', 'Bill Created'),
        ('payment_submitted', 'Payment Submitted'),
        ('issue_reported', 'Issue Reported'),
        ('issue_resolved', 'Issue Resolved'),
        ('bill_commented', 'Bill Commented'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sms_notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    target_url = models.CharField(max_length=500, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class IssueReport(models.Model):
    STATUS_CHOICES = [
        ('new', 'Mới'),
        ('in_progress', 'Đang xử lý'),
        ('pending_confirmation', 'Chờ xác nhận'),
        ('resolved', 'Đã xử lý'),
        ('rejected', 'Chưa xong'),
    ]
    
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='issues')
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='reported_issues')
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.house.ten} - {self.title}"


class IssueImage(models.Model):
    """Images attached to issue reports"""
    issue = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='issues/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    caption = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return f"Image for {self.issue.title}"


class IssueComment(models.Model):
    """Comments and replies on issues"""
    issue = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.issue.title}"


class IssueStatusHistory(models.Model):
    """Track status changes for issues"""
    issue = models.ForeignKey(IssueReport, on_delete=models.CASCADE, related_name='status_history')
    old_status = models.CharField(max_length=20, choices=IssueReport.STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=IssueReport.STATUS_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'Issue status histories'
    
    def __str__(self):
        return f"{self.issue.title}: {self.old_status} → {self.new_status}"


# ==========================
# Bill Comments
# ==========================
class BillComment(models.Model):
    """Comments and replies on bills (Hoadon)"""
    bill = models.ForeignKey(Hoadon, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Bill #{self.bill_id} - {self.user.username}: {self.comment[:30]}"