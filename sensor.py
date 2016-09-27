# Copyright (C) 2016 Synapse Wireless, Inc.
# Subject to your agreement of the disclaimer set forth below, permission is given by Synapse Wireless, Inc. ("Synapse")
# to you to freely modify, redistribute or include this SNAPpy code in any program. The purpose of this code is to help
# you understand and learn about SNAPpy by code examples.
# BY USING ALL OR ANY PORTION OF THIS SNAPPY CODE, YOU ACCEPT AND AGREE TO THE BELOW DISCLAIMER. If you do not accept or
# agree to the below disclaimer, then you may not use, modify, or distribute this SNAPpy code.
# THE CODE IS PROVIDED UNDER THIS LICENSE ON AN "AS IS" BASIS, WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING, WITHOUT LIMITATION, WARRANTIES THAT THE COVERED CODE IS FREE OF DEFECTS, MERCHANTABLE, FIT FOR A
# PARTICULAR PURPOSE OR NON-INFRINGING. THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE COVERED CODE IS WITH
# YOU. SHOULD ANY COVERED CODE PROVE DEFECTIVE IN ANY RESPECT, YOU (NOT THE INITIAL DEVELOPER OR ANY OTHER CONTRIBUTOR)
# ASSUME THE COST OF ANY NECESSARY SERVICING, REPAIR OR CORRECTION. UNDER NO CIRCUMSTANCES WILL SYNAPSE BE LIABLE TO
# YOU, OR ANY OTHER PERSON OR ENTITY, FOR ANY LOSS OF USE, REVENUE OR PROFIT, LOST OR DAMAGED DATA, OR OTHER COMMERCIAL
# OR ECONOMIC LOSS OR FOR ANY DAMAGES WHATSOEVER RELATED TO YOUR USE OR RELIANCE UPON THE SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGES OR IF SUCH DAMAGES ARE FORESEEABLE. THIS DISCLAIMER OF WARRANTY AND LIABILITY
# CONSTITUTES AN ESSENTIAL PART OF THIS LICENSE. NO USE OF ANY COVERED CODE IS AUTHORIZED HEREUNDER EXCEPT UNDER THIS
# DISCLAIMER.

"""
Example SNAPpy script for Data Collector sensors.

Returns:
  * Number of polls received since last restart
  * ATmega128RFA1 internal temperature in deci-degrees Celsius (dC)
  * ATmega128RFA1 power supply voltage in milliVolts (mV)

Also blinks an led each time it is polled.
"""

from snappyatmega.sensors import *

# Setting this to none will disable the blink
# LED_PIN = None

# 6 is GPIO_1 for SN-171 protoboards and SN-132 paddleboards,
# and the green led on SS200 / SN220 SNAPsticks.
LED_PIN = 6

NUM_POLLS = 0


def data():
    """Return the formatted data string"""
    # First, blink the LED
    pulsePin(LED_PIN, 1000, True)

    # Get the individual values
    num_polls = _get_poll_counter()

    raw_temp = atmega_temperature_read_raw()
    temp_dC = atmega_temperature_raw_to_dC(raw_temp)

    ps_mV = atmega_ps_voltage()

    # Return as a CSV-formatted string
    return str(num_polls) + "," + str(temp_dC) + "," + str(ps_mV)


@setHook(HOOK_STARTUP)
def _on_startup():
    # Initialize the LED
    setPinDir(LED_PIN, True)
    writePin(LED_PIN, False)


def _get_poll_counter():
    """Increment and return the poll counter"""
    global NUM_POLLS
    NUM_POLLS += 1

    return NUM_POLLS
