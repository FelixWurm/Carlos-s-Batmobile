from bluepy.btle import Scanner

scanner = Scanner()
devices = scanner.scan(20.0)

for device in devices:
    print(f"DEV={device.addr} TYPE={device.addrType}  RSSI={device.rssi}")
    device.getScanData()
