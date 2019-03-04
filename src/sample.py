# -*- coding: utf-8 -*-
"""Tutorial on using the InfluxDB client."""

import argparse
import json

from influxdb import InfluxDBClient


class Metric(object):
    '''A single metric family and its samples.

    This is intended only for internal use by the instrumentation client.

    Custom collectors should use GaugeMetricFamily, CounterMetricFamily
    and SummaryMetricFamily instead.
    '''

    def __init__(self, measurement, tags, fields):
        self.measurement = measurement
        self.tags = tags
        self.fields = fields


def main(host='192.168.1.18', port=8086):
    """Instantiate a connection to the InfluxDB."""

    databaseName = 'example'
    json_body = [
        {
            "measurement": "sample_python",
            "tags": {
                "host": "surface_book",
                "env": "test"
            },
            "fields": {
                "Float_value": 0.64,
                "Int_value": 3,
                "String_value": "Text",
                "Bool_value": True
            }
        }
    ]

    metric = Metric("sample_python", {
                    "host": "surface_book",
                    "env": "test"}, {
        "Float_value": 0.64,
        "Int_value": 3,
        "String_value": "Text",
        "Bool_value": True})

    client = InfluxDBClient(host, port, "root", "root", databaseName)

    print("Create database: " + databaseName)
    # client.create_database(databaseName)
    client.switch_database(databaseName)

    metricsAsJson = json.dump(metric)
    client.write_points(metricsAsJson)
    print("Write points: {0}".format(json_body))


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='192.168.1.18',
                        help='hostname of InfluxDB http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port of InfluxDB http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
