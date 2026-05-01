#!/usr/bin/env bash

sudo cp unit.service /etc/systemd/system/rtip-dapr-placement.service

sudo systemctl enable rtip-dapr-placement