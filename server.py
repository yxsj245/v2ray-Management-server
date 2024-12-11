from flask import Flask, request, jsonify, abort

import function.v2ray as v2ray
import function.internet as internets
import function.iptables as iptables

# 设置关键地址的校验
apikey = 'vcvQW3SIwqgoSWCyUwq7cokt0sMLyiCd'

# 创建 Flask 应用
app = Flask(__name__)

@app.before_request
def validate_request():
    # 检查请求方法是否有效
    valid_methods = {"GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}
    if request.method not in valid_methods:
        abort(400, description="Invalid HTTP method.")

    # 检查请求行是否符合 HTTP 标准
    if not request.url or not request.url.startswith("http"):
        abort(400, description="Invalid HTTP request line.")

# 新增梯子
@app.route('/add/node', methods=['POST'])
def receive_data():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    if not data:
        return jsonify(error="请求内容有误"), 400

    port = data.get('port')
    time = data.get('time')
    internet = data.get('internet')
    apikeyverify = data.get('apikey')
    if apikeyverify == apikey:
        # 开通v2ray
        vmess = v2ray.addV2ray(port)
        # 创建防火墙
        iptables.add_iptables_rule(port)
        # 增加端口记录
        internets.add_port_to_json(port)
        # 设置到期时间
        internets.set_expiration_time(port,time)
        # 设置预设流量
        internets.set_preset_traffic(port,internet)
        return jsonify(message=vmess),200
    else:
        return jsonify(error="接口密钥错误"), 405

# 更新梯子信息
@app.route('/update/node', methods=['POST'])
def receive_data_2():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    if not data:
        return jsonify(error="请求内容有误"), 400

    port = data.get('port')
    time = data.get('time')
    internet = data.get('internet')
    xuanze = data.get('type')
    apikeyverify = data.get('apikey')

    if apikeyverify == apikey:
        if xuanze == 'updatetime':
            iptables.remove_iptables_blackrule(port)
            internets.update_expiration_time(port, time)
            return jsonify(message=f"到期时间更新成功"), 200
        if xuanze == 'updateinternet':
            iptables.remove_iptables_blackrule(port)
            internets.update_preset_traffic(port, internet)
            return jsonify(message=f"流量更新成功"), 200
        return jsonify(error="未找到的操作类型"), 405
    else:
        return jsonify(error="接口密钥错误"), 405

# 删除梯子
@app.route('/remove/node', methods=['POST'])
def receive_data_3():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    if not data:
        return jsonify(error="请求内容有误"), 400

    port = data.get('port')
    apikeyverify = data.get('apikey')
    
    if apikeyverify == apikey:
        v2ray.removev2ray(port)
        internets.delete_port_entry(port)
        iptables.remove_iptables_rule(port)
        iptables.remove_iptables_blackrule(port)
        return jsonify(message=f"删除成功"), 200
    else:
        return jsonify(error="接口密钥错误"), 405

# 查看梯子
@app.route('/check/node', methods=['POST'])
def receive_data_4():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    if not data:
        return jsonify(error="请求内容有误"), 400

    port = data.get('port')
    apikeyverify = data.get('apikey')
    
    if apikeyverify == apikey:
        parms = v2ray.checkv2ray(port)
        return jsonify(message=parms), 200
    else:
        return jsonify(error="接口密钥错误"), 405

# 查看端口信息
@app.route('/check/port', methods=['POST'])
def receive_data_5():
    data = request.get_json()  # 获取 POST 请求中的 JSON 数据
    if not data:
        return jsonify(error="请求内容有误"), 400

    port = data.get('port')

    expiration_date = internets.Expiration_date(port)
    restrict_traffic = internets.Restrict_traffic(port)
    flow_information = internets.flow_information(port)

    data = {
        'expiration_date':expiration_date,
        'restrict_traffic':restrict_traffic,
        'flow_information':flow_information
    }
    return jsonify(data),200


if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
