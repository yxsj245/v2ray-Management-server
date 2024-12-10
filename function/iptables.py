import subprocess

# 保存配置
def save_iptables():
    command = f"iptables-save > /etc/iptables/rules.v4"

    try:
        subprocess.run(command, shell=True, check=True)
        print(f"保存成功")
    except subprocess.CalledProcessError as e:
        print(f"添加阻止端口出错 {e}")

# 添加端口记录
def add_iptables_rule(port):
    command = f"iptables -A OUTPUT -p tcp --sport {port} -j ACCEPT"
    try:
        subprocess.run(command, shell=True, check=True)
        save_iptables()
        print(f"添加端口记录成功{port}")
    except subprocess.CalledProcessError as e:
        print(f"添加端口出错 {e}")

# 移除端口记录
def remove_iptables_rule(port):
    command = f"iptables -D OUTPUT -p tcp --sport {port} -j ACCEPT"
    try:
        subprocess.run(command, shell=True, check=True)
        save_iptables()
        print(f"移除端口记录成功{port}")
    except subprocess.CalledProcessError as e:
        print(f"移除端口记录出错 {e}")

# 添加阻止端口
def add_iptables_blackrule(port):
    command = f"iptables -A INPUT -p tcp --dport {port} -j DROP"

    try:
        subprocess.run(command, shell=True, check=True)
        save_iptables()
        print(f"添加阻止端口成功{port}")
    except subprocess.CalledProcessError as e:
        print(f"添加阻止端口出错 {e}")

# 移除阻止端口
def remove_iptables_blackrule(port):
    command = f"iptables -D INPUT -p tcp --dport {port} -j DROP"

    try:
        subprocess.run(command, shell=True, check=True)
        save_iptables()
        print(f"移除阻止端口成功{port}")
    except subprocess.CalledProcessError as e:
        print(f"移除阻止端口出错 {e}")


