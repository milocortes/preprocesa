while IFS=, read -r field1 field2
do
    nombre=`echo $field1 | tr ' ' '_'`
    nombre=`echo $nombre"_"$field2`
    echo $nombre
    pdftoppm 702825006792.pdf $nombre -png -f $(($field2+1)) -singlefile
done < zm_extract.csv
mv *.png images/
