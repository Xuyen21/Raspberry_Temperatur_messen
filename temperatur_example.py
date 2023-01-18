'''
******************************************************************************
  * @file    Temperature Humidity Sensor.py
  * @author  Waveshare Team
  * @version
  * @date    2021-02-08
  * @brief   Temperature Humidity Sensor
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, WAVESHARE SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  ******************************************************************************
'''

from machine import Pin
import utime

'''
DHT11 single-bus protocol
First, your MCU pulls the bus down by about 20ms
The MCU then releases the bus, and the bus is pulled up in 1,2uS due to the pull-up resistor
DHT11 has a response time, which is usually between 2 and 40μs
DHT11 responds by first pulling the bus down about 80μs and then pulling it up about 80μs
When the response time of DHT11 is completed, the data will be sent. First, pull the bus down about 50μs and then pull the bus up
If the high level duration of the bus is 20~30us, then the data sent is 0
If the high level duration of the bus is about 70μs, the data sent this time is 1
'''

DHT11 = Pin(15, Pin.OUT, Pin.PULL_DOWN)
DHT11(1)


# Send the start signal
def DHT11_Rst():
    global DHT11
    DHT11 = Pin(15, Pin.OUT, Pin.PULL_DOWN)
    DHT11(0)
    utime.sleep_ms(20)
    DHT11(1)
    DHT11 = Pin(15, Pin.IN, Pin.PULL_DOWN)


# Wait for DHT11 response
def DHT11_Check():
    retry = 0
    while (DHT11.value() == 1) & (retry < 100):
        retry = retry + 1
    if (retry > 99):
        return 1;
    else:
        retry = 0
    while (DHT11.value() == 0) & (retry < 100):
        retry = retry + 1
    if (retry > 99):
        return 1
    return 0


# Read DHT11 data
def DHT11_Read():
    buf = [0, 0, 0, 0, 0]
    retry = 0
    DHT11_Rst()
    if DHT11_Check() == 0:
        j = 0
        while j < 5:
            i = 0
            while i < 8:

                while (DHT11.value() == 1):
                    retry = retry + 1

                while (DHT11.value() == 0):
                    retry = retry + 1

                # Because the sleep_us() delay is not accurate, the call statement delay is used here
                for o in range(1):
                    retry = 0
                i = i + 1
                retry = 0

                buf[j] = buf[j] << 1
                buf[j] = buf[j] | DHT11.value()
            j = j + 1
        if ((buf[0] + buf[1] + buf[2] + buf[3]) == buf[4]):
            humidity = buf[0] + buf[1] / 10
            temperature = buf[2] + buf[3] / 10
            return temperature, humidity
    else:
        return None, None
    return None, None


while True:
    temperature, humidity = DHT11_Read()
    if temperature is None:
        #         temperature = 0
        print(" Transport Error ")
    else:
        print("{:3.1f}'C  {:3.1f}%".format(temperature, humidity))
    # If the delay time is too short, DHT11 may not respond. It is recommended to delay more than 1s
    utime.sleep(1.5)



