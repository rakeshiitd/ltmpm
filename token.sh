TOKEN=`cat ~/.docker/config.json  | tr -d "\n" | base64 -w0`
cat << EOF > secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: ecr
data:
  .dockerconfigjson: ${TOKEN}
type: kubernetes.io/dockerconfigjson
EOF
kubectl apply -f secret.yaml