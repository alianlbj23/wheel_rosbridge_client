import roslibpy
import urwid
import argparse

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


def publish_speeds(publisher, speeds):
    message = {"data": speeds}
    publisher.publish(roslibpy.Message(message))
    wheel_status.set_text(f"📤 Published speeds: {speeds}")


def handle_input(key, publisher):
    if isinstance(key, str):
        key = key.lower()
        if key in key_mappings:
            speeds = key_mappings[key]
            publish_speeds(publisher, speeds)
        elif key == "esc":
            raise urwid.ExitMainLoop()


# UI 顯示區塊
status_text = urwid.Text("Press keys (W/A/S/D/Q/E/Z) or ESC to quit", align="center")
wheel_status = urwid.Text("Current speeds: [0.0, 0.0, 0.0, 0.0]", align="center")
pile = urwid.Pile([status_text, urwid.Divider(), wheel_status])
fill = urwid.Filler(pile, valign="middle")


def main():
    # 命令行參數解析
    parser = argparse.ArgumentParser(description="ROS Wheel Control Client")
    parser.add_argument("ip", help="ROS bridge IP address")
    parser.add_argument(
        "-p", "--port", type=int, default=9090, help="ROS bridge port (default: 9090)"
    )
    args = parser.parse_args()

    # 建立 ROS bridge client
    client = roslibpy.Ros(host=args.ip, port=args.port)
    client.run()

    if not client.is_connected:
        print(f"❌ Failed to connect to ROS bridge at {args.ip}:{args.port}")
        exit(1)

    publisher = roslibpy.Topic(client, "/wheel_speed", "std_msgs/Float32MultiArray")
    publisher.advertise()

    print(f"✅ Connected to ROS bridge at {args.ip}:{args.port}")
    urwid.MainLoop(fill, unhandled_input=lambda key: handle_input(key, publisher)).run()
    publisher.unadvertise()
    client.terminate()
    print("🔌 Disconnected from ROS bridge.")


if __name__ == "__main__":
    main()
