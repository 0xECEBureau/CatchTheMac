import socket
import threading

HOST = '0.0.0.0'
PORT = 5000
FLAG = "MAC{CH4R4D3_M4ST3R_D3PUS_2003}"

WELCOME = """Figure mystique du fort du cyberspace, Mac Fouras a remplacé ses énigmes par des charades techniques...
Connecte-toi à son service et prouve que tu es digne du flag.

🗝️ Un seul mot d'ordre : pas d'erreur, sinon la connexion est rompue !
<user> """

CHARADES = [
    ('Mon premier supporte la tête. Au Cambodge, vous paierez vos achats avec mon second. "Courrier électronique" est synonyme de mon tout.','Courriel'),
    ("Mon premier est l’acronyme de “HyperText Transfer Protocol”.\nMon second est le port standard pour les connexions chiffrées.\nMon tout est le protocole HTTP sécurisé.", "HTTPS"),
    ("Mon premier est contraire de vrai.\nNe pas abuser de mon second, eau-de-vie de canne à sucre !\nVous pouvez échanger vos idées sur mon tout, groupe de discussion sur Internet.", "Forum"),
    ('"Voir" au passé simple représente mon premier.\nMon second s’écrit avec l’alphabet cyrillique.\nMon tout nuit aux logiciels non-malveillants.', "Virus"),
    ("Mon premier est carrossable.\nMon second a pour synonyme prêt-à-monter.\nMon tout est un logiciel malveillant qui crée une porte dans une machine et la maintient ouverte.", "Rootkit"),
]

def handle_client(conn, addr):
    print(f"[+] Connexion établie depuis {addr}")
    try:
        conn.sendall(WELCOME.encode() + b"\n")

        for idx, (question, expected_answer) in enumerate(CHARADES, 1):
            prompt = f"\nCharade {idx} :\n{question}\nTa réponse : "
            conn.sendall(prompt.encode())

            response = conn.recv(1024)
            if not response:
                break
            response = response.decode().strip()

            if response.lower() != expected_answer.lower():
                conn.sendall("Mauvaise réponse. Connexion terminée.\n".encode())
                print(f"[-] Mauvaise réponse de {addr} à la charade {idx}")
                return
            
            conn.sendall("Bonne réponse !\n".encode('utf-8'))

        conn.sendall(f"\nBravo ! Voici ton flag : {FLAG}\n".encode())

    except Exception as e:
        print(f"[!] Erreur avec {addr}: {e}")
    finally:
        conn.close()
        print(f"[*] Connexion fermée pour {addr}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[+] Serveur démarré sur {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
