import re
from datetime import datetime

def parse_time(time_str):
    dt = datetime.strptime(time_str, "%H:%M:%S.%f")
    return int((dt.hour * 3600 + dt.minute * 60 + dt.second) * 1000000 + dt.microsecond)

def convert_log_to_vcd(log_path="renode.log", vcd_path="output.vcd"):
    with open(log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    events = []
    base_time = None

    for line in lines:
        time_match = re.search(r'\[(\d{2}:\d{2}:\d{2}\.\d{4})\]', line)
        if not time_match:
            continue
            
        us = parse_time(time_match.group(1))
        if base_time is None:
            base_time = us
        rel_time = us - base_time

        if "gpioPortA" in line and "0x18" in line:
            if "value 0x20" in line and "value 0x200000" not in line:
                events.append((rel_time, "PA5_STROBE", 1))
            elif "value 0x200000" in line:
                events.append((rel_time, "PA5_STROBE", 0))

        elif "gpioPortB" in line and "0x18" in line:
            if "value 0x10000000" in line:
                events.append((rel_time, "PB12_CS", 0))
            elif "value 0x1000" in line:
                events.append((rel_time, "PB12_CS", 1))

        elif "spi2" in line and "Data" in line:
            val_match = re.search(r'value (0x[0-9A-Fa-f]+)|returned (0x[0-9A-Fa-f]+)', line)
            if val_match:
                hex_val = val_match.group(1) or val_match.group(2)
                events.append((rel_time, "SPI2_DATA", int(hex_val, 16)))

        elif "timer3" in line and "CaptureOrCompare" in line:
            val_match = re.search(r'value (0x[0-9A-Fa-f]+)', line)
            if val_match:
                val = int(val_match.group(1), 16)
                if "34 (CaptureOrCompare1)" in line:
                    events.append((rel_time, "SERVO_AZ_PWM", val))
                elif "38 (CaptureOrCompare2)" in line:
                    events.append((rel_time, "SERVO_EL_PWM", val))

    vcd_events = []
    az_pulse = 1000 
    el_pulse = 2000 
    last_t = 0

    for time, sig, val in events:
        last_t = max(last_t, time)
        if sig == "PA5_STROBE":
            vcd_events.append((time, "!", val))
        elif sig == "PB12_CS":
            vcd_events.append((time, '"', val))
        elif sig == "SPI2_DATA":
            t_curr = time
            for bit_idx in range(7, -1, -1):
                bit_val = (val >> bit_idx) & 1
                vcd_events.append((t_curr, "$", bit_val))      
                vcd_events.append((t_curr + 2, "#", 1))        
                vcd_events.append((t_curr + 5, "#", 0))        
                t_curr += 10
        elif sig == "SERVO_AZ_PWM":
            az_pulse = val if val > 0 else 1000
        elif sig == "SERVO_EL_PWM":
            el_pulse = val if val > 0 else 2000

    pwm_start = last_t + 2000
    for i in range(5):
        t_p = pwm_start + i * 20000
        vcd_events.append((t_p, "%", 1))
        vcd_events.append((t_p, "&", 1))
        vcd_events.append((t_p + az_pulse, "%", 0))
        vcd_events.append((t_p + el_pulse, "&", 0))

    vcd_events.sort(key=lambda x: x[0])

    with open(vcd_path, "w", encoding="utf-8") as vcd:
        vcd.write("$date Today $end\n$version Renode 1-Bit Logic VCD $end\n$timescale 1us $end\n")
        vcd.write("$scope module top $end\n")
        vcd.write("$var wire 1 ! PA5_ADC_STROBE $end\n")
        vcd.write("$var wire 1 \" PB12_FLASH_CS $end\n")
        vcd.write("$var wire 1 # SPI2_SCK $end\n")
        vcd.write("$var wire 1 $ SPI2_MOSI $end\n")
        vcd.write("$var wire 1 % SERVO_AZ_PWM $end\n")
        vcd.write("$var wire 1 & SERVO_EL_PWM $end\n")
        vcd.write("$upscope $end\n$enddefinitions $end\n")

        vcd.write("#0\n0!\n1\"\n0#\n0$\n0%\n0&\n")

        for time, sig, val in vcd_events:
            vcd.write(f"#{time}\n{val}{sig}\n")

    print(f"Згенеровано {vcd_path} з 6 логічними каналами!")

if __name__ == "__main__":
    convert_log_to_vcd()