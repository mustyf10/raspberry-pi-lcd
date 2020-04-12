# Raspberry Pi 3b Status program with Clock
# Demo program for the I2C 16x2 Display from Ryanteck.uk
# Created by Matthew Timmons-Brown for The Raspberry Pi Guy YouTube channel

# Import necessary libraries for communication and display use
import lcddriver
import time
import datetime
import requests
import psutil

# Load the driver and set it to "display"
display = lcddriver.lcd()
emptyString = "                "

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

def getTime():
    currentTime = datetime.datetime.now()
    return currentTime.strftime("%a %d %b %-I:%M")

def printTime():
    display.lcd_display_string(getTime(), 1)

def getCpuLoad(): # Get CPU load as a percentage from psutil
    long_string(display, emptyString + "CPU Usage: " + str(psutil.cpu_count()), 2)

def getStatus():
    display.lcd_display_string("PiHole: " + str(pihole['status']).upper(), 2)

def getNoOfDnsQueriesToday(): # Get total number of DNS queries over the last 24hrs
    long_string(display, emptyString + "No. of Queries Today: " + str(pihole['dns_queries_today']), 2)

def getNoQueriesBlocked(): # Total no of queries blocked over the last 24hrs
    long_string(display, emptyString + "Blocked Today: " + str(pihole['ads_blocked_today']) + " (" + str(pihole['ads_percentage_today'])[:5] + "%)", 2)

try:
   print("Writing to LCD...")
   while True:
        pihole = requests.get("http://192.168.1.3/admin/api.php?summaryRaw").json()
        printTime() # Write the time to display
        getStatus() # Write status of PiHole
        time.sleep(2) # Hold screen
        display.lcd_clear()
        printTime() # Write the time to display
        getNoOfDnsQueriesToday()
        time.sleep(1) # Hold screen
        display.lcd_clear()
        printTime() # Write the time to display
        getNoQueriesBlocked()
        time.sleep(1) # Hold screen
        display.lcd_clear()

        # Program loops with different queries
    	
except KeyboardInterrupt: # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    print("Cleaning up!")
    display.lcd_clear()
    display.lcd_clear()
