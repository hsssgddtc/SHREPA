#!/bin/sh
ps up `cat mydaemon.pid `>/dev/null && echo "Program Running" || "Program Not Running"
