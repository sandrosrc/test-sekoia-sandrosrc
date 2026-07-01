# Test Technique pour Sekoia.io - Alexandre Chaillet

## Temps passé : 2h

## Environnement
- Ubuntu local
- Docker
- K3d
- DockerHub : https://hub.docker.com/repositories/sandrosrc
- GitHub : https://github.com/sandrosrc/test-sekoia-sandrosrc

## 1 - Mettre en place une instance Redis

Le fichier .aof était dans l'ancien format Redis, il fallait donc mettre en place une instance Redis avec une rétro-compatibilité. Le fichier était corrompu avec une perte de 100 octets, ce qui équivaut au final à un vers du premier couplet. Pour le fixer j'ai mis en place un initContainer dédié qui, après l'avoir récupéré depuis mon repo github, fait un check aof et le fix directement.

La stack réalisée pour l'étape 1 consiste en un seul pod avec 2 initcontainers (récupération du fichier, puis fix du fichier si nécessaire), puis ensuite on instancie un conteneur Redis avec un service dédié. Le Service en lui même ne sert pas pour l'étape 1, mais j'en ai besoin pour l'étape 3 pour exposer mon service à mon cluster.

Tout tourne en root, c'est potentiellement un problème sur le long terme d'un point de vue sécurité.

Point d'amélioration, j'aurais dû, avec le recul, mettre en place un statefulset à la place d'un simple pod, car je me suis retrouvé durant la partie 3 à ce que mon pod meurt d'un coup, et vu qu'il était à nu, il ne s'est pas recréé automatiquement.

## 2 - Récupérer le poème, et le déchiffrer, puis le réécrire

Pour trouver le code me permettant de déchiffrer le fichier il a fallu que je fasse un dig DNS sur un domaine qui était écrit en dur sur le fichier .aof, une fois que j'ai trouvé la clé j'ai juste eu besoin de faire un script python pour déchiffrer chacune des valeurs, et les triers ensuite, pour pouvoir les afficher.

La petite subtilité était de réaliser une connexion à mon instance Redis, et je ne savais pas qu'il y avait une librairie redis pour python, j'ai perdu un peu de temps comme ça mais cette derniere était plutôt pratique pour le reste de l'exercice. 

Le script se connecte à Redis, récupère dynamiquement toutes les clés présentes (plutôt que de coder en dur leur nombre), les classe par préfixe de nom (title / author / inspiration.lineN / verses.stanzaN.lineM), déchiffre chacune par XOR répété, et exporte le tout en YAML.

La clé "inspiration.line1" est corrompue à cause de la réparation du fichier à l'étape 1, plutôt que de bloquer le script on remplace les charactères non décodables par U+FFFD (le point d'interrogation dans un carré en diagonale là)

## 3 - Afficher un couplet par minute avec Kubernetes

Alors pour la derniere étape il fallait faire une stack complète qui allait utiliser en partie les ressources qu'on as mise en place avant. A partir d'un script python qui va récupérer le poème puis le déchiffrer, il faut cette fois être en capacité d'afficher un complet aléatoirement toute les minutes. 

Pour que ce script fonctionne j'ai créé un Dockerfile que j'ai poussé sur mon dockerhub (https://hub.docker.com/repository/docker/sandrosrc/poem-display). Ce dernier va créer une instance python, installer les dépendances dont j'ai besoin pour réaliser ma tâche, en l'occurence la librairie redis, définie depuis le fichier requirements.txt.

L'image créée à partir de ce dockerfile, poussée sur mon hub, est récupérée dans mon cronjob yaml afin de déclarer un job du nom de "poem-display", ce cronjob va se lancer toutes les minutes et affichera un couplet aléatoire dans ses logs.

Comme je l'ai dit plus tôt, mon pod Redis est mort durant la réalisation de cette étape, et c'est pour cela que je pense que j'aurais du faire un StatefulSet avec un volume persistent avec le recul. 

Pour être sûr de ne pas avoir de problèmes de dépendances et de garantir la disposition d'un service clé en main, le fichier .aof est récupéré directement depuis un repo public (https://raw.githubusercontent.com/sandrosrc/test-sekoia-sandrosrc/master/poem-1-.aof) et l'image est elle aussi dispo en public aussi sur dockerhub (https://hub.docker.com/repository/docker/sandrosrc/poem-display).