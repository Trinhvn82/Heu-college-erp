# table_cell_alignment.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph


from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
registerFont(TTFont('Arial','ARIAL.ttf'))

def table_cell_alignment():
    doc = SimpleDocTemplate("table_cell_trn.pdf", pagesize=landscape(A4))
    story = []
    ptext = "Đây là một đoạn văn bản dài để kiểm tra việc căn chỉnh văn bản trong ô của bảng. "
    styles = getSampleStyleSheet()
    ptext = '<font name="Arial">' + ptext + '</font>'

    #ptext = 'This is some <font color=blue size=14>formatted</font> text'
    p = Paragraph(ptext, styles['Normal'])


    data = [
            ['KỲ THỨ: 1', '', '', '', '', '', '', '', '', '', ''],
            ['Môn học/Mô-đun', 'Kết quả học tập Môn học/Mô đun', '', '', '', '', '', '', '', '', ''],
            ['', 'Điểm kiểm tra thường xuyên', '','','Điểm kiểm tra định kỳ', '', '', 'Điểm TB\n điểm\n KT', 'Điểm kiểm tra\n hết MH/MĐ', '', 'Điểm\n tổng\n kết'],
            ['', '', '', '', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', '', 'Lần 1', 'Lần 2', ''],
            ['Môn học 1', '', '', '', '', '', '', '', '', '', ''],
            ['Môn học 1', '', '', '', '', '', '', '', '', '', ''],
            ['Môn học 1', '', '', '', '', '', '', '', '', '', ''],
            [p, '', '', '', '', '', '', '', '', '', ''],
            ['Môn học 1', '', '', '', '', '', '', '', '', '', ''],
            ]

    tblstyle = TableStyle([('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ('FONTNAME', (0,0), (-1,-1), 'Arial'),
                           ('SPAN', (0,0), (-1,0)), # dòng 1
                           ('SPAN', (1,1), (-1,1)), # dòng 2
                           ('SPAN', (0,1), (0,4)), # cột 1, dòng 5
                           ('SPAN', (1,2), (3,4)), # cột 2, dòng 3 - cột 4, dòng 5
                           ('SPAN', (4,2), (6,4)), # cột 5, dòng 3 - cột 5, dòng 5
                           ('SPAN', (7,2), (7,4)), # cột 5, dòng 3 - cột 5, dòng 5
                           ('SPAN', (8,2), (9,3)), # cột 5, dòng 3 - cột 5, dòng 5
                           ('SPAN', (10,2), (10,4)), # cột 5, dòng 3 - cột 5, dòng 5

                           ('VALIGN', (0, 1), (0, 1), 'MIDDLE'),  # second column
                           ('ALIGN', (0,1), (0, 1), 'CENTER'),  # second column

                           ('ALIGN', (0, 0), (0, 0), 'CENTER'),   # first column

                           ('ALIGN', (0, 3), (0, -1), 'LEFT'),   # first column
                           ('ALIGN', (1, 1), (1, 1), 'CENTER'),   # first column

                           ('VALIGN', (1, 2), (10, 4), 'MIDDLE'),  # second column
                           ('ALIGN', (1, 2), (10, 4), 'CENTER'),  # second column
                           ])

    tbl = Table(data, colWidths=[250, 45, 45],               
                )
    tbl.setStyle(tblstyle)
    story.append(tbl)
    story.append(PageBreak())
    story.append(tbl)


    doc.build(story)

if __name__ == '__main__':
    table_cell_alignment()