"""
# Sachkerat Singh Matharoo
# 100996938
# 01-12-2025
# Assignment 2 - Server File

"""

import socket
import os
import json

#  FUNCTIONS: Each retrieves one vcgencmd value from the Pi

def get_temp():
    """
    Reads the CPU temperature using vcgencmd.
    Example output from Pi:
        'temp=54.3'C'
    This function removes the text and returns:
        '54.3'
    """
    out = os.popen("vcgencmd measure_temp").readline()
    return out.replace("temp=", "").replace("'C", "").strip()


def get_voltage():
    """
    Reads the core voltage from the Pi.
    Example output:
        'volt=0.88V'
    This returns:
        '0.88'
    """
    out = os.popen("vcgencmd measure_volts").readline()
    return out.replace("volt=", "").replace("V", "").strip()


def get_freq_arm():
    """
    Reads the ARM (CPU) frequency of the Raspberry Pi.
    Example output:
        'clock(48)=1500000000'
    We split at '=' and return only:
        '1500000000'
    """
    out = os.popen("vcgencmd measure_clock arm").readline()
    return out.split("=")[1].strip()


def get_freq_core():
    """
    Reads the Core/GPU/VC4 clock frequency.
    Example:
        'clock(1)=500000000'
    Returns:
        '500000000'
    """
    out = os.popen("vcgencmd measure_clock core").readline()
    return out.split("=")[1].strip()


def get_throttle_status():
    """
    Reads the throttle status of the Raspberry Pi.
    This indicates under-voltage, frequency capping, throttling, etc.
    Example:
        'throttled=0x0'
    Returns:
        '0x0'   (meaning no throttling)
    """
    out = os.popen("vcgencmd get_throttled").readline()
    return out.replace("throttled=", "").strip()

#  SERVER SETUP

# Create a TCP socket for communication
s = socket.socket()

# Host is empty string: listen on ALL interfaces of the Pi (LAN/WLAN)
host = ""

# Port number for client connections
port = 5000

# Bind the socket to host and port
s.bind((host, port))

# Allow up to 5 pending client connections
s.listen(5)

print("Server running... waiting for client connections.")

#  MAIN SERVER LOOP
#  Accepts a client → sends JSON → closes connection

while True:
    # Wait for a client PC to connect
    c, addr = s.accept()
    print("Connection from:", addr)

    # Collect system data by calling each function
    data = {
        "temperature_C": get_temp(),
        "core_voltage_V": get_voltage(),
        "arm_freq_Hz": get_freq_arm(),
        "core_freq_Hz": get_freq_core(),
        "throttle_status": get_throttle_status()
    }

    # Convert Python dictionary → JSON string → bytes for sending
    json_bytes = bytes(json.dumps(data), "utf-8")

    # Send JSON data to the connected client
    c.send(json_bytes)

    # Close connection (required for clean shutdown)
    c.close()
