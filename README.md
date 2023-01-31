## OpenBLab

<img src="assets/petri-monitor-sm.jpg" alt="photo" align="right">

Unleash the power of automation in your lab with this culture monitoring system! Using a Raspberry Pi camera and off-the-shelf components, the system makes it a breeze to track the growth of your cultures. Simply add your sample to the agar gel, set the temperature and snapshot frequency, press START and sit back. Monitor your progress remotely and watch your results soar!

<br clear="both"/>

## Requirements

Parts:

* SBC e.g. [Raspberry Pi](https://rpilocator.com/)
* [Peltier device](https://s.click.aliexpress.com/e/_DBggz5V) (5v or 12v)
* [Temperature sensor](https://s.click.aliexpress.com/e/_DmMl93Z) (DS18B20)
* [Camera](https://s.click.aliexpress.com/e/_DmQooUJ)
* [Power MOSFET](https://s.click.aliexpress.com/e/_DCYRkLv) (IRF540N)

If using a 12V peltier device, you will also need
* [12V power supply](https://s.click.aliexpress.com/e/_DePtWNZ) (about 8A)
* [buck converter](https://s.click.aliexpress.com/e/_DDBOrqR)

For the sample:
* [Agar plates](https://s.click.aliexpress.com/e/_DCe6UFd)

## Example UI

<img src="assets/screen1.png" width="600">

## Setup

Ensure 1-wire module is loaded on RPi:
 - add `dtoverlay=w1-gpio,gpiopin=14` line to /boot/config.txt
 - `sudo apt install bc`
 - reboot

Connect DS18B20 to RPi: 
| Pin on sensor | GPIO on Pi|
|---------------|-----------|
| Data          | GPIO 14   |
| Power         | 3.3v      |
| GND           | GND       |


##

Run API:

```
cd code/api 
pipenv install
pipenv run start:dev
```