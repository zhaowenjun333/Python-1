import openpyxl
import re

path = '土压力运算.xlsx'
wb1 = openpyxl.load_workbook(path)
wb2 = openpyxl.load_workbook(path, data_only=True)

sheet1 = wb1.worksheets[0]
sheet2 = wb2.worksheets[0]

# S
line3_S = re.compile(r'=20\*(.*?)-2\*(.*?)\*(.*)', re.S)
line4_S = re.compile(r'=\(20\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line5_S = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line6_S = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line7_S = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line8_S = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line9_S = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line10_S = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
f_S = open('S列公式.txt', 'w', encoding='utf-8')

# T
line3_T = re.compile(r'=\(20\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line4_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line5_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line6_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line7_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line8_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line9_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
line10_T = re.compile(r'=\(20\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)-2\*(.*?)\*(.*)', re.S)
f_T = open('T列公式.txt', 'w', encoding='utf-8')

# U
line7_U = re.compile(r'=0\*(.*?)\+2\*(.*?)\*(.*)', re.S)
line8_U = re.compile(r'=\(0\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
line9_U = re.compile(r'=\(0\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
line10_U = re.compile(r'=\(0\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
f_U = open('U列公式.txt', 'w', encoding='utf-8')

# V
line7_V = re.compile(r'=\(0\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
line8_V = re.compile(r'=\(0\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
line9_V = re.compile(r'=\(0\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
line10_V = re.compile(r'=\(0\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\+(.*?)\*(.*?)\)\*(.*?)\+2\*(.*?)\*(.*)', re.S)
f_V = open('V列公式.txt', 'w', encoding='utf-8')

# W
# =U7-S7
line7_W = re.compile(r'=(.*?)-(.*)', re.S)
line8_W = re.compile(r'=(.*?)-(.*)', re.S)
line9_W = re.compile(r'=(.*?)-(.*)', re.S)
line10_W = re.compile(r'=(.*?)-(.*)', re.S)
f_W = open('W列公式.txt', 'w', encoding='utf-8')

# X
line7_X = re.compile(r'=(.*?)-(.*)', re.S)
line8_X = re.compile(r'=(.*?)-(.*)', re.S)
line9_X = re.compile(r'=(.*?)-(.*)', re.S)
line10_X = re.compile(r'=(.*?)-(.*)', re.S)
f_X = open('X列公式.txt', 'w', encoding='utf-8')

for j in range(0, 4):
    n = 3 + j * 10
    m = 7 + j * 10
    for i in range(n, n+8):
        s = f'S{i}'
        s_value = sheet1[s].value

        t = f'T{i}'
        t_value = sheet1[t].value
        # print(t_value)
        if i in [3, 13, 23, 33]:
            line3_s_lst = line3_S.findall(s_value)[0]
            for a in line3_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line3_t_lst = line3_T.findall(t_value)[0]
            for b in line3_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [4, 14, 24, 34]:
            line4_s_lst = line4_S.findall(s_value)[0]
            for a in line4_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line4_t_lst = line4_T.findall(t_value)[0]
            for b in line4_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [5, 15, 25, 35]:
            line5_s_lst = line5_S.findall(s_value)[0]
            for a in line5_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line5_t_lst = line5_T.findall(t_value)[0]
            for b in line5_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [6, 16, 26, 36]:
            line6_s_lst = line6_S.findall(s_value)[0]
            for a in line6_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line6_t_lst = line6_T.findall(t_value)[0]
            for b in line6_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [7, 17, 27, 37]:
            line7_s_lst = line7_S.findall(s_value)[0]
            for a in line7_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line7_t_lst = line7_T.findall(t_value)[0]
            for b in line7_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [8, 18, 28, 38]:
            line8_s_lst = line8_S.findall(s_value)[0]
            for a in line8_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line8_t_lst = line8_T.findall(t_value)[0]
            for b in line8_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [9, 19, 29, 39]:
            line9_s_lst = line9_S.findall(s_value)[0]
            for a in line9_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line9_t_lst = line9_T.findall(t_value)[0]
            for b in line9_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
        elif i in [10, 20, 30, 40]:
            line10_s_lst = line10_S.findall(s_value)[0]
            for a in line10_s_lst:
                s_value = s_value.replace(a, str(sheet2[a].value))
            f_S.write(f'第{i}行公式：{s_value}\n')
            line10_t_lst = line10_T.findall(t_value)[0]
            for b in line10_t_lst:
                t_value = t_value.replace(b, str(sheet2[b].value))
            f_T.write(f'第{i}行公式：{t_value}\n')
    for k in range(m, m+4):
        # print(k)
        u = f'U{k}'
        u_value = sheet1[u].value

        v = f'V{k}'
        v_value = sheet1[v].value

        w = f'W{k}'
        w_value = sheet1[w].value
        # print(w_value)

        x = f'X{k}'
        x_value = sheet1[x].value
        if k in [7, 17, 27, 37]:
            line7_u_lst = line7_U.findall(u_value)[0]
            for a in line7_u_lst:
                u_value = u_value.replace(a, str(sheet2[a].value))
            f_U.write(f'第{k}行公式：{u_value}\n')
            line7_v_lst = line7_V.findall(v_value)[0]
            for b in line7_v_lst:
                v_value = v_value.replace(b, str(sheet2[b].value))
            f_V.write(f'第{k}行公式：{v_value}\n')
            line7_w_lst = line7_W.findall(w_value)[0]
            for c in line7_w_lst:
                w_value = w_value.replace(c, '%.2f' % sheet2[c].value)
            f_W.write(f'第{k}行公式：{w_value}\n')
            line7_x_lst = line7_X.findall(x_value)[0]
            for d in line7_x_lst:
                x_value = x_value.replace(d, '%.2f' % sheet2[d].value)
            f_X.write(f'第{k}行公式：{x_value}\n')
        elif k in [8, 18, 28, 38]:
            line8_u_lst = line8_U.findall(u_value)[0]
            for a in line8_u_lst:
                u_value = u_value.replace(a, str(sheet2[a].value))
            f_U.write(f'第{k}行公式：{u_value}\n')
            line8_v_lst = line8_V.findall(v_value)[0]
            for b in line8_v_lst:
                v_value = v_value.replace(b, str(sheet2[b].value))
            f_V.write(f'第{k}行公式：{v_value}\n')
            line8_w_lst = line8_W.findall(w_value)[0]
            for c in line8_w_lst:
                w_value = w_value.replace(c, '%.2f' % sheet2[c].value)
            f_W.write(f'第{k}行公式：{w_value}\n')
            line8_x_lst = line8_X.findall(x_value)[0]
            for d in line8_x_lst:
                x_value = x_value.replace(d, '%.2f' % sheet2[d].value)
            f_X.write(f'第{k}行公式：{x_value}\n')
        elif k in [9, 19, 29, 39]:
            line9_u_lst = line9_U.findall(u_value)[0]
            for a in line9_u_lst:
                u_value = u_value.replace(a, str(sheet2[a].value))
            f_U.write(f'第{k}行公式：{u_value}\n')
            line9_v_lst = line9_V.findall(v_value)[0]
            for b in line9_v_lst:
                v_value = v_value.replace(b, str(sheet2[b].value))
            f_V.write(f'第{k}行公式：{v_value}\n')
            line9_w_lst = line9_W.findall(w_value)[0]
            for c in line9_w_lst:
                w_value = w_value.replace(c, '%.2f' % sheet2[c].value)
            f_W.write(f'第{k}行公式：{w_value}\n')
            line9_x_lst = line9_X.findall(x_value)[0]
            for d in line9_x_lst:
                x_value = x_value.replace(d, '%.2f' % sheet2[d].value)
            f_X.write(f'第{k}行公式：{x_value}\n')
        elif k in [10, 20, 30, 40]:
            line10_u_lst = line10_U.findall(u_value)[0]
            for a in line10_u_lst:
                u_value = u_value.replace(a, str(sheet2[a].value))
            f_U.write(f'第{k}行公式：{u_value}\n')
            line10_v_lst = line10_V.findall(v_value)[0]
            for b in line10_v_lst:
                v_value = v_value.replace(b, str(sheet2[b].value))
            f_V.write(f'第{k}行公式：{v_value}\n')
            line10_w_lst = line10_W.findall(w_value)[0]
            for c in line10_w_lst:
                w_value = w_value.replace(c, '%.2f' % sheet2[c].value)
            f_W.write(f'第{k}行公式：{w_value}\n')
            line10_x_lst = line10_X.findall(x_value)[0]
            for d in line10_x_lst:
                x_value = x_value.replace(d, '%.2f' % sheet2[d].value)
            f_X.write(f'第{k}行公式：{x_value}\n')
    print('\n')
f_S.close()
f_T.close()
f_U.close()
f_V.close()
f_W.close()
f_X.close()
print('over!')

