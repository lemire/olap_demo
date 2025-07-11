import sqlite3

def print_table(rows, headers):
    if not rows:
        print("Aucune donnée trouvée.")
        return
    
    # Calculer la largeur maximale pour chaque colonne
    widths = [len(header) for header in headers]
    for row in rows:
        for i, value in enumerate(row):
            widths[i] = max(widths[i], len(str(value)))
    
    # Afficher l'en-tête
    header_row = " | ".join(f"{header:<{widths[i]}}" for i, header in enumerate(headers))
    print(header_row)
    print("-" * len(header_row))
    
    # Afficher les lignes
    for row in rows:
        row_str = " | ".join(f"{str(value):<{widths[i]}}" for i, value in enumerate(row))
        print(row_str)

def perform_olap_operations(db_name):
    # Connexion à la base de données existante
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Roll-up: Agrégation vers un niveau supérieur (moyenne des salaires par secteur et année)
    roll_up_query = """
    SELECT e.sector, s.year, AVG(s.salary) as average_salary
    FROM salaries s
    JOIN employers e ON s.employer_id = e.employer_id
    GROUP BY e.sector, s.year
    """
    cursor.execute(roll_up_query)
    print("\nRoll-up (moyenne des salaires par secteur et année):")
    print_table(cursor.fetchall(), ["Secteur", "Année", "Salaire moyen"])
    
    # Drill-down: Décomposition vers un niveau plus détaillé (moyenne des salaires par employeur)
    drill_down_query = """
    SELECT e.employer_name, s.year, AVG(s.salary) as average_salary
    FROM salaries s
    JOIN employers e ON s.employer_id = e.employer_id
    WHERE e.sector = 'Technologie'
    GROUP BY e.employer_name, s.year
    """
    cursor.execute(drill_down_query)
    print("\nDrill-down (moyenne des salaires par employeur dans le secteur Technologie):")
    print_table(cursor.fetchall(), ["Employeur", "Année", "Salaire moyen"])
    
    # Dice: Sélection d'un sous-ensemble spécifique (salaires pour employeurs 'Ontario' et titres 'software')
    dice_query = """
    SELECT i.last_name, i.first_name, e.employer_name, s.salary
    FROM salaries s
    JOIN individuals i ON s.individual_id = i.individual_id
    JOIN employers e ON s.employer_id = e.employer_id
    WHERE e.employer_name LIKE 'Ontario%' AND i.job_title LIKE '%software%'
    """
    cursor.execute(dice_query)
    print("\nDice (salaires des employés avec 'software' dans le titre pour employeurs commençant par 'Ontario'):")
    print_table(cursor.fetchall(), ["Nom", "Prénom", "Employeur", "Salaire"])
    
    # Slice: Réduction de la dimensionnalité (moyenne des salaires pour 'Pay Equity Commission')
    slice_query = """
    SELECT s.year, AVG(s.salary) as average_salary
    FROM salaries s
    JOIN employers e ON s.employer_id = e.employer_id
    WHERE e.employer_name = 'Pay Equity Commission'
    GROUP BY s.year
    """
    cursor.execute(slice_query)
    print("\nSlice (moyenne des salaires par année pour Pay Equity Commission):")
    print_table(cursor.fetchall(), ["Année", "Salaire moyen"])
    
    # Fermeture de la connexion
    conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: python olap_operations.py <database_name>")
        sys.exit(1)
    db_name = sys.argv[1]
    perform_olap_operations(db_name)