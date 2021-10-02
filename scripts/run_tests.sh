#!/bin/sh

cd $(dirname $0)/..

docker-compose -f docker-compose.yml \
               -f docker-compose.tests.yml \
               up --no-deps --build --abort-on-container-exit

status=$?

docker-compose -f docker-compose.yml \
               -f docker-compose.tests.yml \
               down -v

if [ "$status" = 5 ]; then
    echo "No tests collected"
    exit 0
fi

exit $status