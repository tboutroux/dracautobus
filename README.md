# Pokedex - Projet Python avec Flask

## Description

Ce projet est une application web développée avec Flask qui permet aux utilisateurs d'explorer les 151 premiers Pokémon de l'univers Pokémon, de créer des équipes personnalisées et de les utiliser dans des combats. L'interface utilisateur est réactive et intuitive, grâce à l'utilisation des WebSockets pour mettre à jour dynamiquement les données en temps réel.

---

## Fonctionnalités principales

1. **Affichage de la liste des Pokémon** :
   - Chargement et affichage des 151 premiers Pokémon sous forme de cartes.
   - Chaque carte inclut l'image, le nom et un accès rapide à plus de détails.

2. **Recherche et navigation** :
   - Une barre de recherche permet de filtrer les Pokémon par nom en temps réel.
   - Navigation simple avec des boutons "Précédent" et "Suivant".

3. **Détails des Pokémon** :
   - En cliquant sur une carte, une vue détaillée s'ouvre, affichant les caractéristiques principales :
     - Nom, taille, poids, expérience de base, types, capacités.
     - Statistiques représentées sous forme de barres de progression.

4. **Gestion d'équipe** :
   - Les utilisateurs peuvent :
     - Ajouter jusqu'à 5 Pokémon à leur équipe.
     - Retirer des Pokémon de leur équipe.
   - Les équipes sont persistantes entre les sessions.

5. **Page "Jouer"** :
   - Permet de définir un nom pour le joueur.
   - Affiche l'équipe actuelle du joueur.

6. **Système de combat** :
   - Permet de simuler un combat entre deux équipes de 5 Pokémon.
   - la deuxième équipe est celle d'un bot.
   - Pour jouer, rien de plus simple, voici les méchaniques :
         - Par défaut le pokémon envoyer ce le premier de votre équipe cependant vous pouvez changer au cours de la partie en appuyant sur "envoyer au combat" sur l'un des pokémon encore en vie.
         - Pour attaquer, il vous suffit de séléctionner l'une des compétences de votre pokémon.
         - Prennez en compte que le calcul des dommages est basé sur les règles suivantes :
                - Les types des pokémons influent sur vos dégats et vos résistances (l'herbe ne résiste pas au feu et le feu à l'eau etc).
                - La statistique de résistance de votre pokémon entre aussi en compte.
                - Concernant l'attaque, elle est basée sur votre statistique s'attaque ainsi que la puissance de votre compétence.
                - Les pokémons ne sont pas affectés par les status (poison, enflammé, sommeil etc)
   - Une fois les pokémons de l'équipe adverse battues, vous gagnez !

---

## Installation

1. Clonez le projet :
   ```bash
   git clone <url-du-repo>
   cd <dossier-du-projet>
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancer l'application Flask :
   ```bash
   flask run
   ```

4. Accédez à l'application dans votre navigateur à l'adresse [http://localhost:5000](http://localhost:5000).

---

## Détails techniques

- **Backend** :
  - Utilise Flask comme framework web.
  - Les routes principales incluent :
    - `/`: Affiche la page d'accueil avec la liste des Pokémon.
    - `/play`: Permet de gérer l'équipe du joueur.
    - `/pokemon/<id>`: Affiche les détails d'un Pokémon spécifique.

- **Frontend** :
  - Développé en HTML, CSS et JavaScript.
  - Utilisation de WebSockets pour une mise à jour dynamique des données.

- **API** :
  - Les données sont récupérées via [PokeAPI](https://pokeapi.co/).

---

## Utilisation

1. **Page d'accueil** :
   - Parcourez les Pokémon ou recherchez un Pokémon spécifique via la barre de recherche.

2. **Page "Jouer"** :
   - Définissez un nom de joueur.
   - Gérez votre équipe en ajoutant ou en supprimant des Pokémon.

3. **Combat** :
   - Sélectionnez une équipe et affrontez une autre équipe.

---

## Choix techniques

- **WebSockets** : Permet de mettre à jour les cartes Pokémon en temps réel sans recharger la page.
- **Session Flask** : Assure la persistance des données du joueur et de son équipe.
- **Multithreading** : Optimise les requêtes simultanées vers l'API Pokémon.
