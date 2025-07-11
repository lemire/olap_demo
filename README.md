# OLAP sur la base de données shunshine

La base de données Sunshine de l’Ontario, officiellement appelée Public Sector Salary Disclosure (divulgation des salaires du secteur public), est une liste annuelle publiée par le gouvernement de l’Ontario, conformément à la Public Sector Salary Disclosure Act de 1996. Elle recense les employés du secteur public et des organisations financées par la province qui gagnent un salaire de 100 000 $ ou plus par an. Cette initiative vise à promouvoir la transparence et la responsabilité dans l’utilisation des fonds publics.
Nous pouvons utiliser cette base de données pour tester des requêtes OLAP.

## Prérequis

Avant de procéder, assurez-vous d'installer Python 3.7 ou une version ultérieure sur votre machine.

- **Pour Windows** :
  1. Téléchargez l'installateur depuis https://www.python.org/downloads/windows/
  2. Lancez l'installateur et cochez l'option "Add Python to PATH" avant de cliquer sur "Install Now".
  3. Ouvrez l'invite de commandes :
     - Cliquez sur le menu Démarrer (icône Windows en bas à gauche), tapez "Invite de commandes" ou "cmd", puis cliquez sur l'application correspondante.
  4. Vérifiez l'installation en tapant :
     ```
     python --version
     ```
     ou
     ```
     python3 --version
     ```

- **Pour macOS** :
  1. Ouvrez le Terminal.
  2. Installez Homebrew si ce n'est pas déjà fait :
     ```
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```
  3. Installez Python 3 avec Homebrew :
     ```
     brew install python
     ```
  4. Vérifiez l'installation :
     ```
     python3 --version
     ```

Le nom de l'interpréteur Python sur votre système peut être `python` ou `python3` selon votre système. 


## Obtention des fichiers du projet

Pour obtenir les fichiers du projet, vous pouvez télécharger une archive ZIP depuis GitHub :

1. Rendez-vous sur la page du projet : https://github.com/lemire/olap_demo
2. Cliquez sur le bouton vert « Code » puis sur « Download ZIP ».
3. Décompressez l’archive téléchargée sur votre ordinateur.
4. Ouvrez le dossier extrait dans votre terminal ou explorateur de fichiers pour suivre les instructions d’installation ci-dessus.

## Création de la base de données


Placez-vous dans le répartoire principal du projet. La commande

```bash
python python/create.py  data/tbs-pssd-compendium-salary-disclosed-2024-en-utf-8-2025-03-26.csv database.bin
```

ou 

```bash
python python/create.py  data/tbs-pssd-compendium-salary-disclosed-2024-en-utf-8-2025-03-26.csv database.bin
```

devrait créer une base de données "database.bin" normalisée.





## Description du schéma de la base de données

La base de données est conçue pour gérer les informations des employés du secteur public, en se concentrant sur leurs employeurs, leurs données personnelles et leurs rémunérations annuelles. Elle comprend quatre tables principales : `employers`, `individuals`, `salaries` et une table système `sqlite_sequence`. La table `employers` stocke les informations sur les employeurs, avec un identifiant unique (`employer_id`), le nom de l'employeur (`employer_name`) et son secteur d'activité (`sector`), garantissant l'unicité de la combinaison nom-secteur. La table `individuals` recense les employés avec un identifiant unique (`individual_id`), leur nom de famille (`last_name`), prénom (`first_name`) et titre de poste (`job_title`), avec une contrainte d'unicité sur ces trois champs pour éviter les doublons. Des index sont définis sur `individuals.last_name`, `salaries.employer_id` et `salaries.individual_id` pour optimiser les requêtes.

La table `salaries` est le cœur de la base, reliant les employeurs et les employés via leurs identifiants (`employer_id` et `individual_id`) pour enregistrer les salaires (`salary`), avantages (`benefits`) et l'année (`year`). Une clé primaire composite sur `employer_id`, `individual_id` et `year` assure l'unicité des enregistrements annuels. Les clés étrangères établissent des relations avec les tables `employers` et `individuals`, garantissant l'intégrité référentielle. La table `sqlite_sequence` est utilisée par SQLite pour gérer les séquences des clés primaires auto-incrémentées. Ce schéma normalisé permet des requêtes efficaces sur les données salariales tout en maintenant une structure claire et cohérente.




## Table employers
- **employer_id** : INTEGER, clé primaire, auto-incrémenté
- **employer_name** : TEXT, nom de l'employeur, non nul
- **sector** : TEXT, secteur d'activité, non nul
- **Contrainte** : UNIQUE(employer_name, sector)

## Table sqlite_sequence
- **name** : TEXT, nom de la table
- **seq** : INTEGER, valeur de la séquence
- **Description** : Gère les séquences pour les clés primaires auto-incrémentées

## Table individuals
- **individual_id** : INTEGER, clé primaire, auto-incrémenté
- **last_name** : TEXT, nom de famille, non nul
- **first_name** : TEXT, prénom, non nul
- **job_title** : TEXT, titre de poste, non nul
- **Contrainte** : UNIQUE(last_name, first_name, job_title)
- **Index** : idx_individuals_last_name ON last_name

## Table salaries
- **employer_id** : INTEGER, clé étrangère référençant employers(employer_id)
- **individual_id** : INTEGER, clé étrangère référençant individuals(individual_id)
- **year** : INTEGER, année, non nul
- **salary** : REAL, salaire, non nul
- **benefits** : REAL, avantages, non nul
- **Clé primaire** : (employer_id, individual_id, year)
- **Index** : idx_salaries_employer_id ON employer_id
- **Index** : idx_salaries_individual_id ON individual_id


## Requêtes OLAP


Lancez les requêtes avec la commande

```bash
python3 python/olap.py database.bin
```

ou 


```bash
python python/olap.py database.bin
```

## Résultat attendu

```

Roll-up (moyenne des salaires par secteur et année):
Secteur                                                  | Année | Salaire moyen     
-------------------------------------------------------------------------------------
Colleges                                                 | 2024  | 127213.46445178571
Crown Agencies                                           | 2024  | 134380.20016608812
Government of Ontario - Judiciary                        | 2024  | 252989.33872592592
Government of Ontario - Legislative Assembly and Offices | 2024  | 142334.92651771958
Government of Ontario - Ministries                       | 2024  | 130698.8821660054 
Hospitals & Boards of Public Health                      | 2024  | 125066.36676918289
Municipalities & Services                                | 2024  | 129788.75211054421
Ontario Power Generation                                 | 2024  | 167894.5876068959 
Other Public Sector Employers                            | 2024  | 133772.4451449602 
School Boards                                            | 2024  | 127747.39465499842
Seconded (Attorney General)*                             | 2024  | 184807.78         
Seconded (Children, Community and Social Services)*      | 2024  | 132979.16999999998
Seconded (Citizenship and Multiculturalism)*             | 2024  | 129375.29999999999
Seconded (Education)*                                    | 2024  | 140793.70596774193
Seconded (Health)*                                       | 2024  | 351025.75666666665
Seconded (Natural Resources and Forestry)*               | 2024  | 124451.66666666667
Seconded (Solicitor General)*                            | 2024  | 134213.20249999998
Seconded (Tourism, Culture and Sport)*                   | 2024  | 164468.33333333334
Universities                                             | 2024  | 162657.09051503617

Drill-down (moyenne des salaires par employeur dans le secteur Technologie):
Aucune donnée trouvée.

Dice (salaires des employés avec 'software' dans le titre pour employeurs commençant par 'Ontario'):
Nom               | Prénom          | Employeur                                                 | Salaire  
-----------------------------------------------------------------------------------------------------------
Aghababyan        | Aleksandr       | Ontario Health                                            | 117423.12
Arab              | Mahmood-Reza    | Ontario Health                                            | 104898.8 
Arthur            | John            | Ontario Health                                            | 105410.58
Bai               | Sheng           | Ontario Health                                            | 127605.91
Balayan           | Madhusudhan     | Ontario Health                                            | 105410.57
Batista Freijanes | Alejandro       | Ontario Health                                            | 120548.05
Bedi              | Deep Singh      | Ontario Health                                            | 114571.47
Blaga             | Lucian          | Ontario Health                                            | 104423.52
Bodean            | Petrisor R      | Ontario Health                                            | 104387.11
Bordun            | Sergiy          | Ontario Health                                            | 105410.55
Broytman          | Dmitry          | Ontario Educational Communications Authority (TV Ontario) | 101984.95
Bui               | Duyen           | Ontario Health                                            | 107613.15
Cacenco           | Vladimir M      | Ontario Health                                            | 121866.92
Cerelli           | Nancy           | Ontario Educational Communications Authority (TV Ontario) | 106446.4 
Chau              | David W         | Ontario Health                                            | 120589.69
Chau              | Johnson         | Ontario Health                                            | 108688.7 
Chawla            | Kartik          | Ontario Health                                            | 104387.13
Chen              | Hui             | Ontario Health                                            | 119960.03
Cheng             | Manchung        | Ontario Health                                            | 106864.76
Cong              | Peijun          | Ontario Health                                            | 128683.8 
Dasanayaka        | Sandaruwan      | Ontario Health                                            | 104898.88
Dehghani          | Daryoosh        | Ontario Health                                            | 107457.34
Deneweth          | Glenn           | Ontario Health atHome                                     | 120068.42
Dinesan           | Priya           | Ontario Health                                            | 107749.48
Durson            | Indra           | Ontario Health                                            | 124474.92
El-Hallak         | Walid           | Ontario Health                                            | 122811.21
Ferguson          | Brandon A       | Ontario Health                                            | 105410.56
Fonseka           | Chandima        | Ontario Health                                            | 116154.39
Fu                | Bing            | Ontario Health                                            | 120589.65
Ghafouri          | Behnam          | Ontario Cannabis Retail Corporation                       | 131535.9 
Goodine           | Richard         | Ontario Educational Communications Authority (TV Ontario) | 106387.31
Han               | Hao Peter       | Ontario Health                                            | 121380.11
Haque             | Syed Mairajul   | Ontario Health                                            | 104387.18
Hawkins           | Jennifer        | Ontario Health                                            | 105849.64
He                | Yubo            | Ontario Health                                            | 105410.55
Hloba             | Yevhen          | Ontario Health                                            | 114532.48
Hoad              | Christian       | Ontario Educational Communications Authority (TV Ontario) | 106451.81
Hu                | Xiaodong        | Ontario Health                                            | 110385.55
Huang             | Jian            | Ontario Health                                            | 121224.79
Hudson            | Warren          | Ontario Health                                            | 109612.07
Hui               | Michael         | Ontario Health                                            | 140709.72
Jacobs            | Leo             | Ontario Cannabis Retail Corporation                       | 153583.31
Jing              | Li              | Ontario Health                                            | 112857.61
Jose              | Jane Elizabeth  | Ontario Health                                            | 104865.46
Joukova           | Tatiana         | Ontario Health                                            | 133926.45
Kalambet          | Igor            | Ontario Health                                            | 136751.38
Kanagasabapathy   | Balakumar       | Ontario Health                                            | 100890.46
Kim               | Hongwan         | Ontario Health                                            | 122800.38
Kim               | Kwonil          | Ontario Health                                            | 126277.13
Kim               | Sae-Il          | Ontario Health                                            | 127470.99
Kolhe             | Pradnya         | Ontario Health                                            | 124778.55
Kulkarni          | Hrishikesh      | Ontario Lottery And Gaming Corporation                    | 157184.41
Kurian            | Liza            | Ontario Health                                            | 104387.17
Lam               | Kam Chuen       | Ontario Health                                            | 116905.44
Lee               | Michelle        | Ontario Educational Communications Authority (TV Ontario) | 110343.33
Lee               | Simon           | Ontario Health                                            | 105410.54
Lennox            | Keith           | Ontario Educational Communications Authority (TV Ontario) | 104007.95
Li                | Jie             | Ontario Health                                            | 108578.87
Lim               | Reayen Ron      | Ontario Health                                            | 124464.49
Lin               | Hai             | Ontario Health                                            | 106365.87
Lin               | Shaole          | Ontario Health                                            | 120589.64
Liu               | Gang            | Ontario Health                                            | 105410.61
Liu               | Michael         | Ontario Health                                            | 105410.54
Liu               | Xin             | Ontario Health                                            | 105410.54
Lou               | Dong            | Ontario Health                                            | 104963.77
Ma                | Chenghua        | Ontario Health                                            | 111141.78
Ma                | Yuefei          | Ontario Health                                            | 120589.69
Maserrat          | Abdol           | Ontario Health                                            | 130850.48
Mikesewala        | Yasmin          | Ontario Health                                            | 105410.58
Nanushi           | Valentina       | Ontario Health                                            | 147829.93
Naseer            | Muhammad        | Ontario Health                                            | 120589.66
Niazmand          | Najla           | Ontario Health                                            | 120636.89
Pala              | Bharathi Alisha | Ontario Health                                            | 106716.38
Park              | Jeesun          | Ontario Health                                            | 120589.63
Parmar            | Shailendrasinh  | Ontario Health                                            | 110163.2 
Perera            | Thenkuttige     | Ontario Health                                            | 106350.72
Qin               | Bill            | Ontario Health                                            | 134632.4 
Rygiel            | Mateusz         | Ontario Health                                            | 122312.24
Sazonova          | Lioudmila       | Ontario Health                                            | 105410.57
Scaletchi         | Victor          | Ontario Health                                            | 121323.66
Sedighi           | Amir            | Ontario Health                                            | 149957.12
Shaik             | Nazia B         | Ontario Educational Communications Authority (TV Ontario) | 103889.38
Shi               | Hang            | Ontario Health                                            | 129335.48
Singh             | Dalveer         | Ontario Health                                            | 104898.93
Sivarasathurai    | Latheesan       | Ontario Health                                            | 121760.4 
Stark             | Corey           | Ontario Health                                            | 104898.87
Stewart           | Ashley          | Ontario Health                                            | 150389.73
Sun               | Wei             | Ontario Health                                            | 120589.63
Sun               | Zhu Wen         | Ontario Health                                            | 105410.56
Syal              | Ashish          | Ontario Health                                            | 104898.81
Taylor            | Shirley         | Ontario Health                                            | 111692.55
Tran              | Chi-Lea         | Ontario Educational Communications Authority (TV Ontario) | 105681.06
Waita             | Naomi           | Ontario Health                                            | 104898.77
Wang              | Jason           | Ontario Health                                            | 106904.68
Wang              | Shanshan        | Ontario Health                                            | 140274.88
Wang              | Xiaomei         | Ontario Health                                            | 124858.21
Wang              | Yongzhong       | Ontario Health                                            | 109278.06
Wen               | Xinhua          | Ontario Health                                            | 124876.97
Wiszniewski       | Sebastian       | Ontario Health                                            | 127770.24
Xie               | Ting            | Ontario Health                                            | 113578.95
Xu                | Cong            | Ontario Health                                            | 119418.86
Xu                | Hai Yan         | Ontario Cannabis Retail Corporation                       | 139524.89
Yamada            | Joseph          | Ontario Health                                            | 129529.55
Yep               | Daniel          | Ontario Health                                            | 106916.16
Yi                | Jun             | Ontario Health                                            | 106528.55
Zhang             | Linhan          | Ontario Health                                            | 104387.14
Zhang             | Zhen            | Ontario Health                                            | 128492.4 
Zhou              | Gang            | Ontario Health                                            | 121801.65
Zhou              | Jianzhou        | Ontario Cannabis Retail Corporation                       | 127958.97
Zhou              | Ye              | Ontario Health                                            | 104898.83
Zuo               | Rui Song        | Ontario Health                                            | 119418.87

Slice (moyenne des salaires par année pour Pay Equity Commission):
Année | Salaire moyen    
-------------------------
2024  | 137576.0246153846
```

## Explication

Voici les explications des requêtes OLAP utilisées dans le fichier `python/olap.py` :

### 1. Roll-up (Agrégation par secteur et année)
```sql
SELECT e.sector, s.year, AVG(s.salary) as average_salary
FROM salaries s
JOIN employers e ON s.employer_id = e.employer_id
GROUP BY e.sector, s.year
```
Cette requête calcule le salaire moyen par secteur et par année. Elle regroupe les salaires selon le secteur d'activité de l'employeur et l'année, permettant d'obtenir une vue agrégée des rémunérations par secteur public.

### 2. Drill-down (Détail par employeur dans le secteur Technologie)
```sql
SELECT e.employer_name, s.year, AVG(s.salary) as average_salary
FROM salaries s
JOIN employers e ON s.employer_id = e.employer_id
WHERE e.sector = 'Technologie'
GROUP BY e.employer_name, s.year
```
Cette requête affine l'analyse en calculant le salaire moyen par employeur et par année, mais uniquement pour le secteur "Technologie". Elle permet d'identifier les employeurs les plus rémunérateurs dans ce secteur spécifique.

### 3. Dice (Sous-ensemble : employeurs "Ontario" et titres "software")
```sql
SELECT i.last_name, i.first_name, e.employer_name, s.salary
FROM salaries s
JOIN individuals i ON s.individual_id = i.individual_id
JOIN employers e ON s.employer_id = e.employer_id
WHERE e.employer_name LIKE 'Ontario%' AND i.job_title LIKE '%software%'
```
Cette requête extrait les salaires des employés dont le titre de poste contient "software" et dont l'employeur commence par "Ontario". Elle permet de cibler un sous-ensemble précis de la base pour des analyses ciblées.

### 4. Slice (Moyenne des salaires pour "Pay Equity Commission")
```sql
SELECT s.year, AVG(s.salary) as average_salary
FROM salaries s
JOIN employers e ON s.employer_id = e.employer_id
WHERE e.employer_name = 'Pay Equity Commission'
GROUP BY s.year
```
Cette requête calcule le salaire moyen par année pour l’employeur "Pay Equity Commission". Elle réduit la dimensionnalité en se concentrant sur un employeur précis, permettant de suivre l’évolution des salaires dans cette organisation au fil des années.

