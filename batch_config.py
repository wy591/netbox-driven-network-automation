import telnetlib
import time

# 待配置的设备 IP 列表
devices = ["192.168.14.20", "192.168.14.30"]

for host in devices:
    print(f"===== 配置 {host} =====")
    try:
        tn = telnetlib.Telnet(host, timeout=10)
        tn.read_until(b"Password:", timeout=5)
        tn.write(b"Huawei@123\n")
        time.sleep(2)

        tn.write(b"system-view\n")
        time.sleep(2)

        tn.write(b"vlan 100\n")
        time.sleep(2)
        tn.write(b"vlan 200\n")
        time.sleep(2)

        tn.write(b"return\n")
        time.sleep(1)
        tn.write(b"save\n")
        time.sleep(2)
        tn.write(b"y\n")
        time.sleep(2)

        print(f"{host} 配置完成！")
        tn.close()
    except Exception as e:
        print(f"{host} 配置失败: {e}")
