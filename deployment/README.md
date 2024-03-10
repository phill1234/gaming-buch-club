# Deployment

## Setup Documentation

### Create pull secrets GitHub for Kubernetes

- set env `CR_PAT` (you can create the token here: https://github.com/settings/tokens)
- `kubectl create secret docker-registry github-container-registry --namespace=default --docker-server=ghcr.io --docker-username=phill1234 --docker-password=${CR_PAT} --dry-run=client --output=yaml > docker-secret.yaml`

### Create new ssh private and public key

- `ssh-keygen -t rsa -b 4096 -C ssh_private_key`

### Update cert-manager

- download cert-manager file from here https://cert-manager.io/docs/installation/#default-static-install


### HOTFIX FOR actual PROBLEMS 
`kubectl apply --server-side --force-conflicts -k https://github.com/traefik/traefik-helm-chart/traefik/crds/`
`kubectl rollout restart deployment traefik -n kube-system`
