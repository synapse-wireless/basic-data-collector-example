"""Synapse Data Collector Simple Client

Usage:
    scdc_client [-h] [-l LEVEL] [--host HOSTNAME] [-p PORT] [-t TOPIC]
    scdc_client --help

Options:
    --host HOSTNAME                      Set the hostname of the data collector [default: localhost]
    -p PORT, --port PORT                 Set the port of the data collector [default: 1883]
    -t TOPIC, --topic TOPIC              Set the topic of the data collector [default: dc1]
    -l LEVEL, --log-level LEVEL          Set current log level. [default: warn]
    -h, --help                           Show this help screen.

"""

from __future__ import print_function

import base64
import json
import logging

import paho.mqtt.client as mqtt

LOG = logging.getLogger(__name__)


def simple_data_collector_client(poll_cb=None, metrics_cb=None, status_cb=None, host='localhost', port=1883, topic='dc1'):  # noqa
    """Create an instance of the paho MQTT client and subscribe to things we're interested in."""

    root_topic = 'dc/' + topic

    mqtt_client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        """MQTT connect callback.

        After we successfully connect to the broker,
        subscribe to the 'polled' and 'status' events.

        See the full documentation at https://eclipse.org/paho/clients/python/docs/ for more information.
        """
        if rc == mqtt.MQTT_ERR_SUCCESS:
            # When we successfully connect, subscribe to the
            # 'polled' and 'status' topics.
            mqtt_client.subscribe(root_topic + '/polled')
            mqtt_client.subscribe(root_topic + '/metrics')
            mqtt_client.subscribe(root_topic + '/status')

    def on_mqtt_message(client, userdata, msg):
        """MQTT message callback

        This function gets called each time a message
        is published to a topic we've subscribed to.
        """
        try:
            if poll_cb and mqtt.topic_matches_sub(root_topic + '/polled', msg.topic):
                # It's a polled message
                poll = json.loads(msg.payload.decode("utf-8"))
                for node, data in poll['successful'].items():
                    poll['successful'][node] = base64.b64decode(data)
                poll_cb(poll)

            elif metrics_cb and mqtt.topic_matches_sub(root_topic + '/metrics', msg.topic):
                # It's a metrics message
                metrics = json.loads(msg.payload.decode("utf-8"))
                metrics_cb(metrics)

            elif status_cb and mqtt.topic_matches_sub(root_topic + '/status', msg.topic):
                # It's a status message
                status = json.loads(msg.payload.decode("utf-8"))
                status_cb(status)

            else:
                LOG.warn("Got unexpected message: %r", msg)
        except:
            LOG.exception("Could not process message: %r", msg.payload)

    # Set up our callbacks for connect and messages
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_mqtt_message

    mqtt_client.connect(host, port, 60)

    return mqtt_client
