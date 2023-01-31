#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <pin number> <desired temperature>"
    exit 1
fi

pin=$1
desired_temp=$(($2*1000))

Kp=0.5*0.001

if ! test -d /sys/class/gpio/gpio$pin/; then
    echo $pin > /sys/class/gpio/export
    echo "out" > /sys/class/gpio/gpio$pin/direction
fi

trap 'echo $pin > /sys/class/gpio/unexport; exit' INT
echo "Starting heater control. Desired temperature: $desired_temp"

function heat_on {
    echo "heat on"
    echo 1 > /sys/class/gpio/gpio$pin/value
}

function heat_off {
    echo "heat off"
    echo 0 > /sys/class/gpio/gpio$pin/value
}

function max() {
    if echo "$1 > $2" | bc -q | grep -q 1; then
        echo $1
    else
        echo $2
    fi
}

heat_off

cooldown=0
timestep=2

while true
do
    current_temp=$(cat /sys/bus/w1/devices/28-*/w1_slave | grep t= | cut -d "=" -f 2)
    echo "Current temperature: $current_temp"
    echo $(date +%s) $current_temp >> /tmp/temperature.log
    error=$(($desired_temp-$current_temp))
    if [ "$error" -gt 0 ] && [ $cooldown -le 0 ] ; then
        factor=$(echo "$error * $Kp" | bc -q)
        sleep_time=$(printf "%.0f" $factor)
        heat_on
        sleep $(max $sleep_time 0.7)
        heat_off
        cooldown=8
    fi
    cooldown=$(($cooldown-$timestep))
    sleep $timestep
done
