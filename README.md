# OHM-to-influxdv
Get data from Open Hardware Monitor and put in influxdb

#Step1:
install Open Hardware Monitor on your windows
<link>https://openhardwaremonitor.org/</link>

in <B>option</B> -> <B>Remote Web Server</B> -> check <B>RUN</B>
edit OHM.py and set ip addres of you windows machin
set password and dbname of influxdb
add +x attribute to OHM.py and everySecond.sh file

run bash script with this commond
./everySecond.sh &
