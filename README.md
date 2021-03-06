# Raspberry Pi LCD

This project is a small python file to send to my raspberry pi and run as a script upon boot in order to read the output of various information running on the pi on a 16\*2 LCD.

I've started off by printing the time and information from Pi-Hole, including the number of queries and total number which are blocked.
Implemented the use of RPi Monitor, getting stats such as SoC temperature and uptime.

Added latest bitcoin spot price using the Coinbase API.

# Installation

I used [this youtube video](https://www.youtube.com/watch?v=3XLjVChVgec) to install my LCD and [this youtube video](https://www.youtube.com/watch?v=49RkQeiVTGU) to learn about the scrolling text.

```bash
pip install RPLCD
```

Use this command to install 16\*2 LCD libraries.

Visit https://github.com/XavierBerger/RPi-Monitor to install RPi-Monitor.

# Contributing

Pull requests are welcome. Any changes or improvements I can make in the code are also welcome, please raise an issue for this.

# License

[GPLv3](https://github.com/mustyf10/raspberry-pi-lcd/blob/master/LICENSE)
