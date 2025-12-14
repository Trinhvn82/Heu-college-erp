from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import os

def generate_renter_account_pdf(username, password, full_name=None, system_url=None):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Đăng ký font Unicode (DejaVuSans)
    # Đăng ký font Arial nếu có, nếu không thì dùng Helvetica
    arial_path = None
    if os.name == 'nt':
        arial_path = r'C:\Windows\Fonts\arial.ttf'
    else:
        arial_path = '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf'
    try:
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('Arial', arial_path))
            font_name = 'Arial'
        else:
            font_name = 'Helvetica'
    except Exception:
        font_name = 'Helvetica'

    # Margin cho nội dung
    margin = 40
    y = height-110
    # Tiêu đề phụ
    c.setFont(font_name, 15)
    c.drawString(margin, y, "THÔNG TIN ĐĂNG NHẬP TÀI KHOẢN")
    y -= 30

    # Renter info
    c.setFont(font_name, 12)
    if full_name:
        c.drawString(margin, y, f"Họ tên: {full_name}")
        y -= 20
    c.drawString(margin, y, f"Tên tài khoản: {username}")
    y -= 20

    # Password
    c.drawString(margin, y, f"Mật khẩu: {password if password else '[Không có thông tin]'}")
    y -= 20

    # System URL (lấy từ biến truyền vào)
    c.drawString(margin, y, f"Đường dẫn truy cập hệ thống: {system_url if system_url else '[Không có thông tin]'}")
    y -= 20
    c.showPage()
    c.save()
    pdf_bytes = buffer.getvalue()
    buffer.close()
    if not pdf_bytes or not isinstance(pdf_bytes, bytes):
        raise ValueError("PDF generation failed: No valid PDF bytes returned.")
    return pdf_bytes
