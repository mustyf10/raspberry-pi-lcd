# -*- coding: utf-8 -*-
#!/usr/bin/python

# Raspberry Pi 3b program to run on 16*2 LCD
# Created by Mustafa Fajandar for personal use

# Import necessary libraries for communication and display use
import lcddriver
import time
import datetime
import requests
import subprocess

# Load the driver and set it to "display"
display = lcddriver.lcd()
emptyString = "                "
degrees = chr(223) + "C" # Special character and C for degrees celcius

def long_string(display, text = '', num_line = 1, num_cols = 16):
		"""
		Parameters: (driver, string to print, number of line to print, number of columns of your display)
		Return: This function send to display your scrolling string.
		"""
		if(len(text) > num_cols):
			display.lcd_display_string(text[:num_cols],num_line)
			time.sleep(1)
			for i in range(len(text) - num_cols + 1):
				text_to_print = text[i:i+num_cols]
				display.lcd_display_string(text_to_print,num_line)
				time.sleep(0.4)
			time.sleep(1)
		else:
			display.lcd_display_string(text,num_line)

def getCmdOutput(cmd): # Function to run CLI commands
    out = subprocess.Popen(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)

    stdout, stderr = out.communicate()

    return stdout.decode("utf-8")

def getHostname(): # Get hostname and username
    whoami = "whoami"
    hostname = "hostname"

    username = getCmdOutput(whoami).replace("\n", "")
    device = getCmdOutput(hostname).replace("\n", "")
    return username + "@" + device

def getLocalIp(): # Get local IP raspberry pi is running on
    localip = "hostname -I"
    ip = getCmdOutput(localip).replace("\n", "")
    return ip

def printHostname(): # Print hostname to screen
    display.lcd_display_string(getHostname(), 1)

def printLocalIp(): # Print local IP to screen
    display.lcd_display_string(getLocalIp(), 2)

def getFreeDiskSpace(): # Get available disk space on /dev/sda1 in Gb with %
    command1 = "df -h | grep -E '^/dev/sda1' | awk '{ print $4 }'"
    command2 = "df -h | grep -E '^/dev/sda1' | awk '{ print $5 }'"

    freeSpace = getCmdOutput(command1).replace("\n", "")
    percentage = getCmdOutput(command2).replace("\n", "")

    return freeSpace + "b (" + percentage + " used)"

def printFreeDiskSpace(): # Print available disk space on /dev/sda1
    long_string(display, emptyString + "Free disk space: " + getFreeDiskSpace(), 2)


def getTime(): # Get system time and return in my format day/date/month hh:mm
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%a %d %b %-I:%M")

def printTime(): # Print time to LCD
    display.lcd_display_string(getTime(), 1)

def getPiholeStatus(): # Get status of pi-hole (enabled/disabled)
    display.lcd_display_string("PiHole: " + str(pihole['status']).upper(), 2)

def getNoOfDnsQueriesToday(): # Get total number of DNS queries over the last 24hrs
    long_string(display, emptyString + "No. of Queries Today: " + str(pihole['dns_queries_today']), 2)

def getNoQueriesBlocked(): # Total no of queries blocked over the last 24hrs
    long_string(display, emptyString + "Blocked Today: " + str(pihole['ads_blocked_today']) + " (" + str(pihole['ads_percentage_today'])[:5] + "%)", 2)

def getSocTemp(): # Get temperature of SoC in degrees celcius
    display.lcd_display_string("SoC Temp: " + str(rpimonitor['soc_temp'][:4]) + degrees, 2)

def getUptime(): # Get uptime in seconds and convert to days/hrs/mins
    upTime = round(float(rpimonitor['uptime']), 0)
    convertedTime = str(datetime.timedelta(seconds=upTime))
    return convertedTime

def printUptime(): # Print uptime using long string to scroll text
    long_string(display, "Uptime: " + getUptime(), 2)

def getPackageUpgrade(): # Print how many packages need upgrading
    display.lcd_display_string(str(rpimonitor['upgrade']), 2)

def getBitcoinPrice(): # Print current bitcoin price from coinbase
    bitcoinPrice = str(round(float(coinbase['data']['amount']), 2))
    display.lcd_display_string(("BTC/GBP:" + bitcoinPrice ), 2)

def getNodeStatus(): # Get online status of bitcoin node
    status = bitnode['success']
    if (status == True):
        display.lcd_display_string("Bitnode: ONLINE", 2)
    else:
        display.lcd_display_string("Bitnode: OFFLINE", 2)
    
try:
    print("Writing to LCD...")
    while True:
        pihole = requests.get("http://192.168.1.3/admin/api.php?summaryRaw").json()
        rpimonitor = requests.get("http://192.168.1.3:8888/dynamic.json").json()
        coinbase = requests.get("https://api.coinbase.com/v2/prices/BTC-GBP/spot").json()
        bitnode = requests.get("https://bitnodes.io/api/v1/nodes/me-8333/").json()

        printHostname() # Write hostname to display
        printLocalIp() # Write local IP address to display
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        printUptime() # Write uptime of system
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getNodeStatus() # Write status of Bitnode
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getPiholeStatus() # Write status of PiHole
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getSocTemp() # Write Temperature of SoC
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        printFreeDiskSpace() # Write amount of disk space left on /dev/sda1
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getPackageUpgrade() # Write amount of packages that need updating
        time.sleep(2) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getNoOfDnsQueriesToday()
        time.sleep(2) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getNoQueriesBlocked()
        time.sleep(2) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getBitcoinPrice() # Write price of bitcoin
        time.sleep(3) # Hold screen
        display.lcd_clear()

        # Program loops with different queries

except (KeyboardInterrupt): # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
finally:
    display.lcd_clear()