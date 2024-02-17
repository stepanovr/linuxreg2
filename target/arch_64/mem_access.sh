#!/usr/bin/env bash

PORT=35035

PIPE_NAME=pipe
PIPE_DOWN=${PIPE_NAME}_down
PIPE_UP=${PIPE_NAME}_up

FIFO_LOCATION=/tmp

WORK_DIR=`pwd`


killall udpserv


${WORK_DIR}/udpserv $PORT ${FIFO_LOCATION}/$PIPE_DOWN ${FIFO_LOCATION}/$PIPE_UP &
exit 0

while [ true ]
do
  MESSAGE=`cat ${FIFO_LOCATION}/$PIPE_DOWN`
  MESSAGE1=`$WORK_DIR/devmem $MESSAGE`

echo "$MESSAGE1" 
echo " ${FIFO_LOCATION}/$PIPE_UP"

  echo "$MESSAGE1" > ${FIFO_LOCATION}/$PIPE_UP

echo "$MESSAGE $MESSAGE1"

done


