#!/bin/bash

IMG_FILE=$1
REDUCE_SIZE=$2
START_OFFSET=$(sudo fdisk -l $IMG_FILE | grep 'Linux' | awk '{print $(2)}')

echo "Start Offset $START_OFFSET"

# Reduce Size
sudo losetup /dev/loop0 $IMG_FILE -o $(($START_OFFSET*512))
sudo e2fsck -f /dev/loop0
sudo resize2fs -p /dev/loop0 $REDUCE_SIZE
sudo losetup -d /dev/loop0

# Re-Partition
echo -en "d\n2\nn\np\n2\n$START_OFFSET\n+$REDUCE_SIZE\nw\n" > partition.log
sudo losetup /dev/loop0 $IMG_FILE
sudo fdisk /dev/loop0 < partition.log

# Reduce Size
END_OFFSET=$(sudo fdisk -l /dev/loop0 | grep 'Linux' | awk '{print $(3)}')
echo "New End Offset $END_OFFSET"
truncate -s $((($END_OFFSET+1)*512)) $IMG_FILE

sudo losetup -d /dev/loop0
rm partition.log
