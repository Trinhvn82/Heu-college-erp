from django.shortcuts import render

def faq_view(request):
    faqs = [
        {
            'question': 'Làm thế nào để đăng ký tài khoản?',
            'answer': 'Nhấn vào "Đăng ký mới" trên trang đăng nhập, và sau đó sẽ được hướng dẫn kích hoạt tài khoản qua email.'
        },
        {
            'question': 'Tôi quên mật khẩu, phải làm sao?',
            'answer': 'Nhấn vào "Quên mật khẩu" trên trang đăng nhập để nhận hướng dẫn khôi phục.'
        },
        {
            'question': 'Tôi cần hướng dẫn nhanh sử dụng phần mềm này.',
            'answer': 'Hệ thống phần mềm này hỗ trợ chủ nhà quản lý các địa điểm cho thuê, mỗi địa điểm có thể gồm nhiều nhà, và mỗi nhà sẽ có các người thuê tương ứng. Chủ nhà có thể cấp tài khoản cho người thuê để quản lý thông tin cá nhân và hóa đơn. Hàng tháng, chủ nhà tạo hóa đơn, người thuê sẽ nhận được thông báo khi có hóa đơn mới. Tình trạng hóa đơn (số tiền đã trả, số tiền còn lại, trạng thái) được cập nhật bởi cả chủ nhà và người thuê. Khi phát sinh sự cố, người thuê có thể gửi báo cáo sự cố trên hệ thống để chủ nhà tiếp nhận và xử lý kịp thời.\nNgoài ra, hệ thống còn cung cấp dashboard giúp người dùng theo dõi tổng quan tình hình như: doanh thu, số hóa đơn tồn đọng, các căn nhà còn trống, v.v..'
        },
        {
            'question': 'Tôi muốn hỏi kỹ hơn vê phần mềm này hoặc có đề xuất cải tiến, phải làm sao?',
            'answer': 'Vui lòng vào Forum và tạo chủ đề mới để thảo luận, chúng tôi sẽ phản hồi trong thời gian sớm nhất.'
        },

    ]
    return render(request, 'sms/faq.html', {'faqs': faqs})
