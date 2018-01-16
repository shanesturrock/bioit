#!/bin/bash
# ----------------------------------------------------------------------
# mikes handy rotating-filesystem-snapshot utility
# ----------------------------------------------------------------------
# this needs to be a lot more general, but the basic idea is it makes
# rotating backup-snapshots of /$BACKUP_DIR whenever called
# ----------------------------------------------------------------------

unset PATH      # suggestion from H. Milz: avoid accidental use of $PATH

# ------------- system commands used by this script --------------------
ID=/usr/bin/id;
ECHO=/bin/echo;

MOUNT=/bin/mount;
RM=/bin/rm;
MV=/bin/mv;
CP=/bin/cp;
TOUCH=/bin/touch;

RSYNC=/usr/bin/rsync;


# ------------- file locations -----------------------------------------

SNAPSHOT_RW=/raid/snapshot;
EXCLUDES=/usr/local/etc/backup_exclude;
BACKUP_DIR=$1

# ------------- the script itself --------------------------------------

# make sure we're running as root
if (( `$ID -u` != 0 )); then { $ECHO "Sorry, must be root.  Exiting..."; exit; } fi

# rotating snapshots of /$BACKUP_DIR (fixme: this should be more general)

# step 1: delete the oldest snapshot, if it exists:
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/hourly.3 ] ; then                     \
$RM -rf $SNAPSHOT_RW/$BACKUP_DIR/hourly.3 ;                            \
fi ;

# step 2: shift the middle snapshots(s) back by one, if they exist
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/hourly.2 ] ; then                     \
$MV $SNAPSHOT_RW/$BACKUP_DIR/hourly.2 $SNAPSHOT_RW/$BACKUP_DIR/hourly.3 ;     \
fi;
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/hourly.1 ] ; then                     \
$MV $SNAPSHOT_RW/$BACKUP_DIR/hourly.1 $SNAPSHOT_RW/$BACKUP_DIR/hourly.2 ;     \
fi;

# step 3: make a hard-link-only (except for dirs) copy of the latest snapshot,
# if that exists
if [ -d $SNAPSHOT_RW/$BACKUP_DIR/hourly.0 ] ; then                     \
$CP -al $SNAPSHOT_RW/$BACKUP_DIR/hourly.0 $SNAPSHOT_RW/$BACKUP_DIR/hourly.1 ; \
fi;

# step 4: rsync from the system into the latest snapshot (notice that
# rsync behaves like cp --remove-destination by default, so the destination
# is unlinked first.  If it were not so, this would copy over the other
# snapshot(s) too!
$RSYNC                                                          \
        -va --delete --delete-excluded                          \
        --exclude-from="$EXCLUDES"                              \
        /$BACKUP_DIR/ $SNAPSHOT_RW/$BACKUP_DIR/hourly.0 ;

# step 5: update the mtime of hourly.0 to reflect the snapshot time
$TOUCH $SNAPSHOT_RW/$BACKUP_DIR/hourly.0 ;
