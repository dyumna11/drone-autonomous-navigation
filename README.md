# Drone Autonomous Navigation System

## Overview
A Python-based autonomous drone navigation system developed for a drone competition. The project enables waypoint logging during manual flight and autonomous traversal of recorded GPS coordinates.

## Features
- GPS waypoint logging
- RC-channel-based mission control
- Autonomous waypoint navigation
- DroneKit integration
- Flight telemetry monitoring

## Technologies
- Python
- DroneKit
- MAVLink
- GPS Navigation

## My Contributions
- Developed waypoint logging functionality using RC channel triggers.
- Implemented GPS coordinate storage and retrieval.
- Built autonomous waypoint traversal logic using DroneKit APIs.
- Contributed to mission-control and navigation workflows.

## Workflow
1. Pilot manually flies the drone.
2. GPS coordinates are logged using an RC trigger.
3. Coordinates are stored locally.
4. Autonomous mode reads stored waypoints.
5. Drone navigates through each waypoint sequentially.
