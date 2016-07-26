BASEDIR=$(dirname "$0")
basepy="$BASEDIR/ltmain.py"
echo "$basepy"
setup(){
	sudo pip install runp
	sudo pip install awscli
	echo 'provide your aws Access key Id'
	read accessKey
	echo 'provide your aws secret key Id'
	read secretKey
	printf "$accessKey\n$secretKey\nus-east-1\njson"|aws configure
	echo "setup is done..!!"
	echo "connecting to ecr services....."
	echo "trying to login........................"
	runp lt.py dockerECRLogin
	echo "login successful!!!"
	TOKEN=`cat ~/.docker/config.json  | tr -d "\n" | base64 -w0`
	sed -i -e 's/tokenPlace/'${TOKEN}'/g' secret.yaml

	echo "your setup is done."
	echo "Do you want to setup limetray cloud infra(Yes/No): "
	read inp
	echo "You entered: $inp"
	if [ "$inp" == Yes ]; then
		start
	else
		echo "Done!"
	fi
}

helpp(){
	echo "type>>>> 'setup' for setting up the infrastructure"
	echo "type>>>> 'images' to see images from ecr"
	echo "type>>>>  'service active' to see active services"
	echo "type>>>>  'start cloud' to start local limetray cloud cluster"
	echo "type>>>> 'dashboard' to view limetray cloud dashboard in browser"
	echo "type>>>> 'list services' to view running services in limetray cloud"
	echo "type>>>> 'list pods' to view running pods in limetray cloud"
	echo "type>>>> 'run services <imagename>' to run services in limetray cloud"
}

images(){
	runp "$basepy" images
}
stop(){
	minikube stop
}

dashboard(){
	minikube dashboard
}

serviceStatus(){
	kubectl get services 
}

podStatus(){
	kubectl get pods 
}

runService(){
	kubectl create -f nodes/service.yaml
	kubectl create -f nodes/dep.json --record
}
gitInstall(){
	runp "$basepy" pullFromGithub:$2
}

if [ "$1" == setup ]; then
	setup
elif [ "$1" == 'help' ]; then
	helpp
elif [ "$1" == 'images' ]; then
	images
elif [ "$1" == 'start' ]; then
	start
elif [ "$1" == 'stop' ]; then
	stop
elif [ "$1" == 'dashboard' ]; then
	dashboard
elif [ "$1" == 'dashboard' ]; then
	dashboard
elif [ "$1" == 'list' ] && [ "$2" == 'services' ]; then
	serviceStatus
elif [ "$1" == 'list' ] && [ "$2" == 'pods' ]; then
	podStatus
elif [ "$1" == 'run' ] && [ "$2" == 'services' ]; then
	runService
elif [ "$1" == 'git' ]; then
	gitInstall
elif [ "$1" == '' ]; then
	echo ''
elif [ "$1" == 'run' ]; then
	runp /usr/local/bin/ltmain.py run
elif ["$1"=='config']; then
	runp /usr/local/bin/ltmain.py run
else
	echo "Command not supported"

fi