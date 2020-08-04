#!/bin/bash

set -m
#mongod --fork --logpath /var/log/mongodb.log &
#fg 1

sleep 1m
cd /home/ivado/ivado

scrapy crawl musmuems
PYTHONPATH=$PYTHONPATH:`pwd` python3 extra_data/city_population.py
PYTHONPATH=$PYTHONPATH:`pwd` python3 ml/linear_regression_influx_pred.py
