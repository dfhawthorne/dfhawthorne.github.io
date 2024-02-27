#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Updates the site map
# Assumes that the scripts and docs sub-directories are siblings
# Ref: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap#xml
# ------------------------------------------------------------------------------

script_loc="$(dirname $(realpath $0))"
site_base_loc="$(realpath ${script_loc}/../docs)"
site_map_loc="${site_base_loc}/system/app/pages"
url_fmt='  <url>\n    <loc>https://dfhawthorne.github.io/%n</loc>\n    <lastmod>%y</lastmod>\n  </url>\n'

cat > "${site_map_loc}/sitemap.xml" <<DONE
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
DONE

"${script_loc}/find_converted_web_pages.sh" | \
    xargs -I@ stat --print "${url_fmt}" "@" | \
    sed -re 's!/./!/!g' \
        -e "s!${site_base_loc}!!" \
        -e 's!//!/!g' \
        -e 's!:/!://!' \
        -e 's!(<lastmod>.{10}).*(</lastmod>)!\1\2!' \
    >> "${site_map_loc}/sitemap.xml"

cat >> "${site_map_loc}/sitemap.xml" <<DONE
</urlset>
DONE
