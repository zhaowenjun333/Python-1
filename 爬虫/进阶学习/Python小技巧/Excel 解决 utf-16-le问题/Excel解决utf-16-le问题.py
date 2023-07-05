import json
import os
import sys

import pandas as pd


def get_xls_encoding(f_path):
    import chardet
    f = open(f_path, 'rb')
    xls_encoding = chardet.detect(f.read())['encoding']
    f.close()
    return xls_encoding


def get_xls_content(f_path):
    f = open(f_path, 'rb')
    content = f.read().decode('utf-16-le')
    return content


if __name__ == '__main__':
    base_dir = os.path.abspath(os.path.dirname(sys.argv[0] + '/../'))

    file_path = fr'{base_dir}/excel/Leshka.eth ⛩粉丝个性签名.xls'
    new_file_path = file_path.replace('xls', 'xlsx')

    # 自动获取文件编码格式
    file_encoding = get_xls_encoding(file_path)
    print(file_encoding)    # Windows-1254

    # 一、pandas 打开 xls 文件
    # df = pd.read_excel(file_path, engine='xlrd')

    # 二、xlrd 打开 xls 文件
    '''
    import xlrd
    from openpyxl import Workbook
    # 打开原始的 .xls 文件
    xls_wordbook = xlrd.open_workbook(file_path, encoding_override='utf-8')
    # xls_wordbook = xlrd.open_workbook(file_path, encoding_override=file_encoding)
    
    # 创建新的 .xls 文件
    xlsx_workbook = Workbook()
    
    # 获取原始 .xlsx 文件的工作表
    xls_sheet = xls_wordbook.sheet_by_index(0)
    
    # 创建新的 .xlsx 文件的工作表
    xlsx_sheet = xlsx_workbook.active
    
    # 复制原始的 .xls 文件的数据到新的 .xlsx 文件
    for row in range(xls_sheet.nrows):
        for col in range(xls_sheet.ncols):
            cell_value = xls_sheet.cell_value(row, col)
            xlsx_sheet.cell(row=row+1, column=col+1).value = cell_value
    
    # 保存新的 .xlsx 文件
    xlsx_workbook.save(new_file_path)
    '''

    # 三、通过 pyexcel打开 xls 文件
    # import pyexcel
    # xls_data = pyexcel.get_array(file_name=file_path, encoding='utf-8')
    # xls_data = pyexcel.get_array(file_name=file_path, encoding=file_encoding)

    # 四、通过 Excel 打开 xls 并自动另存为 编码为 utf-8 的 xlsx

    import win32com.client as win32

    # 创建 Excel 应用程序对象
    excel = win32.gencache.EnsureDispatch('Excel.Application')

    # 打开源文件
    source_workbook = excel.Workbooks.Open(file_path)

    # 新建目标文件

    target_workbook = excel.Workbooks.Add()
    target_sheet = target_workbook.Sheets(1)

    # 复制源文件中的所有工作表到目标文件
    for sheet_index in range(source_workbook.Sheets.Count):
        source_sheet = source_workbook.Sheets(sheet_index+1)
        if sheet_index == 0:
            source_sheet.UsedRange.Copy(target_sheet.Range("A1"))
        else:
            target_sheet = target_workbook.Sheets.Add(After=target_workbook.Sheets(target_workbook.Sheets.Count))
            source_sheet.UsedRange.Copy(target_sheet.Range("A1"))

    # 关闭源文件
    source_workbook.Close()

    # 另存为目标文件，并设置编码格式
    xlOpenXMLWorkbook = 51   # Excel 2007+ 文件格式
    target_workbook.SaveAs(new_file_path, FileFormat=xlOpenXMLWorkbook)

    # 关闭目标文件
    target_workbook.Close()

    # 退出 Excel 应用程序
    excel.Quit()

    # 测试目标文件是否可以通过 openpyxl 引擎 打开
    if os.path.exists(new_file_path):
        df = pd.read_excel(new_file_path, engine='openpyxl')
        users_list = json.loads(df.to_json(orient='records', force_ascii=False))
        print(users_list)
    else:
        print('没有该文件')
