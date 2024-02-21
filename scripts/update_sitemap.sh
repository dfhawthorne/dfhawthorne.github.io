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

find "${site_base_loc}" \
        -type f \
        \( -name "*.html" -o -name "*.gif" -o -name "*.png" \) | \
    sed -re '/\/_site\//d' \
        -e '/\/system\/errors\/NodeNotFound/d' \
        -e '/\/system\/app\/pages\//d' \
        -e '/\?attredirects/d' | \
    xargs -I@ stat --print "${url_fmt}" "@" | \
    sed -re 's!/./!/!g' \
        -e 's!/home/douglas/git-repositories/dfhawthorne.github.io/docs!!' \
        -e 's!//!/!g' \
        -e 's!:/!://!' \
    >> "${site_map_loc}/sitemap.xml"

cat >> "${site_map_loc}/sitemap.xml" <<DONE
</urlset>
DONE
