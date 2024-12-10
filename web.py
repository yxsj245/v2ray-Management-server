from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime

app = Flask(__name__)


# 读取流量数据文件
def read_file(filename='data.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


# 读取端口控制文件（例如：portinternet.json）
def read_port_control(filename='portinternet.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


# 读取端口到期时间文件（time_data.json）
def read_time_data(filename='time_data.json'):
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}


# 转换字节数为最佳单位（B, KB, MB, GB）
def format_traffic(traffic):
    if traffic < 1024:
        return f"{traffic} B"
    elif traffic < 1024 ** 2:
        return f"{traffic / 1024:.2f} KB"
    elif traffic < 1024 ** 3:
        return f"{traffic / 1024 ** 2:.2f} MB"
    else:
        return f"{traffic / 1024 ** 3:.2f} GB"


# 转换字节数为 GB 单位
def format_limit(limit):
    if limit < 1024:
        return f"{limit} B"
    elif limit < 1024 ** 2:
        return f"{limit / 1024:.2f} KB"
    elif limit < 1024 ** 3:
        return f"{limit / 1024 ** 2:.2f} MB"
    else:
        return f"{limit / 1024 ** 3:.2f} GB"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_traffic', methods=['GET'])
def get_traffic():
    port = request.args.get('port')  # 从前端获取端口号
    data = read_file()  # 读取流量数据
    port_control = read_port_control()  # 读取端口控制数据
    time_data = read_time_data()  # 读取端口到期时间数据


    if port in data:
        last_entry = data[port][-1]
        traffic = last_entry['traffic']
        formatted_traffic = format_traffic(traffic)
        last_entry['formatted_traffic'] = formatted_traffic  # 添加转换后的流量

        # 获取端口的限制和阻断状态
        port_info = port_control.get(port, {})
        limit = port_info.get('limit', '无')
        blocked = port_info.get('blocked', False)

        # 将最大流量限制转换为 GB
        formatted_limit = format_limit(limit)

        # 获取端口的到期时间
        expiration_time = time_data.get(port, None)[0]

        if expiration_time:
            # 转换为 datetime 对象进行格式化
            expiration_time = datetime.strptime(expiration_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        else:
            expiration_time = "长期"  # 如果没有到期时间，显示 "长期"

        # 返回数据，包括限制和阻断状态以及到期时间
        last_entry['limit'] = formatted_limit
        last_entry['blocked'] = blocked
        last_entry['expiration_time'] = expiration_time  # 添加到期时间

        return jsonify(last_entry)
    else:
        return jsonify({"error": "Port not found"}), 404


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port=5001)
