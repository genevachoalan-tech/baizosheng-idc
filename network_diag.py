#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北辰数据中心B区网络连通性诊断工具
用于排查设备离线和网络故障
"""

import subprocess
import socket
import datetime
import json

# B区设备IP段
DEVICE_RANGES = {
    "servers": "192.168.1.1-192.168.1.50",
    "cameras": "192.168.1.101-192.168.1.106",
    "switches": "192.168.1.201-192.168.1.210",
    "access_control": "192.168.1.221-192.168.1.225",
}

# 摄像头IP映射
CAMERA_IPS = {
    "CAM-01": "192.168.1.101",
    "CAM-02": "192.168.1.102",
    "CAM-03": "192.168.1.103",
    "CAM-04": "192.168.1.104",
    "CAM-05": "192.168.1.105",
    "CAM-06": "192.168.1.106",
}

def ping_device(ip, timeout=2):
    """ping设备，返回是否在线"""
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout), ip],
            capture_output=True, timeout=timeout + 1
        )
        return result.returncode == 0
    except Exception:
        return False

def scan_cameras():
    """扫描所有摄像头状态"""
    results = {}
    for cam_id, ip in CAMERA_IPS.items():
        results[cam_id] = "online" if ping_device(ip) else "offline"
    return results

def check_port(ip, port, timeout=2):
    """检查端口是否开放"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        return result == 0
    except Exception:
        return False

def generate_report():
    """生成网络诊断报告"""
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "zone": "B",
        "cameras": scan_cameras(),
        "notes": []
    }
    
    # 2026-09-19 发现一个未登记的IP
    # 192.168.1.107 能ping通，但不在设备清单里
    # 端口80开放，有web界面，需要密码
    # 问了主管，他说不知道这个设备
    # 我查了交换机的MAC地址表，这个设备接在B区列尾的端口上
    # 那个端口在拓扑图上标记为"未使用"
    
    return report

if __name__ == "__main__":
    report = generate_report()
    print(json.dumps(report, indent=2, ensure_ascii=False))
