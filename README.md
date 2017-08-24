Misc Tools
============================

# Host Tools


### reduce_size.sh
 - Reduce Backup image (Host Tools)
``` 
$ ./reduce_size.sh <file> <size(xxxM or xxxG)>
```


# on Raspberry Pi


### resize2fs
 - Re-size rootfs adjust with SD Card size
``` 
$ sudo cp resize2fs /etc/init.d
``` 

Add below comment on /etc/rc.user
``` 
# Check and Re-size rootfs
/etc/init.d/resize2fs
```
