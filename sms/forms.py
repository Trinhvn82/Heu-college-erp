from tkinter.ttk import LabeledScale
from django import forms
from .models import Ctdt, Diemdanh, Diemthanhphan, Hocphi, Hsgv, Lichhoc, Lop, TeacherInfo, CtdtMonhoc, Hssv, LopMonhoc
from .models import LopHk, Monhoc, Hp81

class CreateTeacher(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = "__all__"

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'teacher_img': forms.FileInput(attrs={'class': 'form-control'}),
            'passing_year': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Passing Year'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Joining Date'}),
            'admission_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Admission ID'}),
            'dept_type': forms.Select(attrs={'class': 'form-control'}),
            'sub_type': forms.Select(attrs={'class': 'form-control'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary'}),
        }

        
class CreateLichhoc(forms.ModelForm):
    class Meta:
        model = Lichhoc
        #fields = "__all__"
        fields = ('lop','thoigian','diadiem','monhoc',
                       'giaovien','sotiet','status','ghichu')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'trungtam': 'Trung tâm',
            'diadiem': 'Địa điểm',
            'thoigian': 'Thời gian',
            'sotiet': 'Số tiết',
            'lop': 'Lop',
            'status': 'Trang thai',
            'monhoc': 'Mon hoc',
            'giaovien': 'Giáo viên',
            'ghichu': 'Ghi chú',
        }
        widgets = {
            'trungtam': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Trung tam'}),
            'diadiem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dia diem'}),
            #'thoigian': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'thoigian': forms.DateInput(attrs={'class': 'form-control', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            #'thoigian': forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': 'datetimepicker','type': 'date' }),
            'sotiet': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'So tiet', 'max': 5, 'min': 1}),
            'lop': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Lop'}),
            'monhoc': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'giaovien': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Giao vien'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chu'}),
        }
class CreateCtdtMonhoc(forms.ModelForm):
    class Meta:
        model = CtdtMonhoc
        #fields = "__all__"
        fields = ('ctdt','hocky','monhoc')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'ctdt': 'Chuong trinh DT',
            'hocky': 'Hoc ky',
            'monhoc': 'Mon hoc',
        }
        widgets = {
            'hocky': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-4', 'max':4, 'min':1}),
            'monhoc': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'ctdt': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Giao vien'}),
       }

class CreateLopHk(forms.ModelForm):
    class Meta:
        model = LopHk
        #fields = "__all__"
        fields = ('lop','hk','start_hk', 'end_hk')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'start_hk': 'Thời gian bắt đầu',
            'end_hk': 'Thời gian kết thúc',
        }
        widgets = {
            'start_hk': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_hk': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
       }

class CreateLopMonhoc(forms.ModelForm):
    class Meta:
        model = LopMonhoc
        #fields = "__all__"
        fields = ('lop','monhoc', 'ngaystart', 'ngayend', 'status', 'hsdt')
        labels = {
            'monhoc': 'Mon hoc',
            'ngaystart': 'Ngay bat dau',
            'ngayend': 'Ngay ket thuc',
            'status': 'Trang thai',
            'hsdt': 'Ho so dao tao'
        }
        widgets = {
            'lop': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'monhoc': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ngaystart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ngayend': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hsdt': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chu'}),
       }
        
class CreateDiemdanh(forms.ModelForm):
    class Meta:
        model = Diemdanh
        #fields = "__all__"
        fields = ('lichhoc','sv')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'lichhoc': 'Lich hoc',
            'sv': 'Sinh vien'
        }
        widgets = {
            'lichhoc': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'sv': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Giao vien'}),
        }

class CreateCtdt(forms.ModelForm):
    class Meta:
        model = Ctdt
        #fields = "__all__"
        fields = ('ten','khoa', 'khoahoc')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'ten': 'Ten CTDT',
            'khoa': 'Khoa',
            'khoahoc': 'Khoa hoc'
        }
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'form-control'}),
            'khoa': forms.TextInput(attrs={'class': 'form-control'}),
            'khoahoc': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CreateLop(forms.ModelForm):
    # mhs = forms.ModelMultipleChoiceField(
    #     queryset=Monhoc.objects.all(),
    #     widget=forms.SelectMultiple,
    # )
    class Meta:
        model = Lop
        fields = "__all__"
        #fields = ('ten','khoa', 'khoahoc')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'ma': 'Mã lớp',
            'ten': 'Tên lớp',
            'trungtam': 'Trung tâm',
            'ctdt': 'Chương trình đào tạo'
            #'mhs': 'Môn học của lớp'
        }
        widgets = {
            'ma': forms.TextInput(attrs={'class': 'form-control'}),
            'ten': forms.TextInput(attrs={'class': 'form-control'}),
            #'trungtam': forms.TextInput(attrs={'class': 'form-control'}),
            'trungtam': forms.Select(attrs={'class': 'form-control'}),
            'ctdt': forms.Select(attrs={'class': 'form-control'}),
        }

class CreateHp81(forms.ModelForm):
    # mhs = forms.ModelMultipleChoiceField(
    #     queryset=Monhoc.objects.all(),
    #     widget=forms.SelectMultiple,
    # )
    class Meta:
        model = Hp81
        #fields = "__all__"
        fields = ('hk','hs81_st','status', 'thoigian', 'sotien1', 'sotien2', 'ghichu', 'sv')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'hk': 'Học kỳ',
            'hs81_st': 'Tình trạng hồ sơ',
            'status': 'Tình trạng học phí',
            'thoigian': 'Tgian giải ngân dự kiến',
            'sotien1': 'Số tiền giải ngân dự kiến',
            'sotien2': 'Số tiền thực nhận từ học viên',
            'ghichu': 'Ghi chú',
            #'mhs': 'Môn học của lớp'
        }
        widgets = {
            'hs81_st': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'thoigian': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sotien1': forms.NumberInput(attrs={'class': 'form-control'}),
            'sotien2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control'}),
            'hk': forms.Select(attrs={'class': 'form-control'}),
            'sv': forms.Select(attrs={'class': 'form-control'}),
        }

class CreateSv(forms.ModelForm):
    class Meta:
        model = Hssv
        #fields = "__all__"
        fields = ('msv','hoten','image','malop', 'namsinh','gioitinh', 'dantoc','noisinh', 'quequan','diachi', 'cccd','hotenbo', 'hotenme','sdths', 'sdtph', 'status', 'ghichu')
        #,'diachi', 'cccd','hotenbo', 'hotenme','sdths', 'sdtph')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'msv': 'Mã học viên',
            'hoten': 'Họ tên',
            'image': 'Ảnh',
            'malop': 'Tên lớp',
            'namsinh': 'Năm sinh',
            'gioitinh': 'Gioi tính',
            'dantoc': 'Dân tộc',
            'noisinh': 'Nơi sinh',
            'quequan': 'Quê quán',
            'diachi': 'Địa chỉ thương trú',
            'cccd': 'CCCD',
            'hotenbo': 'Họ tên bố',
            'hotenme': 'Họ tên mẹ',
            'sdths': 'SĐT học sinh',
            'sdtph': 'SĐT phụ huynh',
            'status': 'Trạng thái',
            'ghichu': 'Ghi chú'
        }
        widgets = {
            'msv': forms.TextInput(attrs={'class': 'form-control'}),
            'hoten': forms.TextInput(attrs={'class': 'form-control'}),
            'malop': forms.Select(attrs={'class': 'form-control'}),
            'namsinh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'gioitinh': forms.TextInput(attrs={'class': 'form-control'}),
            'dantoc': forms.TextInput(attrs={'class': 'form-control'}),
            'noisinh': forms.TextInput(attrs={'class': 'form-control'}),
            'quequan': forms.TextInput(attrs={'class': 'form-control'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control'}),
            'hotenbo': forms.TextInput(attrs={'class': 'form-control'}),
            'hotenme': forms.TextInput(attrs={'class': 'form-control'}),
            'sdths': forms.TextInput(attrs={'class': 'form-control'}),
            'sdtph': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chu'}),
        }

class CreateGv(forms.ModelForm):
    class Meta:
        model = Hsgv
        #fields = "__all__"
        fields = ('ma', 'hoten','email','diachi', 'quequan','sdt', 'gioitinh','cccd', 'thoihanhd', 'hsgv')
        
        #,'diachi', 'cccd','hotenbo', 'hotenme','sdths', 'sdtph')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'ma': 'Mã',
            'email': 'Email',
            'hoten': 'Họ tên',
            'diachi': 'Đại chỉ',
            'quequan': 'Quê quán',
            'sdt': 'SDT',
            'gioitinh': 'Giới tính',
            'cccd': 'CCCD',
            'thoihanhd': 'Thời hạn hợp đồng',
            'hsgv': 'Thông tin hồ sơ giáo viên'
        }
        widgets = {
            'ma': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'hoten': forms.TextInput(attrs={'class': 'form-control'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control'}),
            'quequan': forms.TextInput(attrs={'class': 'form-control'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control'}),
            'gioitinh': forms.TextInput(attrs={'class': 'form-control'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control'}),
            'thoihanhd': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'hsgv': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CreateHocphi(forms.ModelForm):
    class Meta:
        model = Hocphi
        fields = "__all__"
#        fields = ('lichhoc','sv', 'ghichu')

class CreateDiem(forms.ModelForm):
    class Meta:
        model = Diemthanhphan
        fields = ('sv', 'monhoc', 'tp', 'diem')
        labels = {
            'diem': 'Diem',
            'tp': 'Diem thanh phan',
            'monhoc': 'Mon hoc',
            'sv': 'Ten sinh vien'
        }
        widgets = {
            'diem': forms.NumberInput(attrs={'class': 'form-control'}),
            'tp': forms.Select(attrs={'class': 'form-control'}),
            'monhoc': forms.Select(attrs={'class': 'form-control'}),
            'sv': forms.Select(attrs={'class': 'form-control'}),
        }

