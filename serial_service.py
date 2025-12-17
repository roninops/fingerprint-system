import serial
import requests
import time

SERIAL_PORT = "/dev/ttyUSB0"
BAUDRATE = 57600

API_URL = "http://127.0.0.1:8000/access/{}"

def main():
    ser = serial.Serial(
        SERIAL_PORT,
        BAUDRATE,
        timeout=0.1   # 🔑 ikke-blokerende
    )

    print("Serial service started")

    buffer = ""

    while True:
        try:
            data = ser.read().decode(errors="ignore")
            if data:
                buffer += data

                if "FINGERPRINT_ID:" in buffer:
                    lines = buffer.splitlines()
                    for line in lines:
                        if line.startswith("FINGERPRINT_ID:"):
                            fid = int(line.split(":")[1])
                            print("Fingerprint ID:", fid)

                            r = requests.get(
                                API_URL.format(fid),
                                timeout=3
                            )
                            print("Server response:", r.json())

                    buffer = ""  # ryd buffer efter behandling

            time.sleep(0.05)

        except Exception as e:
            print("Error:", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
