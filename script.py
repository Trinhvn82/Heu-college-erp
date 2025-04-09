import win32com.client


o = win32com.client.Dispatch("Excel.Application")

o.Visible = False

wb_path = 'D:\\Coding\\Python-Code\\College-ERP-v1.1\\media\\sv_kqht.xlsx' #path to your excel file

wb = o.Workbooks.Open(wb_path)



#ws_index_list = [1,4,5] #say you want to print these sheets
ws_index_list = [1] #say you want to print these sheets

path_to_pdf = 'D:\\Coding\\Python-Code\\College-ERP-v1.1\\media\\sv_kqht.pdf'

print_area = 'A1:K98'

try:


    for index in ws_index_list:

        #off-by-one so the user can start numbering the worksheets at 1

        ws = wb.Worksheets[index - 1]

        ws.PageSetup.Zoom = False

        ws.PageSetup.FitToPagesTall = 4

        ws.PageSetup.FitToPagesWide = 1

        ws.PageSetup.PrintArea = print_area



    wb.WorkSheets(ws_index_list).Select()

    wb.ActiveSheet.ExportAsFixedFormat(0, path_to_pdf)
except Exception as e:
    print('failed.'+ str(e))
else:
    print('Succeeded.')
finally:
    #wb.Close()
    wb.Close(SaveChanges=True) 
    o.Quit()