#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <pin number> <desired temperature>"
    exit 1
fi

pin=$1
desired_temp=$(($2*1000))

if ! test -d /sys/class/gpio/gpio$pin/; then
    echo $pin > /sys/class/gpio/export
    echo "out" > /sys/class/gpio/gpio$pin/direction
fi

trap 'echo $pin > /sys/class/gpio/unexport; exit' INT

echo "Starting heater control. Desired temperature: $desired_temp"

while true
do
    current_temp=$(cat /sys/bus/w1/devices/28-*/w1_slave | grep t= | cut -d "=" -f 2)
    echo "Current temperature: $current_temp"
    if [ "$current_temp" -lt "$desired_temp" ]; then
        echo "heat on"
        echo 1 > /sys/class/gpio/gpio$pin/value
    else
        echo "heat off"
        echo 0 > /sys/class/gpio/gpio$pin/value
    fi
    sleep 1
done
