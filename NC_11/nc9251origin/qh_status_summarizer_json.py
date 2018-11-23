import time
import logging
import os
import json
import datetime
import math

logging.basicConfig(filename='qh_data.log', level=logging.DEBUG)
experiment_flag = False
if experiment_flag:
    origin_money = 130000
else:
    origin_money = 259010
dynamic_money = 0

def generate_daylist():
    result = []
    start = datetime.datetime.strptime("01-01-2017", "%d-%m-%Y")
    end = datetime.datetime.today()
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days + 1)]

    for date_item in date_generated:
        date_str = date_item.strftime("%Y%m%d")
        tmp_date = datetime.datetime.strptime(date_str, "%Y%m%d")
        dow = tmp_date.weekday()
        if dow <= 4:
            result.append(date_str)

    return result
def get_passed_date(date_str):
    date_list = generate_daylist()
    start_idx = date_list.index("20181025")
    end_idx = date_list.index(date_str)
    result = max(end_idx - start_idx+1, 1)
    return result

def read_current_money(output_path):
    global dynamic_money
    money_filename = "C:/profit/money.txt"
    with open(money_filename, "r") as fp:
        lines = fp.readlines()
    lines = [line.strip() for line in lines]
    result = {"current_money": 0}

    if len(lines) > 0:
        tmp_current_money = float(lines[-1].strip())
        tmp_current_date = lines[-2].strip()
        current_profit = round(tmp_current_money - origin_money, ndigits=2)
        tmp_profit_rate = round((tmp_current_money-origin_money)*100/origin_money, ndigits=2)
        dynamic_money = tmp_current_money
        passed_days = get_passed_date(tmp_current_date)
        daily_profit_rate = tmp_profit_rate/passed_days
        should_date_rate = 2.0**(1/240)

        tmp_profit_yty = round(math.pow(1+daily_profit_rate/100, 240)*100-100, ndigits=2) # round(tmp_profit_rate*240/passed_days, ndigits=2)
        should_be = round((math.pow(should_date_rate, passed_days)-1)*origin_money, ndigits=2)#round(origin_money*passed_days/240, ndigits=2)
        advanced = round(current_profit-should_be, ndigits=2)
        if advanced < 0:
            advanced = "(" + str(abs(advanced)) + ")"
        else:
            advanced = str(advanced)

        result['current_money'] = tmp_current_money
        result['current_profit'] = current_profit
        result['profit_rate'] = str(tmp_profit_rate)+"%"
        result['profit_rate_yty'] = str(tmp_profit_yty)+"%"
        result['should_be'] = should_be
        result['advanced'] = advanced

    lines = lines[-20:]
    lines = [line + "\n" for line in lines]
    with open(money_filename, "w") as fp:
        fp.writelines(lines)

    json_file = output_path+"money.json"
    with open(json_file, "w") as json_file:
        json.dump(result, json_file)
    return result


def get_html():

    dir_base = "C:/nginx/html/web/"
    try:
        read_current_money(dir_base)
    except:
        print("Money not retrieved")
    contract_details = {
                           "ZC0": {"name": "动力煤", "market": "郑", "quantity": 100, "contract": 0.05, "cycle_num":13, "category": "黑色"},
                           "CY0": {"name": "棉纱", "market": "郑", "quantity": 5, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "OI0": {"name": "菜籽油", "market": "郑", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "RI0": {"name": "早籼稻", "market": "郑", "quantity": 20, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "WH0": {"name": "强麦", "market": "郑", "quantity": 20, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "FG0": {"name": "玻璃", "market": "郑", "quantity": 20, "contract": 0.05, "cycle_num":13, "category": "化工"},
                           "RS0": {"name": "油菜籽", "market": "郑", "quantity": 10, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "RM0": {"name": "菜籽粕", "market": "郑", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "JR0": {"name": "粳稻", "market": "郑", "quantity": 20, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "LR0": {"name": "晚籼稻", "market": "郑", "quantity": 20, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "SF0": {"name": "硅铁", "market": "郑", "quantity": 5, "contract": 0.05, "cycle_num":8, "category": "黑色"},
                           "SM0": {"name": "锰硅", "market": "郑", "quantity": 5, "contract": 0.05, "cycle_num":8, "category": "黑色"},
                           "CF0": {"name": "棉花", "market": "郑", "quantity": 5, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "SR0": {"name": "白糖", "market": "郑", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "TA0": {"name": "PTA", "market": "郑", "quantity": 5, "contract": 0.05, "cycle_num":13, "category": "化工"},
                           "AP0": {"name": "苹果", "market": "郑", "quantity": 10, "contract": 0.07, "cycle_num":8, "category": "农产品"},
                           "PM0": {"name": "普麦", "market": "郑", "quantity": 50, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "MA0": {"name": "甲醇", "market": "郑", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "化工"},
                           "CS0": {"name": "玉米淀粉", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "M0": {"name": "豆粕", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "A0": {"name": "豆一", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "JM0": {"name": "焦煤", "market": "连", "quantity": 60, "contract": 0.05, "cycle_num":13, "category": "黑色"},
                           "JD0": {"name": "鸡蛋", "market": "连", "quantity": 5, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "I0": {"name": "铁矿石", "market": "连", "quantity": 100, "contract": 0.05, "cycle_num":13, "category": "黑色"},
                           "FB0": {"name": "纤维板", "market": "连", "quantity": 500, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "BB0": {"name": "胶合板", "market": "连", "quantity": 500, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "PP0": {"name": "聚丙烯", "market": "连", "quantity": 5, "contract": 0.05, "cycle_num":8, "category": "化工"},
                           "C0": {"name": "玉米", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":8, "category": "农产品"},
                           "B0": {"name": "豆二", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "Y0": {"name": "豆油", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "L0": {"name": "塑料", "market": "连", "quantity": 5, "contract": 0.05, "cycle_num":8, "category": "化工"},
                           "P0": {"name": "棕榈油", "market": "连", "quantity": 10, "contract": 0.05, "cycle_num":13, "category": "农产品"},
                           "V0": {"name": "PVC", "market": "连", "quantity": 5, "contract": 0.05, "cycle_num":8, "category": "化工"},
                           "J0": {"name": "焦炭", "market": "连", "quantity": 100, "contract": 0.05, "cycle_num":13, "category": "黑色"},
                           "HC0": {"name": "热轧卷板", "market": "沪", "quantity": 10, "contract": 0.04, "cycle_num":12, "category": "黑色"},
                           "CU0": {"name": "铜", "market": "沪", "quantity": 5, "contract": 0.05, "cycle_num":16, "category": "贵金属"},
                           "AL0": {"name": "铝", "market": "沪", "quantity": 5, "contract": 0.05, "cycle_num":16, "category": "有色"},
                           "RU0": {"name": "橡胶", "market": "沪", "quantity": 10, "contract": 0.05, "cycle_num":12, "category": "化工"},
                           "NI0": {"name": "镍", "market": "沪", "quantity": 1, "contract": 0.05, "cycle_num":16, "category": "有色"},
                           "SN0": {"name": "锡", "market": "沪", "quantity": 1, "contract": 0.05, "cycle_num":16, "category": "有色"},
                           "AG0": {"name": "白银", "market": "沪", "quantity": 15, "contract": 0.04, "cycle_num":19, "category": "贵金属"},
                           "BU0": {"name": "沥青", "market": "沪", "quantity": 10, "contract": 0.04, "cycle_num":12, "category": "化工"},
                           "FU0": {"name": "燃料油", "market": "沪", "quantity": 10, "contract": 0.08, "cycle_num":8, "category": "能源"},
                           "ZN0": {"name": "锌", "market": "沪", "quantity": 5, "contract": 0.05, "cycle_num":16, "category": "有色"},
                           "AU0": {"name": "黄金", "market": "沪", "quantity": 1000, "contract": 0.04, "cycle_num":19, "category": "贵金属"},
                           "RB0": {"name": "螺纹钢", "market": "沪", "quantity": 10, "contract": 0.05, "cycle_num":12, "category": "黑色"},
                           "WR0": {"name": "线材", "market": "沪", "quantity": 10, "contract": 0.07, "cycle_num":12, "category": "黑色"},
                           "PB0": {"name": "铅", "market": "沪", "quantity": 5, "contract": 0.05, "cycle_num":16, "category": "有色"},
                           "SC0": {"name": "原油", "market": "沪", "quantity": 1000, "contract": 0.05, "cycle_num":19, "category": "能源"}
                        }
    file_base = "c:/status"
    overall_json = []
    indicator_json = []
    indicator_all_json = []
    scatter_json = []
    recent_amount_json = [{
              "id": '黑色',
              "name": '黑色',
              "color": "#000000"
          }, {
              "id": '农产品',
              "name": '农产品',
              "color": "#000000"
          }, {
              "id": '化工',
              "name": '化工',
              "color": "#000000"
          }, {
              "id": '有色',
              "name": '有色',
              "color": "#000000"
          }, {
              "id": '贵金属',
              "name": '贵金属',
              "color": "#000000"
          }, {
              "id": '能源',
              "name": '能源',
              "color": "#000000"
          }]
    file_list = os.listdir(file_base)
    print("-------")
    overall_list = []
    for filename in file_list:
        file_path = file_base+"/"+filename
        lines = []
        with open(file_path, "r") as fp:
            lines = fp.readlines()
        lines = [line.strip() for line in lines]
        display_unit = lines[-15:]
        overall_list.append(display_unit)
        lines = lines[-20:]
        lines = [line + "\n" for line in lines]
        with open(file_path, "w") as fp:
            fp.writelines(lines)

    onboard_list = []
    overall_list = sorted(overall_list, key=lambda x: abs(int(x[-1])))

    for lines in overall_list:

        current_time = lines[-15]
        score = round(float(lines[-14]), 1)
        contract_size = float(lines[-12])
        contract_hands = str(round(dynamic_money/contract_size))
        big_trend = int(lines[-1])
        small_trend = int(lines[-2])
        profit = float(lines[-3])
        pinzhong_abv = lines[-4][0:-4].upper()
        pinzhong_name = contract_details[pinzhong_abv.upper()+"0"]["name"]
        day_cycles = contract_details[pinzhong_abv.upper()+"0"]["cycle_num"]
        prt_str = lines[-4].upper()+"\t"+pinzhong_name+"\t"+str(big_trend)+"\t"+str(small_trend) + "\t" + str(profit)+"%"
        days = max(round(abs(big_trend/day_cycles), 1),1)
        trend_str = ""
        if big_trend > 0:
            trend_str = "上"
        if big_trend < 0:
            trend_str = "下"

        if small_trend > 0:
            trend_str = trend_str + "<span style='color:red'><small>上</small></span>"
        if small_trend < 0:
            trend_str = trend_str + "<span style='color:lightgreen'><small>下</small></span>"

        daily_profit = str(abs(round(profit/days, 2))) + "%"
        if profit < 0:
            daily_profit = "("+daily_profit+")"

        yty_profit = str(abs(round(profit*240/days, 2))) + "%"
        if profit < 0:
            yty_profit = "(" + yty_profit + ")"

        if big_trend != 0:
            obj_json = {
                "current_time": current_time,
                "pinzhong_abv": pinzhong_abv,
                "pinzhong_name": pinzhong_name + " <small>(" + contract_hands + ")</small>",
                "trend": trend_str,
                "cycles": days,
                "profit": str(profit) + "%",
                "daily_profit": daily_profit,
                "year_to_year": yty_profit,
                "score": score

            }
            overall_json.append(obj_json)
            onboard_list.append(pinzhong_abv)
            print(prt_str)

    overall_list = sorted(overall_list, key=lambda x: abs(int(x[-7])))
    for lines in overall_list:
        current_time = lines[-15]
        score = round(float(lines[-14]), 1)
        distance = float(lines[-13])
        contract_size = float(lines[-12])
        contract_hands = str(round(dynamic_money / contract_size))
        recent_increase_raw = lines[-11]
        recent_increase = int(float(lines[-11])*225/5)
        color_code = "{0:0{1}x}".format(min(abs(recent_increase), 255), 2)
        if recent_increase >= 0:
            color_code = "rgba(255, 0, 0, " + str(abs(recent_increase) / 255) + ")"

        else:
            color_code = "rgba(0, 255, 0, " + str(abs(recent_increase) / 255) + ")"


        recent_amount = lines[-10]
        turning_fact = lines[-9]
        pinzhong_abv = lines[-4][0:-4].upper()
        pinzhong_name = contract_details[pinzhong_abv.upper() + "0"]["name"]
        pinzhong_category = contract_details[pinzhong_abv.upper() + "0"]["category"]
        range_counter = int(lines[-5])
        price_position = int(lines[-6])
        turning_count = int(lines[-7])
        accu = int(lines[-8])

        if accu != 0:
            distance = distance*accu/abs(accu)

        '''
        score = 0
        range_score = range_counter/10
        if range_score > 1:
            range_score = 1
        if range_score < -1:
            range_score = -1
        score += range_score

        turning_score = turning_count / 100
        if turning_score > 1:
            turning_score = 1
        if turning_score < -1:
            turning_score = -1
        score += turning_score

        if accu != 0:
            score += accu / abs(accu)



        price_score = 0
        if price_position >= 85:
            price_score = (price_position - 85) / 15
        elif price_position <= 15:
            price_score = (price_score - 15) / 15
        score += price_score

        distance_score = distance / 4
        if distance_score > 1:
            distance_score = 1
        if distance_score < -1:
            distance_score = -1
        score += distance_score

        score = round(score, ndigits=1)

        '''
        recent_amount_item = {
            "name": pinzhong_name + "<br>"+str(recent_increase_raw)+"%",
            "parent": pinzhong_category,
            "value": int(recent_amount),
            "color": color_code

        }
        recent_amount_json.append(recent_amount_item)

        indicator_json_item = {
            "current_time": current_time,
            "pinzhong_abv": pinzhong_abv,
            "pinzhong_name": pinzhong_name + " <small>(" + contract_hands + ")</small>",
            "distance": distance,
            "range_counter": range_counter,
            "price_position": price_position,
            "turning_count": turning_count,
            "turning_fact": turning_fact,
            "accu": accu,
            "score": score
        }

        if turning_count > 150:
            turning_count = 150
        if turning_count < -150:
            turning_count = -150
        tmp_color = "rgba(0,255,255, 0.5)"
        if turning_count>=80 and score>=4:
            tmp_color = "rgba(255, 0 ,0 , 0.7)"
        if turning_count<=-80 and score<=-4:
            tmp_color = "rgba(0, 255 ,0 , 0.7)"
        scatter_item = {
            "x": turning_count,
            "y": score,
            "z": abs(distance), # math.sqrt(math.pow(turning_count/100, 2) + math.pow(score/6, 2)),
            "name": pinzhong_abv,
            "cname": pinzhong_name,
            "color": tmp_color

        }
        if abs(turning_count) >= 70 and (pinzhong_abv not in onboard_list) and abs(score) > 3.5:
            indicator_json.append(indicator_json_item)
        indicator_all_json.append(indicator_json_item)
        scatter_json.append(scatter_item)

    overall_json = sorted(overall_json, key=lambda x: abs(float(x["cycles"])), reverse=False)
    indicator_json = sorted(indicator_json, key=lambda x: abs(float(x["score"])), reverse=True)
    indicator_all_json = sorted(indicator_all_json, key=lambda x: abs(float(x["score"])), reverse=True)
    #print(json.dumps(overall_json))
    for item in overall_json:
        for idk_item in indicator_all_json:
            if item['pinzhong_abv'] == idk_item['pinzhong_abv']:
                item['pinzhong_abv'] = item['pinzhong_abv'] + "  <small>("+str(idk_item['score'])+")</small>"

    with open(dir_base + "qhitem.json", "w") as json_file:
        overall_json = {"data": overall_json}
        json.dump(overall_json, json_file)
    with open(dir_base + "indicator.json", "w") as json_file:
        indicator_json = {"data": indicator_json, "scatter": scatter_json}
        json.dump(indicator_json, json_file)
    with open(dir_base + "indicatorall.json", "w") as json_file:
        indicator_all_json = {"data": indicator_all_json}
        json.dump(indicator_all_json, json_file)
    with open(dir_base + "recent_amount.json", "w") as json_file:
        recent_amount_json = {"data": recent_amount_json}
        json.dump(recent_amount_json, json_file)

while True:
    get_html()
    time.sleep(30)
