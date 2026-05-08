#!/usr/bin/env bash

sudo cp unit.service /etc/systemd/system/rtip-dapr-debug.service

sudo systemctl enable rtip-dapr-debug