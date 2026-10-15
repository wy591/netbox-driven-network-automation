import subprocess
import time

# 设备列表
devices = {
    "CE1": "192.168.14.20",
    "CE2": "192.168.14.30",
    "AR":  "192.168.14.40"
}

print(f"监控设备列表: {devices}")
print("=" * 50)

# 定时检测循环
while True:
    print(f"\n===== 监控检查 {time.strftime('%Y-%m-%d %H:%M:%S')} =====")
    for name, ip in devices.items():
        result = subprocess.run(
            ["ping", "-c", "2", "-W", "2", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        if result.returncode == 0:
            print(f"✅ {name} ({ip}) 正常")
        else:
            print(f"❌ {name} ({ip}) 异常！请立即检查！")
    time.sleep(30)
