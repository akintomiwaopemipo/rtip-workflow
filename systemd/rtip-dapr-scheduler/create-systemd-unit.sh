#!/usr/bin/env bash

sudo cp unit.service /etc/systemd/system/rtip-dapr-scheduler.service

sudo systemctl enable rtip-dapr-scheduler