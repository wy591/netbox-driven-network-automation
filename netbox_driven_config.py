import pynetbox
import telnetlib
import time

# 1. 连接 NetBox
NETBOX_URL = "http://192.168.14.130:8000"
NETBOX_TOKEN = "your_netbox_token_here"   # ⚠️ 替换成你自己的 Token

nb = pynetbox.api(NETBOX_URL, token=NETBOX_TOKEN)

# 2. 从 NetBox 读取 VLAN 列表
vlans = [v.vid for v in nb.ipam.vlans.all()]
print(f"从 NetBox 读取到 VLAN 列表: {vlans}")

# 3. 从 NetBox 读取设备清单
devices = list(nb.dcim.devices.filter(role="core-switch"))
print(f"从 NetBox 读取到设备: {[d.name for d in devices]}")

# 4. 逐台设备推送 VLAN 配置
for dev in devices:
    print(f"\n正在处理设备: {dev.name}")

    try:
        primary_ip = dev.primary_ip4
        if primary_ip is None:
            print(f"⚠️ 跳过 {dev.name}：没有配置主 IP")
            continue
        ip = str(primary_ip).split("/")[0]
        print(f"  -> 主 IP: {ip}")
    except Exception as e:
        print(f"  ❌ 获取 {dev.name} 的主 IP 失败: {e}")
        continue

    print(f"===== 正在配置 {dev.name} ({ip}) =====")

    try:
        tn = telnetlib.Telnet(ip, timeout=10)
        print("  -> Telnet 连接成功")
        tn.read_until(b"Password:", timeout=5)
        tn.write(b"Huawei@123\n")
        time.sleep(2)

        tn.write(b"system-view\n")
        time.sleep(2)

        for vlan in vlans:
            tn.write(f"vlan {vlan}\n".encode())
            time.sleep(1)

        tn.write(b"return\n")
        time.sleep(1)
        tn.write(b"save\n")
        time.sleep(2)
        tn.write(b"y\n")
        time.sleep(2)

        tn.close()
        print(f"  ✅ {dev.name} 配置完成")

        try:
            dev.custom_fields["deploy_status"] = "Deployed"
            dev.save()
            print(f"  ✅ NetBox 状态已回写")
        except Exception as cb_err:
            print(f"  ⚠️ 回写 NetBox 状态失败: {cb_err}")

    except Exception as e:
        print(f"  ❌ {dev.name} 配置失败: {e}")
