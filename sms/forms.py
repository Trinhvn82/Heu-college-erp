from tkinter.ttk import LabeledScale
from django import forms
from .models import Ctdt, Diemdanh, Diemthanhphan, Hocphi, Hsgv, Lichhoc, Lop, TeacherInfo, CtdtMonhoc, Hssv, LopMonhoc
from .models import LopHk, Monhoc, Hp81, Hs81, Ttgv, UploadedFile, Hsns

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
class CreateNs(forms.ModelForm):
    class Meta:
        model = Hsns
        #fields = "__all__"
        fields = ('ma', 'hoten','email','diachi', 'quequan','sdt', 'gioitinh','cccd')
        
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
            'cccd': 'CCCD'
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
        }

class CreateCtdtMonhoc(forms.ModelForm):
    class Meta:
        model = CtdtMonhoc
        #fields = "__all__"
        fields = ('ctdt','monhoc')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'ctdt': 'Chuong trinh DT',
            'monhoc': 'Mon hoc',
        }
        widgets = {
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

class CreateUploadFile(forms.ModelForm):
    class Meta:
        model = UploadedFile
        #fields = "__all__"
        fields = ('file','mota')
        labels = {
            'file': 'Chọn file',
            'mota': 'Mô tả',
        }
        widgets = {
            'mota': forms.TextInput(attrs={'class': 'form-control'}),
       }

class CreateLopMonhoc(forms.ModelForm):
    class Meta:
        model = LopMonhoc
        #fields = "__all__"
        fields = ('lop','hk','monhoc', 'ngaystart', 'ngayend', 'status', 'hsdt1', 'hsdt2', 'hsdt3', 'hsdt4')
        labels = {
            'hk': 'Học kỳ',
            'monhoc': 'Môn học',
            'ngaystart': 'Ngày bắt đầu',
            'ngayend': 'Ngày kết thúc',
            'status': 'Trạng thái',
            'hsdt1': 'Tên hồ sơ đào tạo 1',
            'hsdt2': 'Tên hồ sơ đào tạo 2',
            'hsdt3': 'Tên hồ sơ đào tạo 3',
            'hsdt4': 'Tên hồ sơ đào tạo 4',
        }
        widgets = {
            'lop': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'hk': forms.Select(attrs={'class': 'form-control'}),
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

class CreateTtgv(forms.ModelForm):
    class Meta:
        model = Ttgv
        #fields = "__all__"
        fields = ('sotien1','sotien2','ghichu', 'gv', 'lopmh')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'sotien1': 'Số tiền cần thanh toán',
            'sotien2': 'Số tiền đã thanh toán',
            'ghichu': 'Ghi chú',
        }
        widgets = {
            'sotien1': forms.NumberInput(attrs={'class': 'form-control'}),
            'sotien2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control'}),
        }
0
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
        fields = ('hk','status', 'thoigian', 'sotien1', 'sotien2', 'ghichu', 'sv')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'hk': 'Học kỳ',
            'thoigian': 'Ngày thu',
            'status': 'Tình trạng học phí',
            'sotien1': 'Số tiền giải ngân dự kiến',
            'sotien2': 'Số tiền thực nhận từ học viên',
            'ghichu': 'Ghi chú',
            #'mhs': 'Môn học của lớp'
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'thoigian': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'sotien1': forms.NumberInput(attrs={'class': 'form-control'}),
            'sotien2': forms.NumberInput(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control'}),
            'hk': forms.Select(attrs={'class': 'form-control'}),
            'sv': forms.Select(attrs={'class': 'form-control'}),
        }

class CreateHs81(forms.ModelForm):
    # mhs = forms.ModelMultipleChoiceField(
    #     queryset=Monhoc.objects.all(),
    #     widget=forms.SelectMultiple,
    # )
    class Meta:
        model = Hs81
        #fields = "__all__"
        fields = ('hk','status', 'thoigian', 'ddn', 'cntn','btn', 'xnct','cccd', 'cccdbo','cccdme', 'gks', 'ghichu','sv')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'hk': 'Học kỳ',
            'status': 'Tình trạng',
            'thoigian': 'Tgian giải ngân dự kiến',
            'ddn': 'Đơn đề nghị',
            'cntn': 'Chứng nhận tốt nghiệp',
            'btn': 'Bằng tốt nghiệp',
            'xnct': 'Xác nhận cư trú',
            'cccd': 'CCCD',
            'cccdbo': 'CCCD Bố',
            'cccdme': 'CCCD Mẹ',
            'gks': 'Giấy khai sinh',
            'ghichu': 'Ghi chú',
            #'mhs': 'Môn học của lớp'
        }
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'thoigian': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control'}),
            'hk': forms.Select(attrs={'class': 'form-control'}),
            'sv': forms.Select(attrs={'class': 'form-control'}),
        }

class CreateSv(forms.ModelForm):
    class Meta:
        model = Hssv
        fields = "__all__"
        exclude = ['user',]
        #fields = ('msv','hoten','malop', 'namsinh','gioitinh', 'dantoc','noisinh', 'quequan','diachi','xa','huyen','tinh', 'cccd','hotenbo', 'hotenme','sdths', 'sdtph', 'status', 'ghichu')
        #,'diachi', 'cccd','hotenbo', 'hotenme','sdths', 'sdtph')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'msv': 'Mã học viên',
            'hoten': 'Họ tên',
            'lop': 'Tên lớp',
            'namsinh': 'Năm sinh',
            'gioitinh': 'Gioi tính',
            'dantoc': 'Dân tộc',
            'noisinh': 'Nơi sinh',
            'quequan': 'Quê quán',
            'diachi': 'Địa chỉ thường trú',
            'xa': 'Xã',
            'huyen': 'Huyện',
            'tinh': 'Tỉnh',
            'cccd': 'CCCD',
            'hotenbo': 'Họ tên bố',
            'hotenme': 'Họ tên mẹ',
            'sdths': 'SĐT học sinh',
            'sdtph': 'SĐT phụ huynh',
            'status': 'Trạng thái học viên',
            'hs_syll' : 'Sơ yếu lý lịch',
            'hs_pxt' : 'Phiếu xét tuyển',
            'hs_btn' : 'Bằng TN',
            'hs_gcntttt' : 'Giay CNTTTT',
            'hs_hbthcs' : 'Học bạ THCS',
            'hs_cccd' : 'CCCD',
            'hs_gks' : 'Giấy khai sinh',
            'hs_shk' : 'Sổ HK',
            'hs_a34' : 'Ảnh 3x4',
            'hs_status': 'Trạng thái hồ sơ',
            'ghichu': 'Ghi chú',
        }
        widgets = {
            'msv': forms.TextInput(attrs={'class': 'form-control'}),
            'hoten': forms.TextInput(attrs={'class': 'form-control'}),
            'lop' : forms.Select(attrs={'class': 'form-control'}),
            'namsinh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'gioitinh': forms.TextInput(attrs={'class': 'form-control'}),
            'dantoc': forms.TextInput(attrs={'class': 'form-control'}),
            'noisinh': forms.TextInput(attrs={'class': 'form-control'}),
            'quequan': forms.TextInput(attrs={'class': 'form-control'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control'}),
            'xa': forms.TextInput(attrs={'class': 'form-control'}),
            'huyen': forms.TextInput(attrs={'class': 'form-control'}),
            'tinh': forms.TextInput(attrs={'class': 'form-control'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control'}),
            'hotenbo': forms.TextInput(attrs={'class': 'form-control'}),
            'hotenme': forms.TextInput(attrs={'class': 'form-control'}),
            'sdths': forms.TextInput(attrs={'class': 'form-control'}),
            'sdtph': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'hs_status' : forms.Select(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chu'}),
        }

class CreateGv(forms.ModelForm):
    class Meta:
        model = Hsgv
        fields = "__all__"
        exclude = ['user',]
        labels = {
            'ma': 'Mã',
            'hoten': 'Họ tên',
            'namsinh': 'Năm sinh',
            'cccd': 'CCCD',
            'ngaycap': 'Ngày cáp',
            'noicap': 'Nơi cấp',
            'diachi': 'Địa chỉ',
            'sdt': 'SĐT',
            'email': 'Email',
            'mst': 'Mã số thuế',
            'bhxh': 'Mã số BHXH',
            'dongbhxh': 'Nơi đóng BHXH',
            'stk': 'STK',
            'nh': 'Ngân hàng',
            'cn': 'Chi nhánh',
            'trinhdo': 'Trình độ',
            'truongtn': 'Trường tốt nghiệp',
            'nganhtn': 'Ngành tốt nghiệp',
            'shdtg': 'Số HĐ Thỉnh giảng',
            'ngayky': 'Ngày ký',
            'ngayhh': 'Ngày hết hạn',
            'hs_btn' : 'Bằng Tốt nghiệp',
            'hs_bd' : 'Bảng điểm',
            'hs_cc' : 'Chứng chỉ NVSP/dạy nghề',
            'hs_syll' : 'Sơ yếu lý lịch',
            'hs_ccta' : 'Chứng chỉ tiếng Anh',
            'hs_ccth' : 'Chứng chỉ tin học',
            'hs_status' : 'Tình trạng hồ sơ',
            'ghichu' : 'Ghi chú',
        }
        widgets = {
            'ma': forms.TextInput(attrs={'class': 'form-control'}),
            'hoten': forms.TextInput(attrs={'class': 'form-control'}),
            'namsinh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control'}),
            'ngaycap': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'noicap': forms.TextInput(attrs={'class': 'form-control'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'mst': forms.TextInput(attrs={'class': 'form-control'}),
            'bhxh': forms.TextInput(attrs={'class': 'form-control'}),
            'dongbhxh': forms.TextInput(attrs={'class': 'form-control'}),
            'stk': forms.TextInput(attrs={'class': 'form-control'}),
            'nh': forms.TextInput(attrs={'class': 'form-control'}),
            'cn': forms.TextInput(attrs={'class': 'form-control'}),
            'trinhdo': forms.Select(attrs={'class': 'form-control'}),
            'truongtn': forms.TextInput(attrs={'class': 'form-control'}),
            'nganhtn': forms.TextInput(attrs={'class': 'form-control'}),
            'shdtg': forms.TextInput(attrs={'class': 'form-control'}),
            'ngayky': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'ngayhh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'hs_status': forms.Select(attrs={'class': 'form-control'}),
            'ghichu' : forms.Textarea(attrs={'class': 'form-control'}),
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

