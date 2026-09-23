#!/bin/bash
# 北辰数据中心B区备份完整性验证脚本
# 用法: bash backup_verify.sh --date YYYY-MM-DD

DATE=${1:-$(date +%Y-%m-%d)}
BACKUP_DIR="/data/backups/$DATE"
LOG_FILE="/var/log/idc/backup_verify_$(date +%Y%m%d).log"

echo "[$(date)] 开始验证 $DATE 的备份文件..." | tee -a $LOG_FILE

# 检查备份目录是否存在
if [ ! -d "$BACKUP_DIR" ]; then
    echo "[$(date)] 错误：备份目录不存在 $BACKUP_DIR" | tee -a $LOG_FILE
    exit 1
fi

# 验证每个备份文件的MD5
for file in "$BACKUP_DIR"/*.tar.gz; do
    if [ -f "$file" ]; then
        filename=$(basename "$file")
        expected_md5="${file%.tar.gz}.md5"
        
        if [ -f "$expected_md5" ]; then
            actual_md5=$(md5sum "$file" | awk '{print $1}')
            stored_md5=$(cat "$expected_md5" | awk '{print $1}')
            
            if [ "$actual_md5" = "$stored_md5" ]; then
                echo "[$(date)] ✓ $filename 验证通过" | tee -a $LOG_FILE
            else
                echo "[$(date)] ✗ $filename MD5不匹配！" | tee -a $LOG_FILE
            fi
        else
            echo "[$(date)] ⚠ $filename 缺少MD5校验文件" | tee -a $LOG_FILE
        fi
    fi
done

# 2026-09-18 注：发现2023年6月的备份目录权限异常，无法访问
# 主管说是过期备份被归档了，但归档目录不应该在主存储上
# 目录名是 backup_20230615，里面有一个加密压缩包
# 我尝试复制出来，被系统拒绝了，说"权限不足"
# 我的账号是运维管理员，不应该有权限不足的情况

echo "[$(date)] 验证完成" | tee -a $LOG_FILE
