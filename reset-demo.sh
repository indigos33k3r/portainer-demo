#!/bin/sh

cd $(dirname $0)

/usr/bin/fab down

sleep 5

/usr/bin/docker system prune --volumes -f

/usr/bin/fab up

exit 0
