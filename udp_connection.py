import socket
import struct


class UDPConnection:

    def __init__(self):
        try:
            self.target_address = "127.0.0.1"

            # Create sender socket (port 7500)
            self.sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sender_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Create receiver socket (port 7501)
            self.receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.receiver_socket.bind(("", 7501))

            # 10ms timeout (Java setSoTimeout(10))
            self.receiver_socket.settimeout(0.01)

        except Exception as e:
            print("Initialization failed:", e)

    def send_to(self, value):
        try:
            # Pack integer into 4 bytes 
            data = value.encode()
            self.sender_socket.sendto(data, (self.target_address, 7500))
        except Exception as e:
            print("Send error:", e)

    def recv_from(self):
        try:
            data, _ = self.receiver_socket.recvfrom(4096)
            return data.decode(errors='ignore')
        except socket.timeout:
            # Normal behavior (non-blocking style)
            return None
        except Exception as e:
            print("Receive error:", e)
            return None

    def set_network_address(self, ip_address):
        try:
            socket.inet_aton(ip_address)  # Validate IP
            self.target_address = ip_address
        except socket.error:
            print("Invalid IP.")