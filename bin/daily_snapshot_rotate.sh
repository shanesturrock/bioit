#!/bin/bash
# ----------------------------------------------------------------------
# mikes handy rotating-filesystem-snapshot utility: daily snapshots
# ----------------------------------------------------------------------
# intended to be run daily as a cron job when hourly.3 contains the
# midnight (or whenever you want) snapshot; say, 13:00 for 4-hour snapshots.
# ----------------------------------------------------------------------

unset PATH

# ------------- system commands used by this script --------------------
ID=/usr/bin/id;
ECHO=/bin/echo;

MOUNT=/bin/mount;
RM=/bin/rm;
MV=/bin/mv;
CP=/bin/cp;

# ------------- file locations -----------------------------------------

SNAPSHOT_RW=/raid/snapshot;
BACKUP_DIR=$1

# ------------- the script itself --------------------------------------

# make sure we're running as root
if (( `$ID -u` != 0 )); then { $ECHO "Sorry, must be root.  Exiting..."; exit; } fi

# step 1: delete the oldest snapshot, if it exists:
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/daily.2 ] ; then                      \
$RM -rf $SNAPSHOT_RW/$BACKUP_DIR/daily.2 ;                             \
fi ;

# step 2: shift the middle snapshots(s) back by one, if they exist
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/daily.1 ] ; then                      \
$MV $SNAPSHOT_RW/$BACKUP_DIR/daily.1 $SNAPSHOT_RW/$BACKUP_DIR/daily.2 ;       \
fi;
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/daily.0 ] ; then                      \
$MV $SNAPSHOT_RW/$BACKUP_DIR/daily.0 $SNAPSHOT_RW/$BACKUP_DIR/daily.1;        \
fi;

# step 3: make a hard-link-only (except for dirs) copy of
# hourly.3, assuming that exists, into daily.0
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/hourly.3 ] ; then                     \
$CP -al $SNAPSHOT_RW/$BACKUP_DIR/hourly.3 $SNAPSHOT_RW/$BACKUP_DIR/daily.0 ;  \
fi;

# note: do *not* update the mtime of daily.0; it will reflect
# when hourly.3 was made, which should be correct.
