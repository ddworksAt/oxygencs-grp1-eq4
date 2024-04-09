# Intégration Continue
L'intégration continue via GitHub Actions fait le déploiement de l'image docker vers Kubernetes. 

## Création de kubeconfig
Cette étape prépare l'environnement pour interagir avec notre cluster Kubernetes. Le fichier kubeconfig, qui est nécessaire pour authentifier et communiquer avec le cluster, est créé à partir d'un secret stocké dans GitHub Secrets.
- `mkdir ${HOME}/.kube echo ${{ secrets.KUBE_CONFIG }} | base64 --decode > ${HOME}/.kube/config cat ${HOME}/.kube/config`

## Utilisation du Contexte
Sélectionne le contexte Kubernetes approprié pour les opérations kubectl suivantes. Ceci assure que nos commandes sont exécutées sur le bon cluster.
- `kubectl config use-context do-tor1-log680-k8s-cluster`

## Déploiement sur Kubernetes
Applique les configurations Kubernetes stockées dans le dossier kubernetes/ de notre dépôt. 
- `kubectl apply -f kubernetes/`