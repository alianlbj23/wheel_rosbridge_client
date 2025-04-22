import roslibpy
import urwid

# ROS bridge 設定
ROS_BRIDGE_IP = "192.168.77.45"
ROS_BRIDGE_PORT = 9090

# 預設速度
SPEED_VALUE = 100.0

# 鍵盤對應的輪速命令
key_mappings = {
    "w": [SPEED_VALUE, SPEED_VALUE, SPEED_VALUE, SPEED_VALUE],
    "s": [-SPEED_VALUE, -SPEED_VALUE, -SPEED_VALUE, -SPEED_VALUE],
    "a": [-SPEED_VALUE, SPEED_VALUE, -SPEED_VALUE, SPEED_VALUE],
    "d": [SPEED_VALUE, -SPEED_VALUE, SPEED_VALUE, -SPEED_VALUE],
    "e": [-SPEED_VALUE, SPEED_VALUE, -SPEED_VALUE, SPEED_VALUE],
    "r": [SPEED_VALUE, -SPEED_VALUE, SPEED_VALUE, -SPEED_VALUE],
    "z": [0.0, 0.0, 0.0, 0.0],
}

# 建立 ROS bridge client
client = roslibpy.Ros(host=ROS_BRIDGE_IP, port=ROS_BRIDGE_PORT)
client.run()

if not client.is_connected:
    print("❌ Failed to connect to ROS bridge.")
    exit(1)

publisher = roslibpy.Topic(client, "/car_C_rear_wheel", "std_msgs/Float32MultiArray")
publisher.advertise()

# UI 顯示區塊
status_text = urwid.Text("Press keys (W/A/S/D/Q/E/Z) or ESC to quit", align="center")
wheel_status = urwid.Text("Current speeds: [0.0, 0.0, 0.0, 0.0]", align="center")
pile = urwid.Pile([status_text, urwid.Divider(), wheel_status])
fill = urwid.Filler(pile, valign="middle")


def publish_speeds(speeds):
    message = {"data": speeds}
    publisher.publish(roslibpy.Message(message))
    wheel_status.set_text(f"📤 Published speeds: {speeds}")


def handle_input(key):
    if isinstance(key, str):
        key = key.lower()
        if key in key_mappings:
            speeds = key_mappings[key]
            publish_speeds(speeds)
        elif key == "esc":
            raise urwid.ExitMainLoop()


def main():
    print(f"✅ Connected to ROS bridge at {ROS_BRIDGE_IP}:{ROS_BRIDGE_PORT}")
    urwid.MainLoop(fill, unhandled_input=handle_input).run()
    publisher.unadvertise()
    client.terminate()
    print("🔌 Disconnected from ROS bridge.")


if __name__ == "__main__":
    main()
