import json
import subprocess
import re
import os
from datetime import datetime
import time

import function.prevent as prevent
import function.internet as internet

# # 数据文件，存储端口的流量信息
# DATA_FILE = 'data.json'
# # 端口列表文件，存储需要监控的端口
# PORTS_FILE = 'ports.json'

# 获取端口流量数据
def get_traffic(port):
    """
    获取指定端口的流量数据。此函数通过执行 `iptables` 命令获取数据包的数量和字节数。

    参数:
        port (int): 端口号

    返回:
        packet_count (int): 数据包的数量
        traffic (int): 流量（字节数）
    """
    try:
        # 执行 iptables 命令，查找特定端口的流量
        command = f"sudo iptables -L -v -n -x | grep 'spt:{port}'"
        result = subprocess.check_output(command, shell=True, text=True)

        # 使用正则表达式提取包数和字节数
        match = re.search(r'(\d+)\s+(\d+)\s+ACCEPT.*\s+spt:(\d+)', result)
        if match:
            packet_count = int(match.group(1))  # 包数
            traffic = int(match.group(2))       # 字节数
            return packet_count, traffic
        else:
            # 如果没有匹配到结果，返回 None
            return None, None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command for port {port}: {e}")
        return None, None

# 重置计数器
def reset_traffic_counters():
    """
    执行 `iptables -Z` 命令重置所有流量计数器，以便下一次采集是从 0 开始。
    """
    try:
        command = "sudo iptables -Z"  # 清除计数器
        subprocess.check_call(command, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Error resetting traffic counters: {e}")

def load_data(port):
    """
    从 `data.json` 文件读取指定端口的流量数据。如果文件不存在或端口没有数据，则返回 [0, 0]。

    参数:
        port (int): 端口号

    返回:
        list: 包含 `packet_count` 和 `traffic` 的列表，如果端口数据不存在，则返回 [0, 0]。
    """
    if os.path.exists("data.json"):
        data = internet.read_file("data.json")  # 读取所有的数据

        # 如果指定端口的数据存在，返回该端口的 packet_count 和 traffic
        if str(port) in data:
            # 假设每个端口只保存了最新的数据
            latest_data = data[str(port)][-1]  # 获取端口数据的最新记录
            packet_count = latest_data.get('packet_count', 0)  # 如果没有 packet_count，返回 0
            traffic = latest_data.get('traffic', 0)  # 如果没有 traffic，返回 0
            return [packet_count, traffic]  # 返回一个列表 [packet_count, traffic]
        else:
            # 如果端口没有数据，返回 [0, 0]
            return [0, 0]
    else:
        # 如果 data.json 文件不存在，返回 [0, 0]
        return [0, 0]

# 更新流量数据并覆盖当前端口数据
def update_traffic_data():
    """
    更新流量数据并保存，当前端口数据会覆盖掉原有的数据。该函数会检查每个端口的流量并更新 `data.json`。
    """
    # 读取当前端口信息
    if os.path.exists("ports.json"):
        ports_info = internet.read_file("ports.json")  # 从 ports.json 读取端口列表
    else:
        ports_info = {'ports': []}  # 如果没有端口列表文件，使用空列表

    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 创建一个新的字典用来保存当前端口的最新数据
    data = {}

    # 遍历所有需要监控的端口
    for port in ports_info['ports']:
        # 获取当前端口的流量
        packet_count, traffic = get_traffic(port)
        packet_count += load_data(port)[0]
        traffic += load_data(port)[1]
        #print(packet_count,traffic)

        # 如果能够获取到流量数据
        if packet_count is not None and traffic is not None:
            # 直接覆盖当前端口的数据
            data[str(port)] = [{
                "timestamp": timestamp,  # 记录流量的时间戳
                "packet_count": packet_count,  # 当前的数据包数量
                "traffic": traffic  # 当前的流量（字节数）
            }]

    # 保存更新后的流量数据（每个端口最新的数据）
    internet.write_file("data.json",data)

# 主循环，每5秒钟检测一次流量
def monitor_traffic():
    """
    主监控循环，每5秒钟检测一次流量，更新 `data.json` 中的端口流量数据，并重置计数器。
    """
    while True:
        # 更新流量数据并覆盖当前端口数据
        update_traffic_data()

        # 重置计数器，确保下一次采集从 0 开始
        reset_traffic_counters()

        # 每5秒钟执行一次
        # 检查流量
        prevent.check_and_block_traffic()
        time.sleep(60)


if __name__ == "__main__":
    # 启动主监控循环
    monitor_traffic()
