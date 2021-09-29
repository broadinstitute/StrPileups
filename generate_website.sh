rm -rf docs
python3 write_out_metadata_files.py

cd images
python3 -m flipbook --generate-static-website -s "Locus (Inheritance)" -s "EH_long" -s "EH_short"
mv flipbook_html ../docs
echo "Moved website to docs dir"
