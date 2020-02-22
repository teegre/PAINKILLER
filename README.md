# RELIEF

## Description
**RELIEF** est un jeu de combat au tour par tour dont tous les aspects sont gérés par des dés.  
Le but du jeu est de vaincre **CIPAATL**, un boss surpuissant.

## 1. Combats

### 1.1 Préambule

Le **joueur** débute l'aventure avec **deux dés 6** qui détermineront la valeur des **attaques** portées à l'adversaire, et **un dé 6** pour la **défense**.  
Ses **PV** sont au nombre de **100**, son **agilité** *(caractéristique utilisée pour déterminer le succès d'une attaque)* est de **2** et sa **faculté d'auto-guérison** est de **10% des PV max**.  
De plus, il obtient une *capsule* aléatoire à chaque début de combat (voir plus bas).

### 1.2 Déroulement

***Avertissement**: la décision de qui débute le combat est prise aléatoirement ! (1 chance sur 2)*

Le joueur dispose au départ des *capsules* *attaque* et *bouclier* et d'une *capsule* aléatoire (cf. 2.).  
Les combattants n'ont droit qu'à une seule action par tour.
La force correspondant au nombre de dés (N) et le niveau déterminant le nombre de faces d'un dé (F), la valeur d'un attaque est égale au lancé de N dés à F faces.  
Si lors du lancé, tous les dés ont une valeur égale à F, alors le résultat est doublé (**attaque chance**).  
Il en est de même lors de l'utilisation du bouclier.
Chaque fois que des dégats sont reçus par l'un ou l'autre des protagonistes, leur jauge de *douleur* se remplit.  
Lorsque le niveau de *douleur* atteint les 100%, il est possible de la *libérer* en effectuant un attaque devastatrice et ainsi de la remettre à zéro.  
Cette attaque permet également de récupérer un certain pourcentage de ses PV max égal (auto-guérison).  
Soit P le pourcentage de douleur, la valeur d'une attaque *libérer* est égale au lancé de N dés à F faces x P
Mais attention ! La déclencher peut faire augmenter drastiquement la jauge de *douleur* de l'adversaire, **la *douleur* pouvant être accumulée bien au-delà de 100%**.  
L'adversaire n'hésitera pas à attaquer s'il est sûr de vous tuer.
A utiliser avec précaution donc...  

A noter que le joueur conserve son niveau de douleur entre les combats, hormis lorsqu'il augmente d'un niveau.

Le **boss** se montrera si le joueur est assez puissant pour l'affronter.

### 1.3 Fin du combat

À chaque victoire remportée, le joueur peut choisir de :

- récupérer tous ses PV
- augmenter ses points de vie maximum (+25)
- augmenter sa force (+1 dé)
- augmenter sa défense (+1 dé)
- garder la *capsule* obtenue en début de combat.

Tous les 5 combats gagnés, le joueur gagne un niveau supplémentaire :

- Soin
- Douleur remise à 0
- PV max +25
- attaque +1 dé
- défense +1 dé
- agilité +1
- auto-guérison +5%
- 1 face supplémentaire pour tous les dés
- +1 dé pour la capsule *poison* si elle est en sa possession

### 1.4 Fin du jeu

Le jeu se termine lorsque les PV du joueur atteignent 0 ou si le joueur réussit à vaincre le boss.

Il est possible de rejouer la partie précédente si le joueur a été tué.


## 2. Capsules

Une capsule est un objet qui octroie des capacités supplémentaires.  
En voici une liste exhaustive :

- **Attaque** → attaque normale. OK
- **Libérer** → attaque spéciale. OK
- **Bouclier** → défense. OK
- **Poison** → inflige des dégats de poison dont la valeur maximum est égale la force du joueur x le nombre de faces de ses dés. A chaque tour la valeur diminue de 1. (réutilisable) OK
- **Calmant** → apaise la douleur de l'adversaire (réutilisable). OK
- **Morphine** → rend l'adversaire insensible à la douleur de la prochaine attaque (réutilisable).
- **Furie** → augmente la jauge de douleur de 200% (ou 100% si la capsule Berserk est détenue par le joueur) (1 fois par combat). OK
- **Miroir** → retourne l'attaque de l'adversaire (réutilisable). OK
- **Mur** → bloque la prochaine attaque (réutilisable). OK
- **Démolition** → casse l'armure de l'adversaire et inflige une attaque normale (réutilisable). OK
- **Paralysie** → l'adversaire est immobilisé jusqu'à ce qu'il subisse des dégats directs (réutilisable). OK
- **Accolade** → réduit la douleur de l'adversaire à 0 et lui ajoute 10% de ses PV max (1 fois par combat). OK
- **Empathie** → la jauge de douleur augmente également lorsque le joueur inflige des dégats à l'adversaire. OK
- **Berserk** → les dégats infligés sont doublés, mais la douleur n'augmente pas (si activé, dure jusqu'à la fin du combat). OK
- **Bombe** → aprés un nombre de tours défini au préalable, le personnage sacrifie le reste de ses PV et inflige autant de dégats à l'adversaire. OK
- **Sacrifice** → le personnage sacrifie tous ses PV sauf 1 et tue l'adversaire. OK
- **Sangsue** → absorbe les dégats infligés à l'adversaire et diminue la douleur du joueur. OK
- **Charité** → le joueur offre une partie de ses PV, apaise la douleur de l'adversaire et augmente la sienne. OK
- **Carapace** → le joueur est invincible tant qu'il n'attaque pas (octroie l'ajout d'une capsule supplémentaire **Passe**).
- **Passe** → le joueur peut passer son tour (action contenue dans la capsule **Carapace**, ne peut être vendue séparément). OK
- **Stéroïdes** → la force est démultipliée (améliorable) (1 fois par combat). OK
- **Fuite** → donne la possibilité de fuir un combat. OK
- **Prudence** → la valeur de l'attaque portée est ajoutée au bouclier. OK
- **Régénère**
- **Endurer** → pas de dégats subis mais la douleur est ressentie (1 fois par combat)

## 3. Statistiques et valeurs par défaut

|Caractéristique | Valeur
|:---------------|:------
|PV              |100
|PV max          |100
|Force           |2x6
|Défense         |1x6
|Agilité         |2
|Auto-guérison   |10% des PV max


## 4. Python Classes

There are two classes in this game: Character and Capsule.  
Basically, a character is given some capsules that he can use.  
Depending on the capsule type, it can be used for immediate effect, like *attack* and *shield*  
or it can be attached so it will be effective only when the character or his opponent takes action (ie. *poison*, *wall*).  
The latter are called *active capsules*

### 4.1 CHARACTER

#### 4.1.1 Properties

|Property         |Description               |Type    |Default value
|:----------------|:------------------------|:-------|:------------
|name             |character's name         |str     |None
|type             |character type (optional)|str     |None
|level            |character's level: determine dice side count (level + 5 = sides) |int |1
|maxhp            |max health points |int |100
|hp               |health point|int |100
|strength         |dice count |int | 1
|defense          |dice count |int | 1
|agility          |ability to succeed an attack |int |1
|self_healing     |ability to heal after performing a *relieve* attack |int |10
|immunity         |capsules without effect on the character |list | []
|str_mul          |strength multiplier |int |1
|def_mul          |defense multiplier |int |1
|shield           |actual shield value |int |0
|pain             |actual pain value |int |0
|p_pain           |actual pain percentage |int |0
|capsules         |owned capsules |list |[]
|active_c         |active capsules |list |[]
|damage_taken     |total damage taken |int |0
|damage_done      |total damage done |int |0
|sides            |dice side count |int |level + 5
|is_in_pain       |is character in pain? |bool |False
|actions          |list of available actions |list |[]

#### 4.1.2 Methods

- roll
- success
- lucky
- can_kill
- is_immune
- add_immunity
- activate_capsules
- activate_capsule
- deactivate_capsules
- deactivate_capsule
- drop_capsules
- drop_capsule
- attach_capsule
- detach_capsules
- detach_capsule
- add_capsule
- use_capsule
- get_capsule
- has_capsule
- is_capsule_active
- get_caps_df
- get_caps_desc
- capsule_trigger
- heal
- hurt
- hpup
- levelup
- reset

### 4.3 CAPSULE

#### 4.3.1 Properties

|Property |Description |Type |Default value
|:-------|:-----------|:-----|:------------
|name |capsule name |str |capsule
|description |capsule description|str |this is an empty capsule
|d_target |default target: can be either self or other|str |empty
|active |if True, capsule appears in character's action list|bool |True
|owner |character |Character |None
|target |character |Character| None

#### 4.3.2 Methods

- use
- attach
- detach
- activate
- deactivate
- on_activate
- on_deactivate
- on_attach
- on_detach
- effect
- upgrade
- reset

## Zones intermédiaires
???
