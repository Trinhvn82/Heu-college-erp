from tkinter.ttk import LabeledScale
from django import forms
from .models import *
import decimal
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username_or_email and password:
            from django.contrib.auth import authenticate, get_user_model
            UserModel = get_user_model()
            # Try to get user by username
            user = authenticate(self.request, username=username_or_email, password=password)
            if not user:
                # Try to get user by email
                try:
                    user_obj = UserModel.objects.get(email=username_or_email)
                    user = authenticate(self.request, username=user_obj.username, password=password)
                except UserModel.DoesNotExist:
                    pass
            if user is None:
                raise ValidationError("Sai tên đăng nhập/email hoặc mật khẩu.")
            self.confirm_login_allowed(user)
            self.user_cache = user
        return self.cleaned_data

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
        fields = ('lmh','thoigian','diadiem',
                       'giaovien','sotiet','status','ghichu')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        labels = {
            'trungtam': 'Trung tâm',
            'diadiem': 'Địa điểm',
            'thoigian': 'Thời gian',
            'sotiet': 'Số tiết',
            #'lop': 'Lop',
            'status': 'Trang thai',
            #'monhoc': 'Mon hoc',
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
            'lmh': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Lop'}),
            'giaovien': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Giao vien'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chu'}),
        }
class CreateNs(forms.ModelForm):
    class Meta:
        model = Hsns
        fields = "__all__"
        exclude = ['user',]

        widgets = {
              'ma': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã nhân sự'}),    
              'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
              'hoten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ tên', 'maxlength': '50'}), 
            'gioitinh': forms.Select(attrs={'class': 'form-control'}),
            'namsinh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'dantoc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dân tộc'}),
            'tongiao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tôn giáo'}),
            'quoctich': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Quốc tịch'}),
            'quequan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nguyên quán'}),
            'diachi1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ tạm trú'}),  
            'diachi2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ thường trú'}),   
            'sdt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CCCD'}),
            'ngaycap': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'noicap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nơi cấp'}),
            'mst': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã số thuế'}),
            'tddt': forms.Select(attrs={'class': 'form-control'}),
            'noidt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nơi đào tạo'}),
            'kdt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Khoa đào tạo'}),
            'cndt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chuyên ngành'}),
            'namtn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Năm tốt nghiệp'}),
            'xldt': forms.Select(attrs={'class': 'form-control'}),
            'cdcv': forms.Select(attrs={'class': 'form-control'}),
            'vtcv': forms.Select(attrs={'class': 'form-control'}),
            'shd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số hợp đồng'}),
            'ngayky': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ngayhh': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'trangthaihd': forms.Select(attrs={'class': 'form-control'}),
            'tcld': forms.Select(attrs={'class': 'form-control'}),
            'loaihd': forms.Select(attrs={'class': 'form-control'}),
            'ngaylv': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tgcd': forms.Select(attrs={'class': 'form-control'}),
            'tgbhxh': forms.Select(attrs={'class': 'form-control'}),
            'ssbhxh': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số sổ BHXH'}),
            'tongluong': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tổng lương'}),
            'luongcb': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Lương cơ bản'}),
            'stk': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số tài khoản'}),
            'nh': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ngân hàng'}),
            'chinhanh': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chi nhánh'}),
            'hs_btn': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_bd': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_cc': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_syll': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_ccta': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_ccth': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_khac': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Giấy tờ khác'}),
            'hs_status': forms.Select(attrs={'class': 'form-control'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chú'}),

        }

class CreateRenter(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            from django.core.validators import validate_email
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError("Email không đúng định dạng. Vui lòng nhập lại.")
        return email
    class Meta:
        model = Renter
        fields = "__all__"
        exclude = ['user','chu_id','ma','init_pwd']

        widgets = {
            'hoten': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Họ tên', 'maxlength': '50'}), 
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'maxlength': '50'}),
            'sdt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Số điện thoại', 'maxlength': '50'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CCCD', 'maxlength': '50'}),
            'ngaycap': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'noicap': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nơi cấp', 'maxlength': '50'}),
            'mst': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mã số thuế', 'maxlength': '50'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chú', 'maxlength': '0'}),
        }

class CreateHouseRenter(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner', None)
        super().__init__(*args, **kwargs)
        if owner:
            self.fields['renter'].queryset = Renter.objects.filter(chu_id=owner.id)
    class Meta:
        model = HouseRenter
        fields = "__all__"
        exclude = ['house']
        widgets = {
            'renter': forms.Select(attrs={'class': 'form-control'}),
            'rent_from': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'rent_to': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'active' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ghi chú'}),
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
    def clean(self):
            cleaned_data = super().clean()
            start_date = cleaned_data.get('start_hk')
            end_date = cleaned_data.get('end_hk')
            if end_date and start_date and end_date < start_date:
                raise forms.ValidationError("End date must be greater than start date")

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
            #'file' : forms.FileField(validators=[file_size])
       }

class CreateLopMonhoc(forms.ModelForm):
    class Meta:
        model = LopMonhoc
        #fields = "__all__"
        fields = ('lop','hk','monhoc', 'ngaystart', 'ngayend', 'status', 'mhdk', 'hsdt1', 'hsdt2', 'hsdt3', 'hsdt4', 'hsdt5', 'hsdt6', 'hsdt7', 'hsdt')
        labels = {
            'hk': 'Học kỳ',
            'monhoc': 'Môn học',
            'ngaystart': 'Ngày bắt đầu',
            'ngayend': 'Ngày kết thúc',
            'status': 'Trạng thái',
        }
        widgets = {
            'lop': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Lớp'}),
            'hk': forms.Select(attrs={'class': 'form-control'}),
            'monhoc': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Mon hoc'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'ngaystart': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ngayend': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mhdk': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt1': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt2': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt3': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt4': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt5': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt6': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt7': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hsdt': forms.Textarea(attrs={'class': 'form-control'}),
       }
        
class CreateSvTn(forms.ModelForm):
    class Meta:
        model = SvTn
        #fields = "__all__"
        fields = ('status','xltn','tctl','tbctl','ycbb','ghichu')
        widgets = {
            'xltn': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'tctl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tbctl': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ycbb': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control'}),
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
            'ten': 'Tên CTDT',
            'khoa': 'Khoa',
            'khoahoc': 'Khóa học'
        }
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'form-control'}),
            'khoa': forms.TextInput(attrs={'class': 'form-control'}),
            'khoahoc': forms.NumberInput(attrs={'class': 'form-control'}),
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


class CreateLoc(forms.ModelForm):

    class Meta:
        model = Location
        fields = "__all__"
        exclude = ['chu',]
        #fields = ('user','diachi','xp')
        #fields_required = ('lop','trungtam','thoigian','monhoc')
        widgets = {
          #  'user': forms.Select(attrs={'class': 'form-control'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control'}),
            'xp': forms.Select(attrs={'class': 'form-control'}),
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
            'gioitinh': forms.Select(attrs={'class': 'form-control'}),
            'dantoc': forms.TextInput(attrs={'class': 'form-control'}),
            'noisinh': forms.TextInput(attrs={'class': 'form-control'}),
            'quequan': forms.TextInput(attrs={'class': 'form-control'}),
            'diachi': forms.TextInput(attrs={'class': 'form-control'}),
            'xa': forms.TextInput(attrs={'class': 'form-control'}),
            'huyen': forms.TextInput(attrs={'class': 'form-control'}),
            'tinh': forms.TextInput(attrs={'class': 'form-control'}),
            'cccd': forms.TextInput(attrs={'class': 'form-control'}),
            'ngaycap': forms.DateInput(attrs={'class': 'form-control', 'type': 'date','placeholder': 'mm/dd/yyyy'}),
            'noicap': forms.TextInput(attrs={'class': 'form-control'}),
            'stk': forms.TextInput(attrs={'class': 'form-control'}),
            'nh': forms.TextInput(attrs={'class': 'form-control'}),
            'hotenbo': forms.TextInput(attrs={'class': 'form-control'}),
            'hotenme': forms.TextInput(attrs={'class': 'form-control'}),
            'sdths': forms.TextInput(attrs={'class': 'form-control'}),
            'sdtph': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'hs_syll' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_pxt' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_btn' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_gcntttt' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_hbthcs' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_cccd' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_gks' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_shk' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_a34' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
            'hs_btn' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_bd' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_cc' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_syll' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_ccta' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_ccth' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hs_status': forms.Select(attrs={'class': 'form-control'}),
            'ghichu' : forms.Textarea(attrs={'class': 'form-control'}),
        }

class CreateHouse(forms.ModelForm):

    permonth = forms.CharField(
        label="Tiền thuê/tháng (VNĐ)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeydown': 'preventNonNumeric(event)',
            'oninput': 'formatThousands(this)' # <-- ĐÃ THÊM ONINPUT
        })
    )
    deposit = forms.CharField(
        label="Tiền đặt cọc (VNĐ)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeydown': 'preventNonNumeric(event)',
            'oninput': 'formatThousands(this)' # <-- ĐÃ THÊM ONINPUT
        })
    )    
    def clean(self):
        cleaned_data = super().clean()
        
        # Lấy giá trị chuỗi (có dấu chấm) từ Form
        raw_permonth = self.cleaned_data.get('permonth')
        raw_deposit = self.cleaned_data.get('deposit')
        
        # --- 2. LÀM SẠCH permonth ---
        if raw_permonth:
            cleaned_permonth = raw_permonth.replace(',', '')
            if not cleaned_permonth.isdigit():
                 self.add_error('permonth', "Vui lòng nhập số nguyên.")
            else:
                # Ghi đè giá trị đã làm sạch vào cleaned_data
                cleaned_data['permonth'] = int(cleaned_permonth)
        
        # --- 3. LÀM SẠCH deposit ---
        if raw_deposit:
            cleaned_deposit = raw_deposit.replace(',', '')
            if not cleaned_deposit.isdigit():
                 self.add_error('deposit', "Vui lòng nhập số nguyên.")
            else:
                # Ghi đè giá trị đã làm sạch vào cleaned_data
                cleaned_data['deposit'] = int(cleaned_deposit)
                
        # ... (các validation khác nếu có)
        return cleaned_data

    class Meta:
        model = House
        fields = "__all__"
        exclude = ['loc',]
        widgets = {
            'ten': forms.TextInput(attrs={'class': 'form-control', 'maxlength':'100'}),
            'loainha': forms.Select(attrs={'class': 'form-control'}),
            'sophong': forms.NumberInput(attrs={'class': 'form-control', 'max':100, 'min':1}),
            'dientich': forms.NumberInput(attrs={'class': 'form-control', 'max':10000, 'min':1}),

            'interval': forms.Select(attrs={'class': 'form-control'}),
            'kitchen' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wc' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aircondition' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wifi' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'washingmachine' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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


# ==========================================================
# FORM TẠO/CẬP NHẬT HÓA ĐƠN MỚI
# ==========================================================
class CreateHoaDonForm(forms.ModelForm):
    # Thêm field renter với queryset động
    renter = forms.ModelChoiceField(
        queryset=Renter.objects.none(),  # Sẽ được set trong __init__
        label="Khách thuê",
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Chọn khách thuê đang thuê nhà này (nếu có)"
    )
    
    # Định nghĩa lại các trường số cần format JS là CharField
    tienthuenha = forms.CharField(
        label="Tiền thuê nhà(VNĐ)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeydown': 'preventNonNumeric(event)',
            'oninput': 'formatThousands(this)' # <-- ĐÃ THÊM ONINPUT
        })
    )
    tiendien = forms.CharField(
        label="Tiền điện (VNĐ)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeydown': 'preventNonNumeric(event)',
            'oninput': 'formatThousands(this)' # <-- ĐÃ THÊM ONINPUT
        })
    )    

    tiennuoc = forms.CharField(
        label="Tiền nước (VNĐ)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeydown': 'preventNonNumeric(event)',
            'oninput': 'formatThousands(this)' # <-- ĐÃ THÊM ONINPUT
        })
    )    
    tienkhac = forms.CharField(
        label="Tiền khác (VNĐ)",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'onkeydown': 'preventNonNumeric(event)',
            'oninput': 'formatThousands(this)' # <-- ĐÃ THÊM ONINPUT
        })
    )    
    
    class Meta:
        model = Hoadon
        # Chỉ hiển thị các trường cần người dùng nhập hoặc chọn
        fields = "__all__"
        exclude = ['house','ngay_tao','status','ngay_cap_nhat', 'TONG_CONG','SO_TIEN_DA_TRA','CONG_NO']
        
        widgets = {
            'house': forms.Select(attrs={'class': 'form-control'}),
            'ten': forms.TextInput(attrs={'class': 'form-control'}),
            # HTML5 date input requires value format YYYY-MM-DD to display on edit
            # Use format='%Y-%m-%d' so existing dates render correctly in the input
            'duedate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'qr_code_image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        
    # Validation và làm sạch dữ liệu (loại bỏ dấu chấm)
    def clean(self):
        cleaned_data = super().clean()
        
        # Danh sách các trường cần làm sạch
        fields_to_clean = {
            'tienthuenha': 'Tiền thuê nhà(VNĐ)',
            'tiendien': 'Tiền điện (VNĐ)',
            'tiennuoc': 'Tiền nước (VNĐ)',
            'tienkhac': 'Tiền khác (VNĐ)',
        }
        
        for field_name, label in fields_to_clean.items():
            value_str = self.cleaned_data.get(field_name)
            
            if not value_str:
                # Nếu chuỗi rỗng, gán về Decimal(0) và tiếp tục vòng lặp
                cleaned_data[field_name] = int(0)
                continue # Chuyển sang trường tiếp theo
            # --- KẾT THÚC LOGIC KHẮC PHỤC ---

            # Nếu có giá trị (không phải chuỗi rỗng), tiến hành làm sạch dấu chấm
            cleaned_value = value_str.replace(',', '')
                
            # Kiểm tra phải là số
            if not cleaned_value.isdigit():
                    self.add_error(field_name, f"Vui lòng nhập số nguyên cho {label}.")
                    
            # Chuyển thành Decimal để khớp với Model và logic tính toán
            cleaned_data[field_name] = int(cleaned_value)
            
                
        return cleaned_data
    
    def clean_renter(self):
        """Validate renter: nếu chọn renter, phải có hợp đồng với house này"""
        renter = self.cleaned_data.get('renter')
        
        # Nếu không chọn renter thì OK (field là optional)
        if not renter:
            return renter
        
        # Nếu chọn renter, cần có house context để validate
        # House được lưu trong instance khi edit, hoặc cần check từ view
        # Vì form được init với house, ta cần lưu house vào form instance
        if hasattr(self, '_house'):
            house = self._house
            # Kiểm tra renter có hợp đồng với house này không
            has_contract = HouseRenter.objects.filter(house=house, renter=renter).exists()
            if not has_contract:
                raise forms.ValidationError(
                    f"Khách thuê '{renter.hoten}' không có hợp đồng nào với nhà '{house.ten}'. "
                    f"Vui lòng chọn khách thuê khác hoặc để trống."
                )
        
        return renter
    
    def __init__(self, *args, **kwargs):
        # Nhận house từ view để filter renter
        house = kwargs.pop('house', None)
        super().__init__(*args, **kwargs)
        
        # Lưu house vào form để dùng trong clean_renter
        self._house = house
        
        # Format các trường số tiền với dấu phẩy khi edit (instance có sẵn)
        if self.instance and self.instance.pk:
            # Danh sách các trường cần format
            money_fields = ['tienthuenha', 'tiendien', 'tiennuoc', 'tienkhac']
            
            for field_name in money_fields:
                # Lấy giá trị từ instance
                value = getattr(self.instance, field_name, None)
                if value is not None and value != 0:
                    # Format với dấu phẩy: 1000000 -> "1,000,000"
                    formatted_value = "{:,}".format(int(value))
                    # Set initial value cho field
                    self.fields[field_name].initial = formatted_value
        
        if house:
            # Lấy TẤT CẢ renter từng có hợp đồng với house này (bất kể active hay không)
            all_contracts = HouseRenter.objects.filter(house=house).select_related('renter')

            if all_contracts.exists():
                # Lấy danh sách renter_id từ tất cả hợp đồng (distinct để tránh trùng)
                renter_ids = all_contracts.values_list('renter_id', flat=True).distinct()
                self.fields['renter'].queryset = (
                    Renter.objects.filter(id__in=renter_ids)
                    .order_by('hoten', 'id')
                )

                # Set default là renter có hợp đồng ACTIVE (nếu có)
                active_contract = all_contracts.filter(active=True).first()
                if active_contract:
                    self.fields['renter'].initial = active_contract.renter
                else:
                    # Nếu không có active, chọn hợp đồng gần nhất
                    last_contract = all_contracts.order_by('-rent_from').first()
                    if last_contract:
                        self.fields['renter'].initial = last_contract.renter

                # Cập nhật help text để người dùng biết
                self.fields['renter'].help_text = "Danh sách khách thuê (đã/đang) có hợp đồng với nhà này"
            else:
                # Không có hợp đồng nào, KHÔNG hiển thị renter khác (đúng yêu cầu: chỉ hiển thị renter có HĐ)
                self.fields['renter'].queryset = Renter.objects.none()
                self.fields['renter'].help_text = "Nhà này chưa có hợp đồng nào — bạn có thể để trống trường Khách thuê."
    
class CreateThanhToanForm(forms.ModelForm):
    # Dùng CharField để xử lý định dạng dấu chấm của JS
    tientt = forms.CharField(label="Số tiền Thanh toán (VND)", 
                             required=True, 
                             widget=forms.TextInput(attrs={
                                 'class': 'form-control', 
                                 'onkeyup': 'formatThousands(this)', 
                                 'onkeypress': 'preventNonNumeric(event)' 
                             }))

    class Meta:
        model = Thanhtoan
        # ĐÃ BỎ TRƯỜNG 'phuong_thuc'
        fields = ['tientt', 'ghichu'] 
        
        widgets = {
            'ghichu': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'required': False}),
        }

    # Hàm clean giữ nguyên logic làm sạch tientt
    def clean_tientt(self):
        tientt_str = self.cleaned_data.get('tientt')
        
        if not tientt_str:
            raise ValidationError("Vui lòng nhập số tiền thanh toán.")

        cleaned_value = tientt_str.replace(',', '')

        if not cleaned_value.isdigit() or decimal.Decimal(cleaned_value) <= 0:
            raise ValidationError("Số tiền phải là số nguyên dương hợp lệ.")
            
        return decimal.Decimal(cleaned_value)    