#!/bin/sh

cd $(dirname $0)

/usr/bin/fab down

sleep 5

/usr/bin/fab up

exit 0
