# ----------------------
#  Format HTML files
# ----------------------
html:
	tidy -config tidy.conf -m html/*.html

.PHONY: html
