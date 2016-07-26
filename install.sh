echo $PWD
base="$PWD"
echo "$base/ltmain.sh"
ltmain="lt='$base/ltmain.sh \$@'"
echo "alias $ltmain">>~/.bash_aliases

sudo chmod -R 777 .
sudo chmod +x ltmain.sh
sudo chmod +x token.sh
sudo chmod +x configureAws.sh