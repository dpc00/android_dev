#!/bin/bash

export agbi=0
em=cymndDM
inotifyd agb1.sh $scrdev:$em &
inotifyd agb1.sh $blog:$em $scrdev:em &
inotifyd agb1.sh /sdcard/documents/Finance.db:$em &
