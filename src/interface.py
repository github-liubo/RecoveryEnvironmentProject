import wmi


def get_windows_usb_devices():
    c = wmi.WMI()
    usb_devices = []

    # 查询Win32_USBControllerDevice关联类获取详细信息
    for usb_controller in c.Win32_USBController():
        for usb_device in usb_controller.associators(wmi_result_class="Win32_PnPEntity"):
            if usb_device.Status == "OK":  # 仅获取正常工作的设备
                usb_devices.append({
                    "name": usb_device.Name,
                    "status": usb_device.Status,
                    "device_id": usb_device.DeviceID
                })

    return usb_devices


if __name__ == "__main__":
    print("Windows USB设备列表:")
    for device in get_windows_usb_devices():
        print(f"{device['name']} - 状态: {device['status']}")