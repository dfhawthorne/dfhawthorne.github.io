#!/usr/bin/sed -rf
s!((.*)\?attredirects=0(&d=[0-9]+)?)!git mv '\1' '\2'!
