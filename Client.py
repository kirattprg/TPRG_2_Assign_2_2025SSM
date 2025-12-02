"""
# Sachkerat Singh Matharoo
# 100996938
# 01-12-2025
# Assignment 2 Client 
"""

import socket
import json

host = "10.102.13.64"   # <-- replace with your Pi's IP
port = 5000

s = socket.socket()
s.connect((host, port))

data = s.recv(2048)
s.close()

# decode JSON
info = json.loads(data.decode("utf-8"))

print("\n==== Raspberry Pi System Status ====\n")
print("CPU Temperature (°C):", info["temperature_C"])
print("Core Voltage (V):", info["core_voltage_V"])
print("ARM Frequency (Hz):", info["arm_freq_Hz"])
print("Core Frequency (Hz):", info["core_freq_Hz"])
print("Throttle Status:", info["throttle_status"])
print("\n====================================\n")
