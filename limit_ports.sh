#!/bin/bash

# 端口范围变量，可以修改为所需的范围
START_PORT=20000
END_PORT=20100

# 限速参数（可以修改）
RATE="50mbit"  # 保证带宽
CEIL="50mbit"  # 最大带宽
DEV="eth0"     # 网口名称

# 删除已有的tc配置
echo "删除已有的tc配置..."
tc qdisc del dev $DEV root 2>/dev/null

# 添加根队列
echo "添加根队列..."
tc qdisc add dev $DEV root handle 1: htb

# 添加根分类
echo "设置根分类限速..."
tc class add dev $DEV parent 1: classid 1: htb rate $RATE ceil $CEIL

# 循环设置分类和iptables规则
echo "设置分类和iptables规则..."
for ((PORT=$START_PORT; PORT<=$END_PORT; PORT++)); do
  CLASSID="1:$((PORT - START_PORT + 2))"
  tc class add dev $DEV parent 1: classid $CLASSID htb rate $RATE ceil $CEIL
  iptables -t mangle -A POSTROUTING -p tcp --sport $PORT -j MARK --set-mark $((PORT - START_PORT + 2))
  tc filter add dev $DEV parent 1:0 protocol ip handle $((PORT - START_PORT + 2)) fw classid $CLASSID
done

echo "批量限速完成，范围：$START_PORT-$END_PORT，带宽限制：$RATE"
