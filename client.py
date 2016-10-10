#!/usr/bin/env python

# Copyright (C) 2016 Synapse Wireless, Inc.
"""Data Collector MQTT Client script for use with Example 1"""
from __future__ import print_function

import logging

from synapse_data_collector_client.simple_client import simple_data_collector_client

LOG = logging.getLogger(__name__)

# TODO: Replace with your SNAP Thing Services credentials
STS_USER = "username"
STS_PASS = "password"


def print_poll_results(poll):
    """Print out the poll results.

    Prints out the data for each successful node.
    Prints out error codes for each failed node.
    """

    for node, data in poll['successful'].items():
        # Parse the CSV string from the node
        poll_counter, temp_dC, ps_mV = [int(v) for v in data.split(b',')]

        # Print out the data, converting to more common units
        print("{} {} [{}]: Temperature = {} degC, Power Supply Voltage = {} V".format(poll['timestamp'], node, poll_counter, temp_dC * 0.1, ps_mV * 0.001))

    for node, err_code in poll['failed'].items():
        # For failed nodes, just print out the error code.
        print("{} {}: ERROR {}".format(poll['timestamp'], node, err_code))


if __name__ == '__main__':
    logging.basicConfig()

    client = simple_data_collector_client(
        poll_cb=print_poll_results,
        metrics_cb=print,
        status_cb=print,
        mqtt_user=STS_USER,
        mqtt_pass=STS_PASS,
    )
    print("Polling until CTRL-C is pressed")
    client.loop_forever()
