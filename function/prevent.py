import json
from pathlib import Path

import function.iptables as iptables

# 文件路径
data_file = Path("data.json")
port_file = Path("portinternet.json")

# 读取JSON文件
def read_json(file_path):
    if not file_path.exists():
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 写入JSON文件
def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 检查流量并更新portinternet.json
def check_and_block_traffic():
    # 读取流量数据
    data = read_json(data_file)
    # 读取端口流量上限设置
    port_limits = read_json(port_file)

    # 遍历每个端口
    for port, port_data in data.items():
        if port in port_limits and port_limits[port]["blocked"] is False:
            # 获取当前流量
            total_traffic = sum(entry["traffic"] for entry in port_data)

            # 检查流量是否超过上限
            if total_traffic > port_limits[port]["limit"]:
                print(f"端口 {port} 超过流量！当前流量： {total_traffic} > 限制流量: {port_limits[port]['limit']}")
                # 执行iptables命令阻止端口
                iptables.add_iptables_blackrule(port)

                # 更新portinternet.json，标记该端口已被阻止
                port_limits[port]["blocked"] = True
                write_json(port_file, port_limits)

if __name__ == "__main__":
    check_and_block_traffic()
