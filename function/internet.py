import json
import os

# 读取 time_data.json 文件
def read_file(file):
    with open(file, "r") as f:
        return json.load(f)

# 写入 time_data.json 文件
def write_file(file,data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# 更新
def replace_key_in_dict(obj, old_key, new_key):
    if old_key in obj:
        obj[new_key] = obj.pop(old_key)
    return obj

# 增加记录端口
def add_port_to_json(port, filename='ports.json'):
    # 检查文件是否存在
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"ports": []}

    # 如果端口不在已有的列表中，则添加
    if port not in data["ports"]:
        data["ports"].append(port)

    # 将更新后的数据写回文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 增加 到期时间
def set_expiration_time(port, expiration_time):
    # 读取当前目录下的 time_data.json 文件
    try:
        with open('time_data.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，初始化数据
        data = {}

    # 如果端口已经存在，添加新的到期时间，否则初始化为一个列表
    if port in data:
        data[port].append(expiration_time)
    else:
        data[port] = [expiration_time]

    # 将更新后的数据写回文件
    with open('time_data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 设置/更新 预设流量
def set_preset_traffic(port,limit):
    # 读取当前目录下的 portinternet.json 文件
    try:
        with open('portinternet.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，初始化数据
        data = {}

    # 如果端口不存在，初始化端口数据
    if port not in data:
        data[port] = {
            "limit": limit,
            "blocked": False  # 默认不被阻止
        }
    else:
        # 更新已存在端口的限速值
        data[port]["limit"] = limit

    # 将更新后的数据写回文件
    with open('portinternet.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 更新 到期时间
def update_expiration_time(port, expiration_time):
    # 读取当前目录下的 time_data.json 文件
    try:
        with open('time_data.json', 'r') as file:
            data = json.load(file)

        with open('portinternet.json', 'r') as file:
            dataportinternet = json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，初始化数据
        data = {}

    del data[port]  # 删除指定端口的条目
    dataportinternet[port]['blocked'] = False

    # 添加新的到期时间
    data[port] = [expiration_time]

    # 将更新后的数据写回文件
    with open('time_data.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    with open('portinternet.json', 'w') as file:
        json.dump(dataportinternet, file, ensure_ascii=False, indent=4)

# 更新 预设流量
def update_preset_traffic(port,limit):
    try:
        with open('portinternet.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        # 如果文件不存在，初始化数据
        data = {}

    del data[port]
    data[port] = {
        "limit": limit,
        "blocked": False  # 默认不被阻止
    }

    # 将更新后的数据写回文件
    with open('portinternet.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# 删除指定端口所有数据
def delete_port_entry(port_number):
    # 读取 ports.json, time_data.json, data.json, portinternet.json 文件
    try:
        with open('ports.json', 'r', encoding='utf-8') as f:
            ports_data = json.load(f)
    except FileNotFoundError:
        print("ports.json 文件不存在")
        return

    try:
        with open('time_data.json', 'r', encoding='utf-8') as f:
            time_data = json.load(f)
    except FileNotFoundError:
        print("time_data.json 文件不存在")
        return

    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("data.json 文件不存在")
        return

    try:
        with open('portinternet.json', 'r', encoding='utf-8') as f:
            portinternet_data = json.load(f)
    except FileNotFoundError:
        print("portinternet.json 文件不存在")
        return

    print('开始删除端口')
    # 删除指定端口号的条目
    if port_number in ports_data.get("ports", []):
        ports_data["ports"].remove(port_number)
        # print(f"删除 ports.json 中端口号 {port_number} 的条目")
    else:
        print(f"ports.json 中没有找到端口号 {port_number}")

    if str(port_number) in time_data:
        del time_data[str(port_number)]
        # print(f"删除 time_data.json 中端口号 {port_number} 的条目")
    else:
        print(f"time_data.json 中没有找到端口号 {port_number}")

    if str(port_number) in data:
        del data[str(port_number)]
        # print(f"删除 data.json 中端口号 {port_number} 的条目")
    else:
        print(f"data.json 中没有找到端口号 {port_number}")

    if str(port_number) in portinternet_data:
        del portinternet_data[str(port_number)]
        # print(f"删除 portinternet.json 中端口号 {port_number} 的条目")
    else:
        print(f"portinternet.json 中没有找到端口号 {port_number}")

    # 将更新后的数据写回文件
    with open('ports.json', 'w', encoding='utf-8') as f:
        json.dump(ports_data, f, ensure_ascii=False, indent=4)

    with open('time_data.json', 'w', encoding='utf-8') as f:
        json.dump(time_data, f, ensure_ascii=False, indent=4)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    with open('portinternet.json', 'w', encoding='utf-8') as f:
        json.dump(portinternet_data, f, ensure_ascii=False, indent=4)

    print('删除完毕')

# 删除portinternet.json文件中所有true的值
def delete_blocked_ports():
    # 读取 portinternet.json 文件
    try:
        with open('portinternet.json', 'r', encoding='utf-8') as f:
            portinternet_data = json.load(f)
    except FileNotFoundError:
        print("portinternet.json 文件不存在")
        return

    # 查找所有 blocked 为 true 的端口号并调用 delete_port_entry 删除
    for port, data in portinternet_data.items():
        if data.get('blocked') is True:
            print(f"删除被阻止的端口 {port}")
            delete_port_entry(int(port))  # 调用 delete_port_entry 并传递端口号
        else:
            print('没有需要删除的端口')

# 查看到期时间 提交端口返回到期时间
def Expiration_date(port):
    try:
        fanhui = read_file('time_data.json')[str(port)][0]
        return fanhui
    except Exception as e:
        return '参数错误'

# 查看限制流量 提交端口返回预设流量和当前状态
def Restrict_traffic(port):
    try:
        fanhui = read_file('portinternet.json')[str(port)]
        return fanhui
    except Exception as e:
        return '参数错误'

# 查看流量信息 提交端口返回最后更新时间，包数目，当前流量字节
def flow_information(port):
    try:
        fanhui = read_file('data.json')[str(port)][0]
        return fanhui
    except Exception as e:
        return '参数错误'