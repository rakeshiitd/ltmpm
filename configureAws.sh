sudo pip install awscli
printf "$1\n$2\nus-east-1\njson"|aws configure
echo "setup done..!!"