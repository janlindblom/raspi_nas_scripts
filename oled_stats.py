# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-FileCopyrightText: 2022 Jan Lindblom for Namnløs
# SPDX-License-Identifier: MIT

import time
import subprocess
import board
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont

# Create the I2C interface.
i2c = board.I2C()

# Create the SSD1306 OLED class.
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c)

# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
width = disp.width
height = disp.height
image = Image.new("1", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)

# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

#font = ImageFont.load_default()
font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)
#font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 9)
#font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 9)

# Draws a 'progress bar' style horisontal meter.
def drawPBar(start, val):
    draw.rectangle((0, top + start, width - 1, top + start + 7), outline=1, fill=0)
    draw.rectangle((1, top + start + 1, (val / 100) * (width - 2), top + start + 6), outline=0, fill=1)

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    cmd = "hostname -I | cut -d' ' -f1"
    IP = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'cut -f 1 -d " " /proc/loadavg'
    CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
    MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "free -m | awk 'NR==2{printf \"%.0f\", $3*100/$2 }'"
    MemPercentage = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
    Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
    cmd = "vcgencmd measure_temp |cut -f 2 -d '='"
    Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

    draw.text((x, top + 0), "IP: " + IP, font=font, fill=128)
    draw.text((x, top + 9), "CPU load: " + CPU, font=font, fill=255)
    drawPBar(20, int(float(CPU) * 100))
    draw.text((x, top + 27), MemUsage, font=font, fill=255)
    drawPBar(37, int(MemPercentage))
    draw.text((x, top + 45), Disk, font=font, fill=255)
    draw.text((x, top + 54), "Temp: " + Temp, font=font, fill=255)

    disp.image(image)
    disp.show()
    time.sleep(1)

