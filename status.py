# -*- coding: utf-8 -*-
#!/usr/bin/python3

# Raspberry Pi 3b program to run on 16*2 LCD
# Created by Mustafa Fajandar for personal use

# Import necessary libraries for communication and display use
import lcddriver
import time
import datetime
import requests

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

def getTime(): # Get system time and return in my format day/date/month hh:mm
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%a %d %b %-I:%M")

def printTime(): # Print time to LCD
    display.lcd_display_string(getTime(), 1)

def getStatus(): # Get status of pi-hole (enabled/disabled)
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

def getBitcoinPrice(): # Print current bitcoin price from coindesk
    bitcoinPrice = str(round(float(coindesk['bpi']['GBP']['rate_float']), 2))
    display.lcd_display_string(("BTC/GBP:" + bitcoinPrice ), 2)

try:
    print("Writing to LCD...")
    while True:
        pihole = requests.get("http://192.168.1.3/admin/api.php?summaryRaw").json()
        rpimonitor = requests.get("http://192.168.1.3:8888/dynamic.json").json()
        coindesk = requests.get("https://api.coindesk.com/v1/bpi/currentprice/GBP.json").json()

        printTime() # Write the time to display
        getStatus() # Write status of PiHole
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        printUptime() # Write uptime of system
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getSocTemp() # Write Temperature of SoC
        time.sleep(3) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getPackageUpgrade() # Write amount of packages that need updating
        time.sleep(3) # Hold screen
        display.lcd_clear()
        
        printTime() # Write the time to display
        getNoOfDnsQueriesToday()
        time.sleep(1) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getNoQueriesBlocked()
        time.sleep(1) # Hold screen
        display.lcd_clear()

        printTime() # Write the time to display
        getBitcoinPrice() # Write price of bitcoin
        time.sleep(3) # Hold screen
        display.lcd_clear()
        
        # Program loops with different queries
 	
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()