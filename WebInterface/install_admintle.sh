#!/bin/bash

VERSION="2.3.0"
DOWNLOAD_URL="https://almsaeedstudio.com/download/AdminLTE-$VERSION"
STATIC_DIR="WebInterface/static/adminlte"


mkdir -p $STATIC_DIR
wget -q $DOWNLOAD_URL -O AdminLTE-$VERSION.zip
unzip -q AdminLTE-$VERSION.zip
cp -r AdminLTE-$VERSION/bootstrap $STATIC_DIR/.
cp -r AdminLTE-$VERSION/dist $STATIC_DIR/.
cp -r AdminLTE-$VERSION/plugins $STATIC_DIR/.

rm AdminLTE-$VERSION.zip
rm -r AdminLTE-$VERSION