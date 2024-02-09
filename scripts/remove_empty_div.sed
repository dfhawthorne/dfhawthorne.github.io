#!/usr/bin/sed -zrf
# ---------------------------------------------------------------
# Remove up to four (4) levels of empty DIV elements
# ---------------------------------------------------------------
s!<div[^>]*>[[:space:]]*</div>!!g
s!<div[^>]*>[[:space:]]*</div>!!g
s!<div[^>]*>[[:space:]]*</div>!!g
s!<div[^>]*>[[:space:]]*</div>!!g
