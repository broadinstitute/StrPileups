rm -rf docs
python3 -m flipbook --generate-static-website
mv flipbook_html docs
echo "Moved website to docs dir"
