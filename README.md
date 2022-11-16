# Laura Cleux

Le code utilisé dans la racine à été utilisé pour la prestation "Atelier Idio-matique" au Quai des Savoirs le 4 novembre 2022 à Toulouse.
L'objectif de l'atelier Idio-matique est de questionner le lien entre les outils d'Intelligence actuels et la langue française (c'est pourquoi cette documentation est en français). L'objectif est aussi de permettre au public passant de pratiquer réellement les outils d'intelligence artificielle, d'en visualiser les enjeux par l'humour.
Le biais exploité ici est la notion de second degré dans les expressions idiomatiques françaises. En effet, les métaphores utilisées peuvent piéger plus facilement les logiques qui demandent un recul culturel.
Enfin, les expressions idiomatiques sont aussi un terrain d'évolution très riches dans les méandres de la langue, de l'argot et de l'Histoire.
Il possède 4 scripts différents en Python 3.8 et met en jeu 4 robots Poppy-Ergo-Junior et un chatbot vocal relié au service en ligne GTP-3 (modèle davinci002) de openAI. Le tout est connecté à un routeur WIFI connecté à Internet qui fixe les adresses IP de chaque machine.

## le script mirror_dlib.py : l'effet miroir par un robot et par le mouvement de translation du cou d'avant en arrière

![](./photo_laura.jpg)

Ce script pilote un poppy-ergo-junior reconfiguré en visage avec une caméra rpicam avec objectif "oeil de poisson".
La libraire dlib est utilisée avec les outils de opencv pour détecter les visages et y repérer les yeux (notamment les coins externes). Les moteurs du robot sont donc réglés (lignes 77 à 82) pour placer le visage au centre de l'image avec les yeux à l'horizontale. Enfin, si le visage est proche, le robot va s'approcher et inversement.
Cette animation robotique est troublante par l'effet miroir qu'il provoque, par la fragilité apparente du mouvement saccadé et le mouvement d'approche ou éloignement qui est un degrés de liberté très rare chez les robots de type humanoïde. Ce mouvement est très puissant car "engageant", ce mouvement évoque clairement une sorte d'effort fourni pour comprendre l'interlocuteur.
Les reactions du public sont comme attendu, soit enthousiaste, soit méfiante car le fait que la caméra fixe le regard sur les yeux des personnes créé de l'empathie malgrés l'aspect décharné du robot.
Ce script est pour l'instant indépendant des autres, la LED du moteur 2 étant pilotée directement par l'autre script de chatbot main_laura.py ("LED en écoute")
Afin de garantir un mouvement assez réactif et fluide et pour des raisons pédagogiques sur ce qu'est l'utilisation d'une API-REST, toute l'API d'appel au robot est rappelée en introduction du script. C'est d'ailleurs le cas dans les autres scripts.

