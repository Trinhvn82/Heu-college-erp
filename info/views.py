from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from .models import Dept, Class, Student, Attendance, Course, Teacher, Assign, AttendanceTotal, time_slots, \
    DAYS_OF_WEEK, AssignTime, AttendanceClass, StudentCourse, Marks, MarksClass
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from sms.models import Hsns, Hsgv, Hssv
from django.http import HttpResponseForbidden,HttpResponse



User = get_user_model()

# Create your views here.


@login_required
def index(request):
    if request.user.is_teacher:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/homepage.html')
    if request.user.is_superuser:
        return render(request, 'info/admin_page.html')
    return render(request, 'info/logout.html')


@login_required()
def attendance(request, stud_id):
    stud = Student.objects.get(USN=stud_id)
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    att_list = []
    for ass in ass_list:
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'info/attendance.html', {'att_list': att_list})


@login_required()
def attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/att_detail.html', {'att_list': att_list, 'cr': cr})


# Teacher Views

@login_required
def t_clas(request, teacher_id, choice):
    teacher1 = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'info/t_clas.html', {'teacher1': teacher1, 'choice': choice})


@login_required()
def t_student(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    att_list = []
    for stud in ass.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=stud, course=ass.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=stud, course=ass.course)
            a.save()
        att_list.append(a)
    return render(request, 'info/t_students.html', {'att_list': att_list})


@login_required()
def t_class_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    att_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
    return render(request, 'info/t_class_date.html', {'att_list': att_list})


@login_required()
def cancel_class(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    assc.status = 2
    assc.save()
    return HttpResponseRedirect(reverse('t_class_date', args=(assc.assign_id,)))


@login_required()
def t_attendance(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'assc': assc,
    }
    return render(request, 'info/t_attendance.html', context)


@login_required()
def edit_att(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    cr = assc.assign.course
    att_list = Attendance.objects.filter(attendanceclass=assc, course=cr)
    context = {
        'assc': assc,
        'att_list': att_list,
    }
    return render(request, 'info/t_edit_att.html', context)


@login_required()
def confirm(request, ass_c_id):
    assc = get_object_or_404(AttendanceClass, id=ass_c_id)
    ass = assc.assign
    cr = ass.course
    cl = ass.class_id
    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if assc.status == 1:
            try:
                a = Attendance.objects.get(course=cr, student=s, date=assc.date, attendanceclass=assc)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
                a.save()
        else:
            a = Attendance(course=cr, student=s, status=status, date=assc.date, attendanceclass=assc)
            a.save()
            assc.status = 1
            assc.save()

    return HttpResponseRedirect(reverse('t_class_date', args=(ass.id,)))


@login_required()
def t_attendance_detail(request, stud_id, course_id):
    stud = get_object_or_404(Student, USN=stud_id)
    cr = get_object_or_404(Course, id=course_id)
    att_list = Attendance.objects.filter(course=cr, student=stud).order_by('date')
    return render(request, 'info/t_att_detail.html', {'att_list': att_list, 'cr': cr})


@login_required()
def change_att(request, att_id):
    a = get_object_or_404(Attendance, id=att_id)
    a.status = not a.status
    a.save()
    return HttpResponseRedirect(reverse('t_attendance_detail', args=(a.student.USN, a.course_id)))


@login_required()
def t_extra_class(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
    }
    return render(request, 'info/t_extra_class.html', context)


@login_required()
def e_confirm(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    cr = ass.course
    cl = ass.class_id
    assc = ass.attendanceclass_set.create(status=1, date=request.POST['date'])
    assc.save()

    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        date = request.POST['date']
        a = Attendance(course=cr, student=s, status=status, date=date, attendanceclass=assc)
        a.save()

    return HttpResponseRedirect(reverse('t_clas', args=(ass.teacher_id, 1)))


@login_required()
def t_report(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    sc_list = []
    for stud in ass.class_id.student_set.all():
        a = StudentCourse.objects.get(student=stud, course=ass.course)
        sc_list.append(a)
    return render(request, 'info/t_report.html', {'sc_list': sc_list})


@login_required()
def timetable(request, class_id):
    asst = AssignTime.objects.filter(assign__class_id=class_id)
    matrix = [['' for i in range(12)] for j in range(6)]

    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(12):
            if j == 0:
                matrix[i][0] = d[0]
                continue
            if j == 4 or j == 8:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                matrix[i][j] = a.assign.course_id
            except AssignTime.DoesNotExist:
                pass
            t += 1

    context = {'matrix': matrix}
    return render(request, 'info/timetable.html', context)


@login_required()
def t_timetable(request, teacher_id):
    asst = AssignTime.objects.filter(assign__teacher_id=teacher_id)
    class_matrix = [[True for i in range(12)] for j in range(6)]
    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(12):
            if j == 0:
                class_matrix[i][0] = d[0]
                continue
            if j == 4 or j == 8:
                continue
            try:
                a = asst.get(period=time_slots[t][0], day=d[0])
                class_matrix[i][j] = a
            except AssignTime.DoesNotExist:
                pass
            t += 1

    context = {
        'class_matrix': class_matrix,
    }
    return render(request, 'info/t_timetable.html', context)


@login_required()
def free_teachers(request, asst_id):
    asst = get_object_or_404(AssignTime, id=asst_id)
    ft_list = []
    t_list = Teacher.objects.filter(assign__class_id__id=asst.assign.class_id_id)
    for t in t_list:
        at_list = AssignTime.objects.filter(assign__teacher=t)
        if not any([True if at.period == asst.period and at.day == asst.day else False for at in at_list]):
            ft_list.append(t)

    return render(request, 'info/free_teachers.html', {'ft_list': ft_list})


# student marks


@login_required()
def marks_list(request, stud_id):
    stud = Student.objects.get(USN=stud_id, )
    ass_list = Assign.objects.filter(class_id_id=stud.class_id)
    sc_list = []
    for ass in ass_list:
        try:
            sc = StudentCourse.objects.get(student=stud, course=ass.course)
        except StudentCourse.DoesNotExist:
            sc = StudentCourse(student=stud, course=ass.course)
            sc.save()
            sc.marks_set.create(type='I', name='Internal test 1')
            sc.marks_set.create(type='I', name='Internal test 2')
            sc.marks_set.create(type='I', name='Internal test 3')
            sc.marks_set.create(type='E', name='Event 1')
            sc.marks_set.create(type='E', name='Event 2')
            sc.marks_set.create(type='S', name='Semester End Exam')
        sc_list.append(sc)

    return render(request, 'info/marks_list.html', {'sc_list': sc_list})


# teacher marks


@login_required()
def t_marks_list(request, assign_id):
    ass = get_object_or_404(Assign, id=assign_id)
    m_list = MarksClass.objects.filter(assign=ass)
    return render(request, 'info/t_marks_list.html', {'m_list': m_list})


@login_required()
def t_marks_entry(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    c = ass.class_id
    context = {
        'ass': ass,
        'c': c,
        'mc': mc,
    }
    return render(request, 'info/t_marks_entry.html', context)


@login_required()
def marks_confirm(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    ass = mc.assign
    cr = ass.course
    cl = ass.class_id
    for s in cl.student_set.all():
        mark = request.POST[s.USN]
        sc = StudentCourse.objects.get(course=cr, student=s)
        m = sc.marks_set.get(name=mc.name)
        m.marks1 = mark
        m.save()
    mc.status = True
    mc.save()

    return HttpResponseRedirect(reverse('t_marks_list', args=(ass.id,)))


@login_required()
def edit_marks(request, marks_c_id):
    mc = get_object_or_404(MarksClass, id=marks_c_id)
    cr = mc.assign.course
    stud_list = mc.assign.class_id.student_set.all()
    m_list = []
    for stud in stud_list:
        sc = StudentCourse.objects.get(course=cr, student=stud)
        m = sc.marks_set.get(name=mc.name)
        m_list.append(m)
    context = {
        'mc': mc,
        'm_list': m_list,
    }
    return render(request, 'info/edit_marks.html', context)


@login_required()
def student_marks(request, assign_id):
    ass = Assign.objects.get(id=assign_id)
    sc_list = StudentCourse.objects.filter(student__in=ass.class_id.student_set.all(), course=ass.course)
    return render(request, 'info/t_student_marks.html', {'sc_list': sc_list})


@login_required()
def add_teacher(request):
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        dept = get_object_or_404(Dept, id=request.POST['dept'])
        name = request.POST['full_name']
        id = request.POST['id'].lower()
        dob = request.POST['dob']
        sex = request.POST['sex']
        
        # Creating a User with teacher username and password format
        # USERNAME: firstname + underscore + unique ID
        # PASSWORD: firstname + underscore + year of birth(YYYY)
        user = User.objects.create_user(
            username=name.split(" ")[0].lower() + '_' + id,
            password=name.split(" ")[0].lower() + '_' + dob.replace("-","")[:4]
        )
        user.save()

        Teacher(
            user=user,
            id=id,
            dept=dept,
            name=name,
            sex=sex,
            DOB=dob
        ).save()
        return redirect('/')
    
    all_dept = Dept.objects.order_by('-id')
    context = {'all_dept': all_dept}

    return render(request, 'info/add_teacher.html', context)


@login_required()
def add_student(request):
    # If the user is not admin, they will be redirected to home
    if not request.user.is_superuser:
        return redirect("/")

    if request.method == 'POST':
        # Retrieving all the form data that has been inputted
        class_id = get_object_or_404(Class, id=request.POST['class'])
        name = request.POST['full_name']
        usn = request.POST['usn']
        dob = request.POST['dob']
        sex = request.POST['sex'] 

        # Creating a User with student username and password format
        # USERNAME: firstname + underscore + last 3 digits of USN
        # PASSWORD: firstname + underscore + year of birth(YYYY)
        user = User.objects.create_user(
            username=name.split(" ")[0].lower() + '_' + request.POST['usn'][-3:],
            password=name.split(" ")[0].lower() + '_' + dob.replace("-","")[:4]
        )
        user.save()

        # Creating a new student instance with given data and saving it.
        Student(
            user=user,
            USN=usn,
            class_id=class_id,
            name=name,
            sex=sex,
            DOB=dob
        ).save()
        return redirect('/')
    
    all_classes = Class.objects.order_by('-id')
    context = {'all_classes': all_classes}
    return render(request, 'info/add_student.html', context)

@login_required()
@permission_required('info.add_user',raise_exception=True)
def add_gvuser(request, id):
    # if not request.user.is_superuser:
    #     #return redirect("/")
    #     return HttpResponseForbidden("Bạn không có quyền thực hiện chức năng này")
    gv = Hsgv.objects.get(id = id)
    # Check if username already exists
    if User.objects.filter(username="gv_"+gv.ma).exists():
        messages.error(request, 'Username already exists')
        return redirect('ns_list')    
    
    user = User.objects.create_user(
        username="gv_"+gv.ma,
        first_name = gv.hoten,
        password=gv.ma + '@123654'
    )
    if Group.objects.filter(name = 'GVTG').exists():
        gr =  Group.objects.get(name = 'GVTG')
    else:
        gr = Group.objects.create(name='GVTG')

    user.groups.add(gr)
    user.save()
    gv.user = user
    gv.save()
    messages.success(request, "Tạo tài khoản cho " + gv.hoten + " thành công")
    return redirect("gv_list")

@login_required()
@permission_required('info.add_user',raise_exception=True)
def add_hvuser(request, id):
    # if not request.user.is_superuser:
    #     return redirect("/")
    sv = Hssv.objects.get(id = id)
    # Check if username already exists
    if User.objects.filter(username="hv_"+sv.msv).exists():
        messages.error(request, 'Username already exists')
        return redirect('sv_list')    
    
    user = User.objects.create_user(
        username="hv_"+sv.msv,
        first_name = sv.hoten,
        password=sv.msv + '@123654'
    )
    if Group.objects.filter(name = 'HV').exists():
        gr =  Group.objects.get(name = 'HV')
    else:
        gr = Group.objects.create(name='HV')

    user.groups.add(gr)
    user.save()
    sv.user = user
    sv.save()
    messages.success(request, "Tạo tài khoản cho " + sv.hoten + " thành công")
    return redirect("sv_list")

@login_required()
@permission_required('info.add_user',raise_exception=True)
def reset_pwd(request, ns_id):
    # if not request.user.is_superuser:
    #     return redirect("/")
    ns = Hsns.objects.get(id = ns_id)
    # Check if username already exists
    if ns.user:
        ns.user.set_password(ns.ma + '@123654')
        ns.user.save()    
        messages.success(request, "Reset password thành công!")
        return redirect('ns_list')    
    return redirect("ns_list")

@login_required()
@permission_required('info.add_user',raise_exception=True)
def reset_pwd_gv(request, gv_id):
    # if not request.user.is_superuser:
    #     return redirect("/")
    gv = Hsgv.objects.get(id = gv_id)
    # Check if username already exists
    if gv.user:
        gv.user.set_password(gv.ma + '@123654')
        gv.user.save()    
        messages.success(request, "Reset password thành công!")
        return redirect('gv_list')    
    return redirect("gv_list")

@login_required()
@permission_required('info.add_user',raise_exception=True)
def reset_pwd_hv(request, hv_id):
    # if not request.user.is_superuser:
    #     return redirect("/")
    sv = Hssv.objects.get(id = hv_id)
    # Check if username already exists
    if sv.user:
        sv.user.set_password(sv.msv + '@123654')
        sv.user.save()    
        messages.success(request, "Reset password thành công!")
        return redirect('sv_list')    
    return redirect("sv_list")

@login_required()
@permission_required('info.add_user',raise_exception=True)
def add_nsuser(request, id):
    # if not request.user.is_superuser:
    #     return redirect("/")
    ns = Hsns.objects.get(id = id)
    # Check if username already exists
    if User.objects.filter(username="ns_" +ns.ma).exists():
        messages.error(request, 'Username already exists')
        return redirect('ns_list')    
    
    user = User.objects.create_user(
        username="ns_" +ns.ma,
        first_name = ns.hoten,
        password=ns.ma + '@123654'
    )
    user.save()
    ns.user = user
    ns.save()
    messages.success(request, "Tạo tài khoản cho " + ns.hoten + " thành công")
    return redirect("ns_list")

@login_required
def user_changepwd(request):

    if request.method == "POST":
        user = User.objects.get(username = request.user.username)
        user.set_password(request.POST.get('password', None))
        user.save()    
        messages.success(request, "Thay doi password thanh cong!")
        return redirect("lop_list")
    return render(request, "sms/changepwd.html")

@login_required()
@permission_required('info.add_user',raise_exception=True)
def ns_quyen(request, ns_id):
    from django.contrib.auth.models import Group

    ns = Hsns.objects.get(id = ns_id)
    user = User.objects.get(id=ns.user_id)
    groups = Group.objects.all()
    if request.method == "POST":
        for gr in groups:
            id = "C"+str(gr.id)
            print(id)
            print(request.POST[id])
            if request.POST[id] == "1" :
                user.groups.add(gr)
                print(id)
                print("add group")
            else:
                user.groups.remove(gr)
                print(id)
                print("remove group")
        
        #     id = "C"+str(stud.id)
        #     status = request.POST[id]
        #     dd = Diemdanh.objects.get(lichhoc_id = lh_id, sv_id=stud.id)
        #     dd.status=status
        #     dd.save() 
        # ttlh.status=1
        # ttlh.save()
        messages.success(request, "Cập nhật lớp thành công!")
        return redirect("ns_list")
    lol=[]
    for gr in groups:
        if user.groups.filter(name = gr.name).exists():
            lol.append({ "name":gr.name,"status": 1})
            gr.status = 1
        else:
            gr.status = 0
            lol.append({ "name":gr.name,"status": 0})

    #groups = Group.objects.all()
    context = {
        "ns_id": ns_id,
        "groups": groups
    }
    return render(request, "sms/ns_quyen.html", context)

@login_required
def add_groups(request):
    from django.contrib.auth.models import Group
    from django.contrib.auth.models import Permission

    group = Group.objects.create(name = "CTSV Test")

    permission = Permission.objects.get(codename='add_hssv')
    group.permissions.add(permission)
    
    group.save()

    group = Group.objects.create(name = "Đào tạo Test")

    permission = Permission.objects.get(codename='add_lichhoc')
    group.permissions.add(permission)
    
    permission = Permission.objects.get(codename='add_lopmonhoc')
    group.permissions.add(permission)

    group.save()

    group = Group.objects.create(name = "Kê toán Test")

    permission = Permission.objects.get(codename='add_hp81')
    group.permissions.add(permission)
    

    group.save()

    group = Group.objects.create(name = "Nhân sự Test")

    permission = Permission.objects.get(codename='add_hsgv')
    group.permissions.add(permission)
    

    group.save()

    group = Group.objects.create(name = "Giao viên Test")

    permission = Permission.objects.get(codename='add_diemdanh')
    group.permissions.add(permission)
    
    permission = Permission.objects.get(codename='add_diemthanhphan')
    group.permissions.add(permission)

    group.save()

    return redirect("ns_list")