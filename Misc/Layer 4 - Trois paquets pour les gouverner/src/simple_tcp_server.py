import socket

HOST = '0.0.0.0'
PORT = 5000
FLAG = "MAC{you_speak_tcp}"

WELCOME = """Bienvenue sur le service de Mac.
Seuls ceux qui connaissent le langage du transport peuvent continuer...
Commencez par parler.
Utilisez le bon protocole.
<user> """

print(f"[+] Serveur démarré sur {HOST}:{PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[+] Connexion établie depuis {addr}")
            try:
                conn.sendall(WELCOME.encode())
                state = 0  # 0 = attente SYN, 1 = attente ACK
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode().strip()
                    if state == 0 and message == "SYN":
                        conn.sendall(b"<srv> SYN-ACK\n<user> ")
                        state = 1
                    elif state == 1 and message == "ACK":
                        conn.sendall((FLAG + "\n").encode())
                        break
                    else:
                        conn.sendall(b"<server> Tu ne maitrise pas mon language...<\nuser> ")
            except Exception as e:
                print(f"[!] Erreur: {e}")
            finally:
                conn.close()
                print("[*] Connexion fermee.")