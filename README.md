# 白噪声科技运维工具集

北辰数据中心B区日常运维脚本与工具。

## 包含内容

- `monitor_check.py` - 机房环境监控检查脚本
- `backup_verify.sh` - 备份完整性验证脚本
- `patrol_template.md` - 夜班巡检记录模板
- `network_diag.py` - 网络连通性诊断工具

## 使用说明

所有脚本均在运维工作站上运行，需使用运维账号执行。

### 监控检查
```bash
python monitor_check.py --zone B
```

### 备份验证
```bash
bash backup_verify.sh --date today
```

## 注意事项

- 夜班巡检请严格按照模板填写，不得遗漏任何摄像头检查项
- 发现异常请立即记录并上报值班主管
- 3号摄像头区域信号不稳定，巡检时请重点确认

## 联系方式

运维部内部沟通请使用企业微信。
外部技术支持：support@baizosheng.tech

---

*最后更新：2026年9月*
