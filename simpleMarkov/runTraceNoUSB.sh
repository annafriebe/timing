echo  performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
echo  performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor
echo  performance > /sys/devices/system/cpu/cpu2/cpufreq/scaling_governor
echo  performance > /sys/devices/system/cpu/cpu3/cpufreq/scaling_governor

echo '1-1' | tee /sys/bus/usb/drivers/usb/unbind

taskset -c 1 trace-cmd record -e sched -o trace1.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace2.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace3.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace4.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace5.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace6.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace7.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace8.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace9.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace10.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace11.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace12.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace13.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace14.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace15.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace16.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace17.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace18.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace19.dat taskset -c 3 ./simpleMarkovPeriodic
taskset -c 1 trace-cmd record -e sched -o trace20.dat taskset -c 3 ./simpleMarkovPeriodic

echo '1-1' | tee /sys/bus/usb/drivers/usb/bind

