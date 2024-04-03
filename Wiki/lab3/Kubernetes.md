# Kubernetes
Notre équipe est allouée le *namespace* `grp01eq4-namespace` dans le cluster Kubernetes `do-tor1-log680-k8s-cluster` pour effectuer le déploiment du *HVAC Controller*. Des configurations sont nécessaires pour permettre à l'application de fonctionner dans notre namespace. D'abord, les variables d'environnement doivent être déclarées à travers un objet Kubernetes *ConfigMap* et des *secrets*. Il faut également configurer les informations pour le *pod* où une instance de l'application roulera ainsi que les ressources que celui-ci utilisera.

Notez que dans le cadre de ce projet, nous avons préalablement créé un fichier de configurations qui donne le contexte du *cluster* utilisé qui contient notre *namespace* ainsi que notre utilisateur pour rouler les commandes `kubectl`. Ce fichier est sauvegardé localement dans notre machine et non dans le répertoire Github. [kubectl](https://kubernetes.io/docs/tasks/tools/) et [OpenLens](https://github.com/MuhammedKalkan/OpenLens) ont également été installés pour effectuer des configurations.

## ConfigMap
Le *ConfigMap* inclut les variables d'environnement utilisés par l'application qui sont `HOST`, `T_MIN`, `T_MAX`, `MIN_CONN` et `MAX_CONN` et sont énumérées dans le fichier `/kubernetes/configmap.yaml`. Ce sont des valeurs non-confidentielles.

Pour appliquer la configuration de ce fichier, utilisez la commande `kubectl apply ./kubernetes/configmap.yaml`.

## Secrets
Les *Secrets* utilisés sont `DATABASE_URL` et `TOKEN` qui permettent de se connecter à notre base de données PostgreSQL et au simulateur HVAC. Ce sont des données sensibles qui sont sauvegardées directement sur l'interface [OpenLens](https://github.com/MuhammedKalkan/OpenLens) et non dans un fichier qui sera sauvegardé dans notre répositoire Github.

## Deployment, containers et pods
Les configurations concernant le déploiement de l'application se situent dans le fichier `/kubernetes/deployment.yaml`. Les informations spécifient les noms du `container` et du déploiement, le nombre de réplicas à rouler, la référence au *ConfigMap* et *Secrets*, quelle image `Docker` utiliser à partir de Docker Hub. Il y a également les spécifications concernant les ressources de mémoire et de *CPU* que l'application devrait utiliser ainsi que leur limite d'utilisation.

Déployer et rouler *HVAC Controller* dans un pod: `kubectl apply -f ./kubernetes/deployment.yaml`

Énumérer les déploiements: `kubectl get deployment`

Énumérer les *replica sets*: `kubectl get replicaset`

Énumérer les *pods*: `kubectl get pod`

Énumérer les *logs*: `kubectl logs <nom du pod>`

## Open Lens
L'interface Open Lens permet à l'utilisateur de visualiser des évènements reliés aux déploiements, la création d'un `pod`, d'un `container` et des `replicas`, ainsi que le `pull` de l'image `Docker` dans la section *Workload* > *Overview*. Ces évènements indiquent si une application roule tel que prévu sans erreur. Il est également possiblement de voir les déploiements et les pods dans les sections *Workload* > *Deployments* et *Workload* > *Pods* en guise d'alternative aux commandes mentionnées ci-hauts. Finalement, il est possible de vérifier les *ConfigMaps* et les *Secrets* dans les sections *Config* > *ConfigMaps* et *Config* > *Secrets*