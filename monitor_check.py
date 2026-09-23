#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北辰数据中心B区环境监控检查脚本
用于巡检时自动采集温湿度、电力、网络状态
"""

import subprocess
import json
import datetime
import os

# 监控点位配置
ZONE_B_CAMERAS = ["CAM-01", "CAM-02", "CAM-03", "CAM-04", "CAM-05", "CAM-06"]
THRESHOLD_TEMP = 28.0
THRESHOLD_HUMIDITY = 70.0

# TODO(limo): 3号摄像头夜间频繁丢帧，已上报但未修复
# 2026-09-18 23:47 CAM-03 再次出现信号中断，持续约12秒
# 2026-09-19 02:15 CAM-03 画面出现静止物体，无法识别
# 主管说可能是线路老化，让我别管

def check_temperature():
      """检查机房温度"""
      result = subprocess.run(["ipmitool", "sensor", "list"], capture_output=True, text=True)
      return result.stdout

def check_camera_status(camera_id):
      """检查摄像头在线状态"""
      try:
                result = subprocess.run(
                              ["ping", "-c", "1", "-W", "2", f"192.168.1.{100 + int(camera_id.split('-')[1])}"],
                              capture_output=True, text=True, timeout=5
                )
                return result.returncode == 0
except Exception:
        return False

def generate_report():
      """生成巡检报告"""
      report = {
          "timestamp": datetime.datetime.now().isoformat(),
          "zone": "B",
          "temperature": "normal",
          "cameras": {}
      }

    for cam in ZONE_B_CAMERAS:
              report["cameras"][cam] = "online" if check_camera_status(cam) else "offline"

    return report

# 2026-09-20 夜班记录
# CAM-03 在23:00-23:30之间三次离线
# 每次恢复后画面角度有轻微变化
# 我没有移动过摄像头
# 机房当时只有我一个人

def main():
      report = generate_report()
      print(json.dumps(report, indent=2, ensure_ascii=False))

    # 保存报告
      log_path = f"/var/log/idc/check_{datetime.date.today()}.json"
      with open(log_path, "w") as f:
                json.dump(report, f, ensure_ascii=False)

  if __name__ == "__main__":
        main()
    
