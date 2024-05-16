#!/usr/bin/sed -rf
# ------------------------------------------------------------------------------
# Fixes issue #88:
# Generates GIT MV commands in /tmp/git-mv.sh
# Generates SED commands in /tmp/fix-url.sed
# ------------------------------------------------------------------------------
/^[0-9-]{10}-.*:title: /d
s!^(([0-9]{2})(-.*)):title: .([0-9-]{10}) ([0-9]) .*!git mv '\1' '\4-\5\3'!
s!^(([0-9]{2})(-.*)):title: .([0-9-]{10}).*!git mv '\1' '\4\3'!
w /tmp/git-mv.sh
s!git mv ('.*') ('.*')!/url:/s~\1~\2~!
w /tmp/fix-url.sed
d

