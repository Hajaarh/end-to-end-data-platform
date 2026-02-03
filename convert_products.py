import json
import csv
import os

# Configuration
INPUT_FILE = 'api_produits.json'
OUTPUT_FILE = 'data_produits_enriched.csv'

def convert_json_to_csv():
    print(f"🔄 Lecture de {INPUT_FILE}...")
    
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        products = data.get('produits', [])
        
        if not products:
            print("⚠️ Aucune donnée produit trouvée.")
            return

        # Récupération automatique des colonnes (headers)
        headers = list(products[0].keys())
        
        print(f"📝 Écriture de {len(products)} produits dans {OUTPUT_FILE}...")
        
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers, delimiter=',')
            writer.writeheader()
            writer.writerows(products)
            
        print("✅ Conversion terminée avec succès !")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    convert_json_to_csv()