import json
import os
from pprint import pprint
import subprocess
print 'Hello limetray shell'
print 'Welcome to limetray shell! type lt.help for help'
baseDir, filename = os.path.split(os.path.abspath(__file__))

print "LT Infra automation framework"
# os.system('pip install runp')
# os.system('rm -rf output.json')
# os.system('aws ecr describe-repositories>>output.json');
with open('ltmpm.json') as data_file:
	data = json.load(data_file)
with open(baseDir+'/config.json') as configs:
		configs = json.load(configs)
def images():
	dd = subprocess.check_output('aws ecr describe-repositories',shell=True)
	dd = json.loads(dd)
	repos = dd['repositories']
	for item in repos:
		print item['repositoryName']
		print "      Tags"
		output2 = subprocess.check_output("aws ecr list-images --repository-name "+str(item['repositoryName']), shell=True)
		data2 = json.loads(output2)
		imageIds = data2['imageIds']
		for t in imageIds:
			if ('imageTag' in t):
			    print "            "+t['imageTag']
			else:
				print "            Image without tag"
def ecrPullAll():
  os.system('aws ecr describe-repositories>>output.json');
with open(baseDir+'/.kubservices/services.json') as runningServices:
	runningServices = json.load(runningServices)

def help(t):
	print "help"
def start():
	os.system('minikube start')
def stop():
	os.system('stop minikube')
def activeAccessToken():
	os.system("sudo chmod +x token.sh")
	os.system("./token.sh")
def dockerECRLogin():
  output = subprocess.check_output("aws ecr get-login", shell=True)
  os.system(output)
  print 'You will be automatically logged out after 12 hrs'
def config(t):
	print "Please select registry(ecr or gcr)"
	registry = raw_input()
	print "Please provide github username"
	githubUsername=raw_input()
	print "Please provide github password"
	githubPassword=raw_input()
	configs['registry']=registry
	start()
	if(registry=='ecr'):
		print 'Provide Aws access key Id'
		awsAccessKeyId = raw_input()
		configs['awsAccessKeyId']=awsAccessKeyId
		print 'Provide Aws secret key Id'
		awsSecretKeyId = raw_input()
		configs['awsSecretKeyId']=awsSecretKeyId
		os.system("sudo chmod +x configureAws.sh")
		os.system(baseDir+"/configureAws.sh "+awsAccessKeyId+" "+awsSecretKeyId)
	elif(registry=='gcr'):
		print 'Provide Google cloud access key Id'
		googleAccessKeyId = raw_input()
		configs['googleAccessKeyId']=googleAccessKeyId
		print 'Provide Google cloud secret key Id'
		googleSecretKeyId = raw_input()
		configs['googleSecretKeyId']=googleSecretKeyId
	else:
		print "LT doesn't support this registry right now. please contact lt@limetray.com"
	os.system('kubectl delete secret ecr')
	dockerECRLogin()
	activeAccessToken()
	configs['githubPassword']=githubPassword
	configs['githubUsername']=githubUsername
	with open(baseDir+'/config.json','w') as configs2:
		configs2.write(json.dumps(configs))
	
def checkConfigs(func):
	print configs
	if (configs['registry']=="" or configs['githubUsername']=="" or configs['githubPassword']==""):
		print "You are not configured right now!"
		return config(func)
	else:
		print "yolo"
		return func
@checkConfigs
def setup():
	os.system("sudo chmod +x configureAws.sh")
	os.system(baseDir+"/configureAws.sh")


@checkConfigs
def run(data=data):
	# os.system("git clone https://github.com/LimeTray/node-service-boilerplate.git")
	print os.getcwd()
	for app in data:
		if(app['name'] in runningServices):
			print app['name']+' is already running......'
			continue
		runningServices.append(app['name'])
		if('githubUrl' in app):
			repoUrl = app['githubUrl']
		else:
			repoName = app['name']
			repoUrl = 'https://github.com/LimeTray/'+repoName+'.git'
		if(os.path.exists(baseDir+'/'+app['name'])==False):
			os.system('git clone '+repoUrl+' '+baseDir+'/'+app['name'])
		else:
			os.system('git fetch --all')
			os.system('git pull --all')
		if('tag' in app and app['tag']!=""):
			os.system('git --git-dir='+baseDir+'/'+app['name']+'/.git --work-tree='+baseDir+'/'+app['name']+'checkout tags/'+app['tag'])
			#os.system("git checkout tags/"+app['tag'])
		elif('branch' in app and app['branch']!=""):
			os.system('git --git-dir='+baseDir+'/'+app['name']+'/.git --work-tree='+baseDir+'/'+app['name']+' checkout '+app['branch'])
			#os.system("git checkout "+app['branch'])
		lt = baseDir+'/'+app['name']+'/k8s'
		dep =lt+'/config.json'
		# ser = lt+'/service.yaml'
		# os.system('kubectl create -f '+ser)
		# os.system('kubectl create -f '+dep+' --record')
		with open(dep) as configFile:
			configData = json.load(configFile)
		with open(baseDir+'/.k8s/deployment.json','r') as deployment:
			print(deployment)
			deployment = json.load(deployment)
		with open(baseDir+'/.k8s/service.json','r') as service:
			service = json.load(service)
		for t in deployment['spec']['template']['spec']['containers']:
			if('imageTag' in app):
				strr = '/'+app['name']+':'+app['imageTag']
			t['image'] = t['image']+strr
			#t['env'] = configData['environment']
			for w in t['ports']:
				w['containerPort'] = configData['port']
			t['resources'] = configData['resources']
			t['name'] = app['name']
		deployment['metadata']['name'] = app['name']
		deployment['spec']['template']['metadata']['labels'] = configData['labels']
		service['metadata']['name'] = app['name']
		service['metadata']['labels'] = configData['labels']
		for w in service['spec']['ports']:
				w['targetPort'] = configData['port']
		service['spec']['type'] = 'NodePort'
		service['spec']['selector']['app'] = app['name']
		deployment['spec']['replicas'] = configData['replicas']
		if not os.path.exists(baseDir+'/'+'.kub/'+app['name']):
			os.system('sudo mkdir '+baseDir+'/.kub/'+app['name'])
		with open(baseDir+'/.kub/'+app['name']+'/deployment.json','w') as f1:
			f1.write(json.dumps(deployment))
		with open(baseDir+'/.kub/'+app['name']+'/service.json','w') as f2:
			f2.write(json.dumps(service))
		os.system('kubectl create -f '+baseDir+'/.kub/'+app['name']+'/deployment.json')
		os.system('kubectl create -f '+baseDir+'/.kub/'+app['name']+'/service.json')
		if os.path.exists(baseDir+'/'+app['name']+'/ltmpm.json'):
			with open(baseDir+'/'+app['name']+'/ltmpm.json') as data_file:
				data = json.load(data_file)
				run(data)
	with open(baseDir+'/.kubservices/services.json','w') as writeServices:
		writeServices.write(json.dumps(runningServices))






# os.system('kubectl create -f service.yaml')
# os.system('kubectl create -f deployment.json --record')
# os.system("wget "+data[0]['imageUrl'])
# os.system("wget "+data[0]['configUrl'])

if __name__ == '__main__':
    run()