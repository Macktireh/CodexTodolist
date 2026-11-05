# Todolist Tkinter

Une petite application de bureau moderne pour organiser ses tâches. Elle est
écrite en Python 3.14 avec Tkinter, sauvegarde les données en JSON et sépare
l'interface graphique de la logique métier.

## Fonctionnalités

- ajout, modification et suppression d'une tâche ;
- validation et réouverture d'une tâche ;
- priorités, catégories et dates d'échéance ;
- vues Aujourd'hui et Calendrier mensuel ;
- recherche et filtres par état ;
- sauvegarde automatique dans `data/tasks.json` ;
- actualisation automatique si le fichier JSON est modifié extérieurement ;
- dashboard, statistiques et paramètres accessibles depuis une sidebar ;
- graphiques Matplotlib intégrés : activité sur sept jours et taux d'accomplissement ;
- cartes et panneaux aux bords arrondis ;
- interface responsive avec modes large, compact et étroit ;
- interface `ttk` redimensionnable et raccourcis clavier ;
- tests unitaires et d'intégration avec pytest.

## Prérequis

Seul [uv](https://docs.astral.sh/uv/) est nécessaire. La version de Python est
fixée à 3.14 dans `.python-version` et peut être installée automatiquement par
uv.

## Installation et lancement

```powershell
uv sync
uv run python main.py
```

Après l'installation, la commande suivante est également disponible :

```powershell
uv run todolist
```

## Tests

```powershell
uv run pytest
```

## Raccourcis

- `Ctrl+N` : créer une tâche ;
- double-clic : modifier la tâche sélectionnée ;
- `Espace` : valider ou rouvrir la tâche ;
- `Suppr` : supprimer la tâche sélectionnée.
