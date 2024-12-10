import json
import os
import time
from datetime import datetime
import subprocess
import schedule

import function.internet as internet
import function.iptables as iptables
import function.v2ray as v2ray

# 创建 time_data.json 文件并初始化
def init_time_data():
    if not os.path.exists("time_data.json"):
        internet.write_file("time_data.json",{})

# 每天检查并执行到期端口阻止
def check_expired_ports():
    time_data = internet.read_file("time_data.json")
    current_time = datetime.now()

    print(f"正在检查过期端口 {current_time.strftime('%Y-%m-%d %H:%M:%S')}...")

    for port, expiration_time_str in time_data.items():
        expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M:%S")

        print(f"端口 {port} 到期日 {expiration_time.strftime('%Y-%m-%d %H:%M:%S')}")

        port_limits = internet.read_file("portinternet.json")

        if port_limits.get(port, {}).get("blocked", False):
            print(f"端口 {port} 已经被阻止，跳过处理。")
            continue

        if expiration_time <= current_time:
            print(f"阻止端口 {port} 由于到期。")
            iptables.add_iptables_blackrule(port)

            port_limits[port]["blocked"] = True
            internet.write_file("portinternet.json",port_limits)
        # else:
        #     print(f"端口 {port} 尚未过期。")


# 固定事件
def reset_ports():
    current_time = datetime.now()
    # 每月1日执行流量重置
    if current_time.day == 1:
        print('正在执行重置流量')
        # 读取 time_data.json 文件，获取需要重置的端口
        if os.path.exists("time_data.json"):
            time_data = internet.read_file("time_data.json")

            # 获取 time_data.json 中的所有端口
            ports_to_reset = time_data.keys()
            # print(f"Ports to reset: {ports_to_reset}")
        else:
            # print("time_data.json does not exist!")
            return

        # 读取 data.json 文件，更新指定端口的流量数据
        if os.path.exists("data.json"):
            data = internet.read_file("data.json")

            # 打印加载的 data.json 数据
            # print("Loaded data from data.json:", json.dumps(data, indent=4))

            for port in list(data.keys()):  # 使用 list 以便在循环时可以修改字典
                if str(port) in ports_to_reset:  # 仅对 time_data.json 中存在的端口进行重置
                    # print(f"Resetting stats for port {port}...")
                    for stat in data[port]:
                        # print(f"Resetting packet_count and traffic for port {port}")
                        stat["packet_count"] = 0
                        stat["traffic"] = 0
                # else:
                    # print(f"Skipping port {port} because it is not in time_data.json")

            # 写入更新后的数据
            internet.write_file("data.json",data)
            # print("Updated data.json:", json.dumps(data, indent=4))
        # else:
        #     print("data.json does not exist!")

        # 对每个端口执行解除阻止命令
        for port in ports_to_reset:
            # print(f"Unblocking port {port} for reset.")
            iptables.remove_iptables_blackrule(port)
        print('重置完毕')

    # 每月30日执过期用户删除
    if current_time.day == 30:
        print('正在执行到期用户删除操作')
        print('执行初始化防火墙')
        # 读取 portinternet.json 文件
        try:
            portinternet_data = internet.read_file("portinternet.json")
        except FileNotFoundError:
            print("portinternet.json 文件不存在")
            return

        # 查找所有 blocked 为 true 的端口号并调用 delete_port_entry 删除
        for port, data in portinternet_data.items():
            if data.get('blocked') is True:
                print(f"删除被阻止的端口 {port}")
                iptables.remove_iptables_rule(int(port))
                iptables.remove_iptables_blackrule(int(port))
                v2ray.removev2ray(int(port))
            else:
                print('没有需要删除的端口')

        internet.delete_blocked_ports()
        print('到期删除完毕')



# 每天检查是否为1月1日，并执行重置操作
def check_new_year_reset():
    current_time = datetime.now()
    print(current_time)
    if current_time.day == 1 or current_time.day == 30:
        reset_ports()


# 定时任务：每分钟执行一次检查过期端口的任务
schedule.every(1).minute.do(check_expired_ports)

# 定时任务：每天检查是否是1月1日
schedule.every().day.at("00:00").do(check_new_year_reset)


# 主程序循环，定时执行任务
def main():
    init_time_data()  # 初始化 time_data.json 文件
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
