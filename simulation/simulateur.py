import psycopg2
import time
import random
import sys
from datetime import datetime

# Configuration extraite de Docker Compose
DB_CONFIG = {
    "host": "postgres",
    "port": "5432",
    "database": "app_database",
    "user": "admin",
    "password": "SecureP@ssw0rd2024!"
}

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f"❌ Impossible de se connecter à Postgres : {e}")
        return None

def get_existing_ids(conn):
    cur = conn.cursor()
    cur.execute("SELECT client_id FROM clients;")
    clients = [r[0] for r in cur.fetchall()]
    cur.execute("SELECT produit_id, prix_unitaire FROM produits;")
    products = {r[0]: float(r[1]) for r in cur.fetchall()}
    cur.close()
    return clients, products

def create_fake_order(conn, clients, products):
    try:
        cur = conn.cursor()
        now = datetime.now()
        client_id = random.choice(clients)
        cmd_id = f"CMD-{now.strftime('%H%M%S')}-{random.randint(100, 999)}"
        
        prod_id, price = random.choice(list(products.items()))
        qty = random.randint(1, 3)
        total_ht = price * qty
        tva = total_ht * 0.20
        total_ttc = total_ht + tva + 5.90 

        # Insertion dans 'commandes' - Ajout des champs transporteur/paiement pour la cohérence
        cur.execute("""
            INSERT INTO commandes (commande_id, client_id, date_commande, heure_commande, statut, mode_paiement, transporteur, montant_ht, tva, frais_port, montant_ttc)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (cmd_id, client_id, now.date(), now.strftime("%H:%M:%S"), 'Livrée', 'Carte bancaire', 'UPS', 
              round(total_ht, 2), round(tva, 2), 5.90, round(total_ttc, 2)))

        # Insertion dans 'lignes_commandes'
        lig_id = f"LIG-{cmd_id}-{random.randint(10,99)}"
        cur.execute("""
            INSERT INTO lignes_commandes (ligne_id, commande_id, produit_id, quantite, montant_ligne)
            VALUES (%s, %s, %s, %s, %s)
        """, (lig_id, cmd_id, prod_id, qty, round(total_ht, 2)))
        
        conn.commit()
        cur.close()
        print(f" [{now.strftime('%H:%M:%S')}] New Order: {cmd_id} | Total: {total_ttc:.2f} €")
    except Exception as e:
        print(f"Erreur lors de l'insertion : {e}")
        conn.rollback()

def main():
    print("Démarrage du simulateur temps réel...")
    conn = None
    while conn is None:
        conn = get_db_connection()
        if conn is None: time.sleep(5)

    clients, products = get_existing_ids(conn)
    
    while True:
        try:
            create_fake_order(conn, clients, products)
            time.sleep(random.randint(2, 5)) # Accélération pour voir le dashboard bouger
        except Exception:
            print("Reconnexion en cours...")
            conn = get_db_connection()

if __name__ == "__main__":
    main()