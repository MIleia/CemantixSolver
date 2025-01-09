# CemantixSolver


Ce projet vise à créer un script Python capable de trouver le mot du jour sur le site Cemantix (https://cemantix.certitudes.org/), un jeu de déduction basé sur la proximité sémantique entre les mots. L’objectif est d’automatiser la recherche du mot du jour en testant une liste de mots provenant d’un dictionnaire filtré et d’optimiser cette liste pour des tentatives futures en excluant les mots non reconnus par le serveur.

La démarche a commencé par la création d’un script de base capable de charger une liste de mots depuis un fichier texte. Une requête POST est envoyée pour chaque mot au serveur du site Cemantix, et les réponses sont analysées pour déterminer si le mot est valide ou si des informations pertinentes, comme le percentile ou le score, sont renvoyées. En cas de réponse d'erreur (mot inconnu), le mot est retiré du dictionnaire pour affiner progressivement la liste.

Ensuite, j’ai intégré un système de sauvegarde des résultats dans un fichier JSON pour permettre une analyse détaillée des réponses du serveur. Ce format est pratique pour conserver les données structurées et consulter les informations post-exécution.

Pour améliorer l’expérience utilisateur, une interface graphique a été créée à l’aide de la bibliothèque Tkinter. Elle affiche dynamiquement les mots testés ainsi que leurs scores, organisés dans un tableau trié par ordre décroissant de percentile. Cette fonctionnalité permet de visualiser immédiatement les résultats et de suivre la progression du script.

Enfin, une fonctionnalité de détection automatique du mot du jour a été ajoutée. Si un mot renvoie un percentile de 1000 (indiquant qu'il s'agit du mot du jour), le script s'arrête et affiche une alerte. 
