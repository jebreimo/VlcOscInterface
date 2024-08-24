# -*- coding: UTF-8 -*-
# ===========================================================================
# Copyright © 2024 Jan Erik Breimo. All rights reserved.
# Created by Jan Erik Breimo on 2024-08-23.
#
# This file is distributed under the BSD License.
# License text is included with the source distribution.
# ===========================================================================
import argparse
import requests
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


class VlcClient:
    def __init__(self, url, pwd):
        self.url = url
        self.pwd = pwd

    def send_command(self, command):
        try:
            auth = ("", self.pwd) if self.pwd else None
            url = f"{self.url}/requests/status.xml?{command}"
            print(url)
            response = requests.get(url, auth=auth, timeout=0.5)
            print(response)
        except requests.exceptions.RequestException as e:
            print(f"Failed to send command: {e}")


# def send_command(command):
#     url = f"http://raspberrypi:8080/requests/status.xml?{command}"
#     print(url)
#     try:
#         response = requests.get(url, auth=("", "mam6tmoh"), timeout=0.1)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print(f"Failed to send command: {e}")


commands = {
    "play": ("pl_play", lambda a: f"id={a[0]}" if a else ""),
    "pause": ("pl_pause", None),
    "stop": ("pl_stop", None),
    "seek": ("seek", lambda a: f"val={a[0]}"),
    "volume": ("volume", lambda a: f"val={a[0]}"),
    "fullscreen": ("fullscreen", None),
}


class OscMessageHandler:
    def __init__(self, vlc_clients):
        assert len(vlc_clients) != 0
        self.vlc_clients = vlc_clients

    def parse_address(self, address: str):
        parts = [p for p in address.split("/") if p]
        if len(parts) == 2:
            return self.vlc_clients[int(parts[0])], parts[1]
        raise ValueError(f"Invalid address: {address}")

    def handle_message(self, addr, *values):
        client, command = self.parse_address(addr)
        if command not in commands:
            print(f"Unknown command: {addr}")
            return
        command, arg_func = commands[command]
        arg = arg_func(values) if arg_func else ""
        client.send_command(f"command={command}&{arg}" if arg
                            else f"command={command}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
                        help="The ip to listen on for OSC messages")
    parser.add_argument("--port", type=int, default=5005,
                        help="The port to listen on for OSC messages")
    parser.add_argument("--vlc", default=[],
                        action="append",
                        help="The URL of the VLC web interface")
    parser.add_argument("--pwd", action="append", default=[],
                        help="The password for the VLC web interfaces. If there"
                             " are multiple interfaces with different"
                             " passwords, provide one password option for each"
                             " interface. One option is sufficient if they all"
                             " have the same password.")
    args = parser.parse_args()

    if not args.vlc:
        args.vlc = ["http://localhost:8080"]

    dispatcher = Dispatcher()
    vlc_clients = []
    for i, url in enumerate(args.vlc):
        pwd = args.pwd[min(i, len(args.pwd) - 1)] if args.pwd else None
        vlc_clients.append(VlcClient(url, pwd))

    handler = OscMessageHandler(vlc_clients)
    for i, client in enumerate(vlc_clients):
        print(f"Mapping /{i}/* to {client.url}")
        dispatcher.map(f"/{i}/*", handler.handle_message)
    # for command in commands:
    #     dispatcher.map(command, handler.handle_message)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()


if __name__ == "__main__":
    main()