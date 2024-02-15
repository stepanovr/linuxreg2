#!/usr/bin/env bash

PORT=35035

PIPE_NAME=pipe
PIPE_DOWN=${PIPE_NAME}_down
PIPE_UP=${PIPE_NAME}_up

FIFO_LOCATION=/tmp

WORK_DIR=`pwd`

#[ -p "${FIFO_LOCATION}/$PIPE_DOWN" ] && rm  "${FIFO_LOCATION}/$PIPE_DOWN"

#[ -p "${FIFO_LOCATION}/$PIPE_UP" ] && rm  "${FIFO_LOCATION}/$PIPE_UP"


#mkfifo  "${FIFO_LOCATION}/$PIPE_DOWN"
#mkfifo  "${FIFO_LOCATION}/$PIPE_UP"
#chmod 666 "${FIFO_LOCATION}/$PIPE_DOWN"
#chmod 666 "${FIFO_LOCATION}/$PIPE_UP"


killall udpserv


${WORK_DIR}/udpserv $PORT ${FIFO_LOCATION}/$PIPE_DOWN ${FIFO_LOCATION}/$PIPE_UP &
#exit 0

while [ true ]
do
  MESSAGE=`cat ${FIFO_LOCATION}/$PIPE_DOWN`
  MESSAGE1=`$WORK_DIR/devmem $MESSAGE`

echo "$MESSAGE1" 
echo " ${FIFO_LOCATION}/$PIPE_UP"

  echo "$MESSAGE1" > ${FIFO_LOCATION}/$PIPE_UP

echo "$MESSAGE $MESSAGE1"

done
#ls -l ${FIFO_LOCATION}/$PIPE_UP
#ls -l ${FIFO_LOCATION}/$PIPE_DOWN


