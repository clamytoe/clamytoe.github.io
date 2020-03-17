#!/bin/bash
DOC='sop'
DATE=`date +%Y-%m-%d`
REV=`grep revnumber sop.asc | cut -d ' ' -f 2`
PARAMS="--attribute revnumber=$REV --attribute revdate=$DATE"

echo "Converting to HTML..."
bundle exec asciidoctor $PARAMS $DOC.asc
echo " -- HTML outpt at $DOC.html"

echo "Converting to ePub..."
bundle exec asciidoctor-epub3 $PARAMS $DOC.asc
echo " -- ePub output at $DOC.epub"

echo "Converting to Mobi (kf8)..."
bundle exec asciidoctor-epub3 $PARAMS -a ebook-format=kf8 $DOC.asc
echo " -- Mobi output at $DOC.mobi"

echo "Converting to PDF ... (This one takes a while)"
bundle exec asciidoctor-pdf $PARAMS $DOC.asc
echo " -- PDF output at $DOC.pdf"
