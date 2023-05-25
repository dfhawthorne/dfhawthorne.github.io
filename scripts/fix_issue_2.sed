#!/usr/bin/env sed -rf 
# ------------------------------------------------------------------------------
# Fix up old Google Sites HTML file
# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
# Change URLs from Google Sites to GitHub
# ------------------------------------------------------------------------------
s!https://sites.google.com/site/yetanotherocmoriginal/!https://dfhawthorne.github.io/!g
s!"/site/yetanotherocmoriginal/!"/!g
s!"/site/yetanotherocmoriginal"!"/"!g
# ------------------------------------------------------------------------------
# Move referenced files out of _/rsrc subdirectory
# ------------------------------------------------------------------------------
s!_/rsrc/[[:digit:]]+/!!g
# ------------------------------------------------------------------------------
# Remove Google Sites widgets
# ------------------------------------------------------------------------------
# Remove 'Join Our Discussion' widget
# ------------------------------------------------------------------------------
s!(<div xmlns="http://www.w3.org/1999/xhtml" id="COMP_[[:digit:]]+" class="sites-embed" role="complementary">)<h4 class="sites-embed-title">Join Our Discussion</h4><div class="sites-embed-content sites-embed-content-sidebar-textbox"><div dir="ltr"><p style="text-align:center"><a href="http://groups.google.com/support/bin/topic.py\?topic=[[:digit:]]+" target="_blank"><img( border="0")? src="(\.\./)*config/app/images/psd-chat-icon-smaller.gif"( border="0")? /></a><(br /|/p)>!\1\&nbsp;!
s!<a href="http://groups.google.com/support/bin/topic.py\?topic=[[:digit:]]+" target="_blank">Join the Discussion</a></p></div></div>(</div>)!\&nbsp;\1!
# ------------------------------------------------------------------------------
# Remove 'Template tips' widget
# ------------------------------------------------------------------------------
s!(<div xmlns="http://www.w3.org/1999/xhtml" id="COMP_[[:digit:]]+" class="sites-embed" role="complementary">)<h4 class="sites-embed-title">Template tips</h4><div class="sites-embed-content sites-embed-content-sidebar-textbox"><div dir="ltr"><a href="https://sites.google.com/site/sitetemplateinfo/tips" target="_blank">Learn more about working with templates.</a><br /><br /><a href="https://sites.google.com/site/sitetemplateinfo/tips/customize-your-site-sidebar" target="_blank">How to change this sidebar.</a><br /></div></div>(</div>)!\1\&nbsp;\2!
# ------------------------------------------------------------------------------
# Remove 'Search this site' widget
# ------------------------------------------------------------------------------
s!(<td id="sites-header-title" class="" role="banner" style="height: 70px"><div class="sites-header-cell-buffer-wrapper"><h2><a href="(\.\./)*index.html" dir="ltr" id="sites-chrome-userheader-title">Yet Another OCM</a></h2></div></td><td class="sites-layout-searchbox  "><div class="sites-header-cell-buffer-wrapper">)<form id="sites-searchbox-form" action="https://dfhawthorne.github.io/system/app/pages/search" role="search"><input type="hidden" id="sites-searchbox-scope" name="scope" value="search-site" /><input type="text" id="jot-ui-searchInput" name="q" size="20" value="" aria-label="Search this site" /><div id="sites-searchbox-button-set" class="goog-inline-block"><div role="button" id="sites-searchbox-search-button" class="goog-inline-block jfk-button jfk-button-standard" tabindex="0">Search this site</div></div></form>(</div></td>)!\1\&nbsp;\2!
# ------------------------------------------------------------------------------
# Remove 'Page Footer' widget
# ------------------------------------------------------------------------------
s!(<div xmlns="http://www.w3.org/1999/xhtml" class="sites-adminfooter" role="navigation"><p>)<a class="sites-system-link" href="https:.*\&amp;service=jotspot">Sign in</a><span aria-hidden="true">|&nbsp;|</span><a class="sites-system-link" href="javascript:;" onclick="window.open(webspace.printUrl)">Print Page</a>!\1!
s!(<div xmlns="http://www.w3.org/1999/xhtml" class="sites-adminfooter" role="navigation"><p>)<a class="sites-system-link" href="https:.*\&amp;service=jotspot">Sign in</a><span aria-hidden="true">|</span><a class="sites-system-link" href="(\.\./)*app/pages/recentChanges.html">Recent Site Activity</a><span aria-hidden="true">|</span><a class="sites-system-link" href="(\.\./)*app/pages/reportAbuse.html" target="_blank">Report Abuse</a>!\1!
s!(<div xmlns="http://www.w3.org/1999/xhtml" class="sites-adminfooter" role="navigation"><p>)<a class="sites-system-link" href="https:.*\&amp;service=jotspot">Sign in</a><span aria-hidden="true">|</span><a class="sites-system-link" href="(\.\./)*recentChanges.html">Recent Site Activity</a><span aria-hidden="true">|</span><a class="sites-system-link" href="(\.\./)*reportAbuse.html" target="_blank">Report Abuse</a>!\1!

