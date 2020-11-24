# Devoir 1
Kilian GUILLAUME

## Modélisation

La conception d'un circuit imprimé est un exemple de problème d'optimisation.

L'objectif est ici d'avoir les traces les plus courtes entre les différents composants afin de réduire l'espace prit par le circuit imprimé.

L'ensemble des solutions possibles est ici chaque combinaison possible de placement des composants (x et y, ainsi que la rotation).

Le critère de qualité peut être décrit comme la surface du circuit imprimé résultant.

## Métaheuristique

### Hill-climbing

L'algorithme de hill-climbing est un algorithme d'exploitation maximale, car il va parcourir les solutions voisines dans le but de trouver la meilleure.

### Recuit simulé

Le recuit-simulé est un algorithme utilisant l'exploration au début de l'exécution, puis de l'exploitation en fin d'exécution.

L'idée est ici de maximiser les chances de trouver l'optimum global grâce à une phase de recherche aléatoire, suivit d'une phase de hill-climbing.

### Recherche taboue

La recherche tabou utilise l'exploitation, mais évite les optima locaux grâce à un système de "mouvements interdits", ce qui favorise l'exploration.

### Recherche locale itérée

La recherche locale itérée réalise une exploitation maximale, jusqu'à trouver un optimum local.

Un fois cet optimum trouvé, une forte modification de cette solution est effectuée afin de quitter le bassin d'attraction de la solution actuelle, une nouvelle phase d'exploration.

## Nouvel algorithme d'optimisation

### Nouvelle métaheuristique

L'idée de cette métaheuristique est de réaliser un hill-climbing first-improvement avec une faible perturbation lors d'un optimum local.

### Avantages et inconvénients

Possibilité de trouver un optimum local en en temps assez faible comme le hill-climbing first improvement, mais une chance plus faible de rester coincé dans un optimum local avec un faible "score".

Les résultats peuvent cependant être toujours inférieurs au best improvement, et cet algorithme est donc plus lent que le hill-climbing first improvement.

### Protocole expérimental

Exécuter cet algorithme sur différents ensembles de données de différentes tailles, avec différentes tailles de bassin d'attractions, et ce une centaine de fois.

Les résultats devraient être en général meilleur que le hill-climbing first improvement, en étant seulement légèrement plus lent.
