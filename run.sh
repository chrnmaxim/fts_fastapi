#!/bin/sh
uvicorn src.main:app --host 0.0.0.0 --port $PORT --loop uvloop --proxy-headers
