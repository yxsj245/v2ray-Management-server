import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import json


class NodeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("节点管理")

        # 请求地址输入框
        self.url_label = ttk.Label(root, text="请求地址")
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.url_entry = ttk.Entry(root)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        self.url_entry.insert(0, "http://150.109.148.136:5000")  # 默认URL

        # 输入框
        self.port_label = ttk.Label(root, text="端口号")
        self.port_label.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.port_entry = ttk.Entry(root)
        self.port_entry.grid(row=1, column=1, padx=10, pady=10)

        self.time_label = ttk.Label(root, text="时间")
        self.time_label.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.time_entry = ttk.Entry(root)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10)

        self.internet_label = ttk.Label(root, text="流量")
        self.internet_label.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.internet_entry = ttk.Entry(root)
        self.internet_entry.grid(row=3, column=1, padx=10, pady=10)

        self.type_label = ttk.Label(root, text="类型")
        self.type_label.grid(row=4, column=0, padx=10, pady=10, sticky='w')

        # 类型选择框
        self.type_combo = ttk.Combobox(root, values=["updateinternet", "updatetime"])
        self.type_combo.grid(row=4, column=1, padx=10, pady=10)
        self.type_combo.set("updateinternet")  # 默认选择更新流量

        # 按钮
        self.add_button = ttk.Button(root, text="添加节点", command=self.add_node)
        self.add_button.grid(row=5, column=0, padx=10, pady=10)

        self.update_button = ttk.Button(root, text="更新节点", command=self.update_node)
        self.update_button.grid(row=5, column=1, padx=10, pady=10)

        self.remove_button = ttk.Button(root, text="删除节点", command=self.remove_node)
        self.remove_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # 返回信息显示框
        self.response_label = ttk.Label(root, text="返回信息")
        self.response_label.grid(row=7, column=0, padx=10, pady=10, sticky='w')

        self.response_text = tk.Text(root, height=6, width=50)
        self.response_text.grid(row=7, column=1, padx=10, pady=10)
        self.response_text.config(state=tk.DISABLED)  # 使文本框不可编辑

    def get_url(self):
        # 获取用户输入的 URL
        return self.url_entry.get()

    def display_response(self, response_text):
        """在文本框中显示返回信息"""
        self.response_text.config(state=tk.NORMAL)  # 允许编辑文本框
        self.response_text.delete(1.0, tk.END)  # 清空文本框内容
        self.response_text.insert(tk.END, response_text)  # 插入返回信息
        self.response_text.config(state=tk.DISABLED)  # 禁止编辑文本框

    def add_node(self):
        url = self.get_url()

        try:
            port = int(self.port_entry.get())  # 确保端口为整数
            internet = int(self.internet_entry.get())  # 确保流量为整数
        except ValueError:
            messagebox.showerror("错误", "端口号和流量必须为整数")
            return

        time = self.time_entry.get()

        payload = json.dumps({
            "port": port,
            "time": time,
            "internet": internet
        })

        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        try:
            response = requests.post(f"{url}/add/node", headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            self.display_response(response.text)  # 显示返回的文本
            messagebox.showinfo("成功", "节点添加成功")
        except requests.exceptions.RequestException as e:
            self.display_response(str(e))  # 显示错误信息
            messagebox.showerror("错误", f"请求失败: {e}")

    def update_node(self):
        url = self.get_url()

        try:
            port = int(self.port_entry.get())  # 确保端口为整数
            internet = int(self.internet_entry.get())  # 确保流量为整数
        except ValueError:
            messagebox.showerror("错误", "端口号和流量必须为整数")
            return

        time = self.time_entry.get()
        node_type = self.type_combo.get()  # 获取选择的类型

        if node_type not in ['updateinternet', 'updatetime']:
            messagebox.showerror("错误", "类型无效，请选择 'updateinternet' 或 'updatetime'")
            return

        payload = json.dumps({
            "port": port,
            "time": time,
            "internet": internet,
            "type": node_type
        })

        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        try:
            response = requests.post(f"{url}/update/node", headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            self.display_response(response.text)  # 显示返回的文本
            messagebox.showinfo("成功", "节点更新成功")
        except requests.exceptions.RequestException as e:
            self.display_response(str(e))  # 显示错误信息
            messagebox.showerror("错误", f"请求失败: {e}")

    def remove_node(self):
        url = self.get_url()

        try:
            port = int(self.port_entry.get())  # 确保端口为整数
        except ValueError:
            messagebox.showerror("错误", "端口号必须为整数")
            return

        payload = json.dumps({
            "port": port
        })

        headers = {
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }

        try:
            response = requests.post(f"{url}/remove/node", headers=headers, data=payload)
            response.raise_for_status()  # 检查请求是否成功
            self.display_response(response.text)  # 显示返回的文本
            messagebox.showinfo("成功", "节点删除成功")
        except requests.exceptions.RequestException as e:
            self.display_response(str(e))  # 显示错误信息
            messagebox.showerror("错误", f"请求失败: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NodeManagerApp(root)
    root.mainloop()
