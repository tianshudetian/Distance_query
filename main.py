import xlrd
import pandas as pd
import pos_geocoding as pg

def read_excel():
    wb = xlrd.open_workbook(r'南阳市所有小区信息.xlsx')
    print("读取sheet: "+str(wb.sheet_names()[2]))
    sheet3 = wb.sheet_by_index(2)
    return sheet3

def data_get(sheet3):
    tem_list = []
    for i in range(sheet3.nrows):
        tem1 = sheet3.row(i)
        tem2 = [str(tem1[0])[6:-1], str(tem1[1])[6:-1]]
        tem_list.append(tem2)
    tem3 = pd.DataFrame(tem_list[1:], columns=tem_list[0])
    return tem3

def distance_query_front(pos_name, pos1, data):
    tem_list = []
    for row in data.iterrows():
        distance = pg.distance_get(pos1, row[1]["经纬度"])
        tem_list.append([pos_name, pos1, row[1]["小区名称"], row[1]["经纬度"], distance])
    result = pd.DataFrame(tem_list, columns=["位置点1", "经纬度1", "位置点2", "经纬度2", "距离"])
    return result

def distance_query(data):
    tem_list = []
    for row in data.iterrows():
        if row[0] < data.shape[0]-1:
            tem1 = data.iloc[row[0]+1:]
            tem_list.append(distance_query_front(row[1]["小区名称"], row[1]["经纬度"], tem1))
    result = pd.concat(tem_list)
    return result

sheet =read_excel()
data = data_get(sheet)
result = distance_query(data)
result.to_csv("result.csv")