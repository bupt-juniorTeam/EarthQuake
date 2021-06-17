import json

location_data = open('window/data/location_dict.json', encoding='utf-8')
location_dict = json.load(location_data)
source = {
    '公网': '101',
    '通信网': '202',
    '电网': '203',
    '微博': '301',
    '川滇': '401',
    '基本震情': '501'
}
disaster_info = {
    '人员伤亡及失踪-死亡': '111',
    '人员伤亡及失踪-受伤': '112',
    '人员伤亡及失踪-失踪': '113',
    '房屋破坏-土木': '221',
    '房屋破坏-砖木': '222',
    '房屋破坏-砖混': '223',
    '房屋破坏-框架': '224',
    '房屋破坏-其他': '225',
    '生命线工程灾情-交通': '331',
    '生命线-供水': '332',
    '生命线-输油': '333',
    '生命线-燃气': '334',
    '生命线-电力': '335',
    '生命线-通信': '336',
    '生命线-水利': '337',
    '次生灾害-崩塌': '441',
    '次生灾害-滑坡': '442',
    '次生灾害-泥石流': '443',
    '次生灾害-岩溶塌陷': '444',
    '次生灾害-地裂缝': '445',
    '次生灾害-地面沉降': '446',
    '次生灾害-其他': '447',
    '震情-基本震情': '551',
    '震情-灾情预测': '552'
}
disaster_grade = {
    '特大': '0',
    '重大': '1',
    '较大': '2',
    '一般': '3'
}

location_dict_value = {}
source_value = {}
disaster_info_value = {}
disaster_grade_value = {}
for k, v in location_dict.items():
    location_dict_value.update({v: k})
for k, v in source.items():
    source_value.update({v: k})
for k, v in disaster_info.items():
    disaster_info_value.update({v: k})
for k, v in disaster_grade.items():
    disaster_grade_value.update({v: k})


# 基础地理信息编码
# location_key:
#   非直辖市：xxx省xxx市xxx县(区)
#   直辖市：xxx市xxx区
def get_location_code(location_key):
    # return location_dict[location_key]+'000000'
    return location_dict.get(location_key,'000000') + '000000'


# 灾情信息编码
def get_index_code(index):
    if index >= 999:
        return str(999)
    elif index >= 100:
        return str(index)
    elif index >= 10:
        return '0' + str(index)
    else:
        return '00' + str(index)


def get_grade_code(disaster_grade_key):
    return disaster_grade[disaster_grade_key]


def get_disaster_set_code(disaster_info_key):
    return disaster_info[disaster_info_key]


def get_disaster_info_code(disaster_info_key, index, disaster_grade_key):
    return disaster_info[disaster_info_key] + get_index_code(index) + disaster_grade[disaster_grade_key]


# 数据来源编码 3位
def get_source_code(source_key):
    return source[source_key]


# 灾情数据编码 19位
def get_disaster_code(location_key, disaster_info_key, index, disaster_grade_key):
    return get_location_code(location_key) + get_disaster_info_code(disaster_info_key, index, disaster_grade_key)


# 基本震情编码 26位
# time_key格式：2008年5月12日14时28分04

def get_time_code(time_key):
    year = list('0000')
    month = list('00')
    day = list('00')
    hour = list('00')
    minute = list('00')
    second = list('00')
    # 到年月日中的哪个
    index = 0
    # 年月日中的哪位
    count = 0
    # 防止time_key后面有其他非数字字符
    flag = False
    for ch in time_key[::-1]:
        if '0' <= ch <= '9':
            flag = True
            if index != 5:  # 非年
                if count > 1:
                    # TODO Throw
                    break
                if index == 0:
                    second[1 - count] = ch
                elif index == 1:
                    minute[1 - count] = ch
                elif index == 2:
                    hour[1 - count] = ch
                elif index == 3:
                    day[1 - count] = ch
                elif index == 4:
                    month[1 - count] = ch
            elif index == 5:  # 年
                if count > 3:
                    # TODO Throw
                    break
                year[3 - count] = ch
            count += 1
        else:
            if flag:
                count = 0
                index += 1
    return "".join(year) + "".join(month) + "".join(day) + "".join(hour) + "".join(minute) + "".join(second)


def get_base_code(location_key, time_key):
    location = get_location_code(location_key)
    time = get_time_code(time_key)
    return location + time


# 数据来源解码
def get_source_desc(code):
    source_code = code[0:3]
    return '数据来源：' + source_value[source_code]


# 灾情数据解码
def get_disaster_desc(code, quantity):
    disaster_code = code[3:22]
    location_code = disaster_code[0:12]
    location_code = location_code[0:6]
    info_code = disaster_code[12:15]
    index_code = disaster_code[15:18]
    grade_code = disaster_code[18:]
    return '第{index}号灾情信息：发生在{location}的[{grade}]地震灾害造成{info}{quantity}起'.format(index=str(int(index_code)),
                                                                                 location=location_dict_value[
                                                                                     location_code],
                                                                                 grade=disaster_grade_value[grade_code],
                                                                                 info=disaster_info_value[info_code],
                                                                                 quantity=str(quantity))


# 基本震情解码
def get_base_desc(code):
    base_code = code[22:]
    location_code = base_code[0:12]
    location_code = location_code[0:6]
    time_code = base_code[12:]
    location = location_dict_value[location_code]
    year = str(int(time_code[0:4]))
    month = str(int(time_code[4:6]))
    day = str(int(time_code[6:8]))
    hour = str(int(time_code[8:10]))
    minute = str(int(time_code[10:12]))
    second = str(int(time_code[12:14]))
    return '{year}年{month}月{day}日{hour}时{minute}分{second}秒{location}发生地震'.format(year=year, month=month, day=day,
                                                                                 hour=hour, minute=minute,
                                                                                 second=second,
                                                                                 location=location)
