# OCN_opener
============
Small plugin which automatically decompresses adc_gz; fsi_gz; mir_gz; yng_gz and
gzip (.gz) files when opened in Sublime Text.

This is an alpha release, use with care, feedback & code welcome!

# Using gzip
When opening a new file this plugin will check the filename for a known compression suffix (.gz currently). If this matches, the useless binary view of the file will be closed and a new file will be opened, filled with the decompressed content.

# Using zlib
When opening a new file this plugin will check the filename for a known compression suffix (*_gz currently). If this matches, the useless binary view of the file will be closed and a new file will be opened, filled with the decompressed content.