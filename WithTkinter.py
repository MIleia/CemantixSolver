import requests
import time
import json
import tkinter as tk
from tkinter import ttk

# Configuration de base
BASE_URL = "https://cemantix.certitudes.org/score"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Accept": "*/*",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://cemantix.certitudes.org",
    "Referer": "https://cemantix.certitudes.org/",
}


# Chargement du dictionnaire
def load_words(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file]


# Sauvegarde du dictionnaire mis à jour
def save_words(words, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("\n".join(words))


# Envoyer une requête pour tester un mot
def test_word(word):
    try:
        response = requests.post(
            BASE_URL,
            headers = HEADERS,
            data = {"word": word},
            timeout = 10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erreur: Statut HTTP {response.status_code} pour le mot '{word}'")
            return None
    except Exception as e:
        print(f"Erreur lors de la requête pour le mot '{word}': {e}")
        return None


# Fenêtre Tkinter
def setup_gui():
    root = tk.Tk()
    root.title("Classement des mots (temps réel)")

    tree = ttk.Treeview(root, columns=("Word", "Percentile", "Score"), show="headings")
    tree.heading("Word", text="Mot")
    tree.heading("Percentile", text="Percentile")
    tree.pack(expand=True, fill="both")

    quit_button = tk.Button(root, text="Quitter", command=root.destroy)
    quit_button.pack()

    return root, tree


# Insertion du mot dans le tableau en fonction de son percentile
def insert_in_order(tree, word, percentile):
    rows = tree.get_children()
    inserted = False

    for i, row in enumerate(rows):
        row_values = tree.item(row, "values")
        current_percentile = int(row_values[1])

        if percentile > current_percentile:
            tree.insert("", i, values=(word, percentile))
            inserted = True
            break

    if not inserted:
        tree.insert("", "end", values=(word, percentile))



def main():
    dictionnaire = "liste_francais.txt"
    words = load_words(dictionnaire)
    results = []
    original_word_count = len(words)
    root, tree = setup_gui()

    for word in words:
        print(f"Test du mot : {word}")
        result = test_word(word)

        if result:
            if "percentile" in result and result["percentile"] == 1000:
                print(f"🎉 Mot du jour trouvé : '{word}' !")
                print(f"Détails de la réponse : {result}")

                # Ajout du résultat au tableau
                insert_in_order(tree, word, result["percentile"])

                # Sauvegarde
                with open("results.json", "w", encoding="utf-8") as file:
                    results.append({"word": word, "response": result})
                    json.dump(results, file, ensure_ascii=False, indent=4)
                break


            elif "error" in result and "Je ne connais pas le mot" in result["error"]:
                print(f"Le mot '{word}' est inconnu, il sera supprimé du dictionnaire.")
                words.remove(word)
                save_words(words, dictionnaire)
            else : # Ajout du mot ayant un percentile
                if "percentile" in result:
                    print(f"Réponse : {result}")
                    results.append({"word": word, "response": result})
                    insert_in_order(tree, word, result["percentile"])
                    root.update()
        else:
            print(f"Le mot '{word}' n'a pas pu être testé.")

    print(f"Script terminé. {len(words)} mots restants dans le dictionnaire (sur {original_word_count}).")

    if not any("percentile" in r.get("response", {}) and r["response"]["percentile"] == 1000 for r in results):
        print("Le mot du jour n'a pas été trouvé. Réessayez avec un dictionnaire mis à jour !")
    root.mainloop()



if __name__ == "__main__":
    main()

