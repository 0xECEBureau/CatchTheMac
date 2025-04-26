#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script Scapy pour générer un fichier PCAP simulant une attaque ARP Spoofing
et un scénario Man-in-the-Middle (MitM).
"""

import os
import random
import time
from scapy.all import (Ether, ARP, IP, TCP, Raw, sendp, wrpcap, conf,
                     get_if_hwaddr, RandShort, RandMAC)

# --- Configuration ---

# Désactiver la verbosité de Scapy pour ne pas afficher les envois de paquets à l'écran
conf.verb = 0

# Fichier PCAP de sortie
PCAP_FILENAME = "arp_spoof_scenario.pcap"

# Configuration réseau
NETWORK = "192.168.1.0/24"
ROUTER_IP = "192.168.1.1"
ROUTER_MAC = "00:aa:bb:cc:dd:ee"

ATTACKER_IP = "192.168.1.13"
ATTACKER_MAC = "00:1a:cd:ef:42:00"

VICTIM_IP = "192.168.1.10"
VICTIM_MAC = "00:11:22:33:44:55"

# Nombre d'autres machines légitimes
NUM_OTHER_MACHINES = 4
# Plage d'IP pour les machines légitimes (hors routeur, attaquant, victime)
LEGIT_IP_RANGE_START = 11 # Commencer après la victime
LEGIT_IP_RANGE_END = 19    # Limite supérieure

# Paramètres de simulation
NUM_INITIAL_NORMAL_ROUNDS = 5  # Nombre de cycles de trafic normal avant l'attaque
NUM_MITM_ROUNDS = 10            # Nombre de cycles de trafic pendant la phase MitM
MIN_DELAY = 0.05                # Délai minimum entre les paquets/groupes (secondes)
MAX_DELAY = 0.5                 # Délai maximum entre les paquets/groupes (secondes)

# --- Variables globales ---
packets = [] # Liste pour stocker tous les paquets générés
current_time = time.time() # Temps de départ pour l'horodatage des paquets

# --- Fonctions utilitaires ---

def get_random_delay():
    """Retourne un délai aléatoire dans la plage définie."""
    return random.uniform(MIN_DELAY, MAX_DELAY)

def add_packet(pkt):
    """Ajoute un paquet à la liste globale avec un horodatage incrémental."""
    global current_time
    # Ajoute un petit délai aléatoire pour simuler la gigue réseau
    current_time += get_random_delay() / 10.0 # Délai plus petit entre paquets d'une même session
    pkt.time = current_time
    packets.append(pkt)

def generate_legit_machines(num_machines, ip_start, ip_end, excluded_ips):
    """Génère une liste de machines légitimes avec des IP/MAC aléatoires."""
    machines = []
    available_ips = list(range(ip_start, ip_end + 1))
    # Retire les IPs déjà utilisées
    for ip in excluded_ips:
        ip_suffix = int(ip.split('.')[-1])
        if ip_suffix in available_ips:
            available_ips.remove(ip_suffix)

    if len(available_ips) < num_machines:
        raise ValueError("Pas assez d'adresses IP disponibles dans la plage spécifiée.")

    chosen_ips = random.sample(available_ips, num_machines)

    for i in range(num_machines):
        ip = f"192.168.1.{chosen_ips[i]}"
        mac = str(RandMAC())
        machines.append({"ip": ip, "mac": mac})
        print(f"[*] Machine Légitime Générée: IP={ip}, MAC={mac}")
    return machines

def simulate_arp_exchange(src_ip, src_mac, target_ip):
    """Simule une requête ARP et la réponse du routeur."""
    print(f"[*] Simulation ARP: {src_ip} demande l'adresse MAC de {target_ip}")
    # Requête ARP (Broadcast)
    arp_request = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff")/ARP(
        pdst=target_ip,      # IP recherchée
        psrc=src_ip,         # IP de l'émetteur
        hwsrc=src_mac,       # MAC de l'émetteur
        op="who-has"         # Type de requête ARP
    )
    add_packet(arp_request)

    # Réponse ARP (Unicast) - Ici, on suppose que seul le routeur répond
    if target_ip == ROUTER_IP:
        arp_reply = Ether(src=ROUTER_MAC, dst=src_mac)/ARP(
            pdst=src_ip,         # IP du destinataire initial (celui qui a demandé)
            psrc=target_ip,      # IP de celui qui répond (le routeur)
            hwdst=src_mac,       # MAC du destinataire initial
            hwsrc=ROUTER_MAC,    # MAC de celui qui répond (le routeur)
            op="is-at"           # Type de réponse ARP
        )
        add_packet(arp_reply)
    # Note : Dans une simulation plus complexe, d'autres machines pourraient répondre.

def simulate_http_transaction(src_ip, src_mac, dst_ip, dst_mac):
    """Simule une transaction HTTP simple (3-way handshake, GET, 200 OK)."""
    sport = random.randint(1025, 65535) # Port source aléatoire
    dport = 80                          # Port destination HTTP

    # Établissement de la connexion TCP (3-way handshake)
    print(f"[*] Simulation HTTP: {src_ip} -> {dst_ip} (via {dst_mac})")
    ip_layer = IP(src=src_ip, dst=dst_ip)

    # 1. SYN
    syn_pkt = Ether(src=src_mac, dst=dst_mac)/ip_layer/TCP(sport=sport, dport=dport, flags='S', seq=random.randint(0, 2**32 - 1))
    add_packet(syn_pkt)

    # 2. SYN-ACK (Réponse du "serveur" - le routeur dans ce cas simple)
    # seq_srv est aléatoire, ack répond au seq du client + 1
    seq_srv = random.randint(0, 2**32 - 1)
    ack_srv = syn_pkt[TCP].seq + 1
    synack_pkt = Ether(src=dst_mac, dst=src_mac)/IP(src=dst_ip, dst=src_ip)/TCP(sport=dport, dport=sport, flags='SA', seq=seq_srv, ack=ack_srv)
    add_packet(synack_pkt)

    # 3. ACK (Confirmation du client)
    # seq_cli est le ack précédent, ack répond au seq du serveur + 1
    seq_cli = ack_srv
    ack_cli = synack_pkt[TCP].seq + 1
    ack_pkt = Ether(src=src_mac, dst=dst_mac)/ip_layer/TCP(sport=sport, dport=dport, flags='A', seq=seq_cli, ack=ack_cli)
    add_packet(ack_pkt)

    # Requête HTTP GET
    http_get_payload = "GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n"
    http_get_pkt = Ether(src=src_mac, dst=dst_mac)/ip_layer/TCP(sport=sport, dport=dport, flags='PA', seq=seq_cli, ack=ack_cli)/Raw(load=http_get_payload)
    add_packet(http_get_pkt)
    seq_cli += len(http_get_payload) # Incrémenter le numéro de séquence client

    # Réponse HTTP 200 OK (du "serveur")
    http_ok_payload = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 12\r\nConnection: close\r\n\r\nHello World!"
    # seq_srv est le ack précédent, ack est le seq client après le GET
    http_ok_pkt = Ether(src=dst_mac, dst=src_mac)/IP(src=dst_ip, dst=src_ip)/TCP(sport=dport, dport=sport, flags='PA', seq=ack_cli, ack=seq_cli)/Raw(load=http_ok_payload)
    add_packet(http_ok_pkt)
    seq_srv = ack_cli + len(http_ok_payload) # Incrémenter le numéro de séquence serveur

    # Fermeture de la connexion (simplifiée - FIN/ACK)
    # Client -> Serveur
    fin_cli_pkt = Ether(src=src_mac, dst=dst_mac)/ip_layer/TCP(sport=sport, dport=dport, flags='FA', seq=seq_cli, ack=seq_srv)
    add_packet(fin_cli_pkt)
    # Serveur -> Client
    ack_srv_fin_pkt = Ether(src=dst_mac, dst=src_mac)/IP(src=dst_ip, dst=src_ip)/TCP(sport=dport, dport=sport, flags='A', seq=seq_srv, ack=seq_cli + 1)
    add_packet(ack_srv_fin_pkt)
    fin_srv_pkt = Ether(src=dst_mac, dst=src_mac)/IP(src=dst_ip, dst=src_ip)/TCP(sport=dport, dport=sport, flags='FA', seq=seq_srv, ack=seq_cli + 1)
    add_packet(fin_srv_pkt)
     # Client -> Serveur
    ack_cli_fin_pkt = Ether(src=src_mac, dst=dst_mac)/ip_layer/TCP(sport=sport, dport=dport, flags='A', seq=seq_cli + 1, ack=seq_srv + 1)
    add_packet(ack_cli_fin_pkt)

# --- Génération du scénario ---

print("--- Début de la génération du scénario ARP Spoofing ---")

# 1. Générer les autres machines légitimes
excluded_ips_for_generation = [ROUTER_IP, ATTACKER_IP, VICTIM_IP]
other_legit_machines = generate_legit_machines(
    NUM_OTHER_MACHINES,
    LEGIT_IP_RANGE_START,
    LEGIT_IP_RANGE_END,
    excluded_ips_for_generation
)
all_legit_machines = [{"ip": VICTIM_IP, "mac": VICTIM_MAC}] + other_legit_machines
all_machines_initially = all_legit_machines + [{"ip": ATTACKER_IP, "mac": ATTACKER_MAC}]

# 2. Phase de trafic normal initial
print(f"\n--- Simulation du trafic normal initial ({NUM_INITIAL_NORMAL_ROUNDS} rounds) ---")
for i in range(NUM_INITIAL_NORMAL_ROUNDS):
    print(f"\n[Round Normal {i+1}/{NUM_INITIAL_NORMAL_ROUNDS}]")
    machines_to_shuffle = all_machines_initially[:] # Copie pour mélange
    random.shuffle(machines_to_shuffle) # Ordre aléatoire pour plus de réalisme

    for machine in machines_to_shuffle:
        # Chaque machine (y compris l'attaquant au début) fait une requête ARP au routeur
        simulate_arp_exchange(machine["ip"], machine["mac"], ROUTER_IP)
        time.sleep(get_random_delay() / 5) # Petit délai entre ARP et HTTP

        # Chaque machine (y compris l'attaquant au début) fait une transaction HTTP vers le routeur
        simulate_http_transaction(machine["ip"], machine["mac"], ROUTER_IP, ROUTER_MAC)
        time.sleep(get_random_delay()) # Délai entre les actions des différentes machines

# 3. L'attaque ARP Spoofing
print("\n--- Lancement de l'attaque ARP Spoofing ---")
print(f"[*] Attaquant ({ATTACKER_IP}/{ATTACKER_MAC}) envoie une réponse ARP frauduleuse à la Victime ({VICTIM_IP}/{VICTIM_MAC})")
print(f"    Se fait passer pour le routeur ({ROUTER_IP})")

# L'attaquant envoie une réponse ARP à la victime ("is-at")
# disant que l'IP du routeur (pdst=ROUTER_IP) est à la MAC de l'attaquant (hwsrc=ATTACKER_MAC)
arp_spoof_reply = Ether(src=ATTACKER_MAC, dst=VICTIM_MAC)/ARP(
    op="is-at",          # Opération: réponse ARP
    psrc=ROUTER_IP,      # IP usurpée (celle du routeur)
    hwsrc=ATTACKER_MAC,  # MAC de l'attaquant (la fausse MAC pour l'IP du routeur)
    pdst=VICTIM_IP,      # IP de la cible (victime)
    hwdst=VICTIM_MAC     # MAC de la cible (victime)
)
add_packet(arp_spoof_reply)
# On peut envoyer plusieurs fois pour s'assurer que le cache de la victime est empoisonné
time.sleep(get_random_delay())

# 4. Phase Man-in-the-Middle (MitM)
print(f"\n--- Simulation de la phase Man-in-the-Middle ({NUM_MITM_ROUNDS} rounds) ---")
for i in range(NUM_MITM_ROUNDS):
    print(f"\n[Round MitM {i+1}/{NUM_MITM_ROUNDS}]")

    # Le trafic de la victime est maintenant redirigé vers l'attaquant
    print(f"[*] Victime ({VICTIM_IP}) envoie du trafic HTTP vers {ROUTER_IP}, mais via la MAC de l'attaquant ({ATTACKER_MAC})")
    # simulate_http_transaction(VICTIM_IP, VICTIM_MAC, ROUTER_IP, ATTACKER_MAC) # Incorrect, il faut relayer

    # Simuler une transaction HTTP complète mais en passant par l'attaquant
    sport_victim = random.randint(1025, 65535)
    dport_victim = 80
    seq_victim = random.randint(0, 2**32 - 1)
    ack_victim = 0
    seq_router_reply = random.randint(0, 2**32 - 1) # Séquence de réponse simulée du routeur

    # 4.1 Victim -> Attacker (SYN) - Couche 2 vers Attacker, Couche 3 vers Router
    syn_victim_to_attacker = Ether(src=VICTIM_MAC, dst=ATTACKER_MAC)/IP(src=VICTIM_IP, dst=ROUTER_IP)/TCP(sport=sport_victim, dport=dport_victim, flags='S', seq=seq_victim)
    add_packet(syn_victim_to_attacker)
    print(f"    1. Victime -> Attaquant (SYN): {VICTIM_IP}:{sport_victim} -> {ROUTER_IP}:{dport_victim} (MAC dst: {ATTACKER_MAC})")

    # 4.2 Attacker -> Router (Relais SYN) - Modifie MAC src/dst
    syn_attacker_to_router = Ether(src=ATTACKER_MAC, dst=ROUTER_MAC)/IP(src=VICTIM_IP, dst=ROUTER_IP)/TCP(sport=sport_victim, dport=dport_victim, flags='S', seq=seq_victim)
    add_packet(syn_attacker_to_router)
    print(f"    2. Attaquant -> Routeur (Relais SYN): {VICTIM_IP}:{sport_victim} -> {ROUTER_IP}:{dport_victim} (MAC src: {ATTACKER_MAC}, MAC dst: {ROUTER_MAC})")

    # 4.3 Router -> Attacker (SYN-ACK) - Réponse normale, mais l'attaquant la reçoit
    ack_victim = seq_victim + 1
    synack_router_to_attacker = Ether(src=ROUTER_MAC, dst=ATTACKER_MAC)/IP(src=ROUTER_IP, dst=VICTIM_IP)/TCP(sport=dport_victim, dport=sport_victim, flags='SA', seq=seq_router_reply, ack=ack_victim)
    add_packet(synack_router_to_attacker)
    print(f"    3. Routeur -> Attaquant (SYN-ACK): {ROUTER_IP}:{dport_victim} -> {VICTIM_IP}:{sport_victim} (MAC dst: {ATTACKER_MAC})")

    # 4.4 Attacker -> Victim (Relais SYN-ACK) - Modifie MAC src/dst
    synack_attacker_to_victim = Ether(src=ATTACKER_MAC, dst=VICTIM_MAC)/IP(src=ROUTER_IP, dst=VICTIM_IP)/TCP(sport=dport_victim, dport=sport_victim, flags='SA', seq=seq_router_reply, ack=ack_victim)
    add_packet(synack_attacker_to_victim)
    print(f"    4. Attaquant -> Victime (Relais SYN-ACK): {ROUTER_IP}:{dport_victim} -> {VICTIM_IP}:{sport_victim} (MAC src: {ATTACKER_MAC}, MAC dst: {VICTIM_MAC})")

    # 4.5 Victim -> Attacker (ACK)
    seq_victim = ack_victim
    ack_victim = seq_router_reply + 1
    ack_victim_to_attacker = Ether(src=VICTIM_MAC, dst=ATTACKER_MAC)/IP(src=VICTIM_IP, dst=ROUTER_IP)/TCP(sport=sport_victim, dport=dport_victim, flags='A', seq=seq_victim, ack=ack_victim)
    add_packet(ack_victim_to_attacker)
    print(f"    5. Victime -> Attaquant (ACK): (MAC dst: {ATTACKER_MAC})")

    # 4.6 Attacker -> Router (Relais ACK)
    ack_attacker_to_router = Ether(src=ATTACKER_MAC, dst=ROUTER_MAC)/IP(src=VICTIM_IP, dst=ROUTER_IP)/TCP(sport=sport_victim, dport=dport_victim, flags='A', seq=seq_victim, ack=ack_victim)
    add_packet(ack_attacker_to_router)
    print(f"    6. Attaquant -> Routeur (Relais ACK): (MAC src: {ATTACKER_MAC}, MAC dst: {ROUTER_MAC})")

    # --- Simulation Requête/Réponse HTTP via MitM ---
    http_get_payload = f"GET /page_{i} HTTP/1.1\r\nHost: relayed.com\r\nConnection: close\r\n\r\n"

    # 4.7 Victim -> Attacker (HTTP GET)
    get_victim_to_attacker = Ether(src=VICTIM_MAC, dst=ATTACKER_MAC)/IP(src=VICTIM_IP, dst=ROUTER_IP)/TCP(sport=sport_victim, dport=dport_victim, flags='PA', seq=seq_victim, ack=ack_victim)/Raw(load=http_get_payload)
    add_packet(get_victim_to_attacker)
    print(f"    7. Victime -> Attaquant (HTTP GET): (MAC dst: {ATTACKER_MAC})")
    seq_victim_after_get = seq_victim + len(http_get_payload)

    # 4.8 Attacker -> Router (Relais HTTP GET)
    get_attacker_to_router = Ether(src=ATTACKER_MAC, dst=ROUTER_MAC)/IP(src=VICTIM_IP, dst=ROUTER_IP)/TCP(sport=sport_victim, dport=dport_victim, flags='PA', seq=seq_victim, ack=ack_victim)/Raw(load=http_get_payload)
    add_packet(get_attacker_to_router)
    print(f"    8. Attaquant -> Routeur (Relais HTTP GET): (MAC src: {ATTACKER_MAC}, MAC dst: {ROUTER_MAC})")

    # 4.9 Router -> Attacker (HTTP Response 200 OK) - Réponse avec contenu simulé
    http_ok_payload = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 15\r\nConnection: close\r\n\r\nRelayed page {i}"
    seq_router_reply = ack_victim # Le seq de la réponse commence au ack reçu
    ack_router_reply = seq_victim_after_get # Le ack de la réponse confirme les données reçues
    resp_router_to_attacker = Ether(src=ROUTER_MAC, dst=ATTACKER_MAC)/IP(src=ROUTER_IP, dst=VICTIM_IP)/TCP(sport=dport_victim, dport=sport_victim, flags='PA', seq=seq_router_reply, ack=ack_router_reply)/Raw(load=http_ok_payload)
    add_packet(resp_router_to_attacker)
    print(f"    9. Routeur -> Attaquant (HTTP 200 OK): (MAC dst: {ATTACKER_MAC})")
    seq_router_after_resp = seq_router_reply + len(http_ok_payload)

    # 4.10 Attacker -> Victim (Relais HTTP Response)
    resp_attacker_to_victim = Ether(src=ATTACKER_MAC, dst=VICTIM_MAC)/IP(src=ROUTER_IP, dst=VICTIM_IP)/TCP(sport=dport_victim, dport=sport_victim, flags='PA', seq=seq_router_reply, ack=ack_router_reply)/Raw(load=http_ok_payload)
    add_packet(resp_attacker_to_victim)
    print(f"   10. Attaquant -> Victime (Relais HTTP 200 OK): (MAC src: {ATTACKER_MAC}, MAC dst: {VICTIM_MAC})")

    # (Optionnel: ajouter la fermeture de connexion relayée également)

    time.sleep(get_random_delay()) # Délai avant le trafic des autres machines

    # 5. Les autres machines continuent leur trafic normal
    print(f"[*] Trafic normal des autres machines légitimes pendant le MitM")
    machines_to_shuffle = other_legit_machines[:] # Ne pas inclure la victime ici
    random.shuffle(machines_to_shuffle)
    for machine in machines_to_shuffle:
         # Pas besoin de refaire l'ARP à chaque fois, mais on peut en ajouter quelques uns
        if random.random() < 0.1: # 10% de chance de refaire un ARP
             simulate_arp_exchange(machine["ip"], machine["mac"], ROUTER_IP)
             time.sleep(get_random_delay() / 5)

        # Trafic HTTP normal vers le routeur
        simulate_http_transaction(machine["ip"], machine["mac"], ROUTER_IP, ROUTER_MAC)
        time.sleep(get_random_delay()) # Délai entre les machines légitimes


# 6. Écriture du fichier PCAP
print(f"\n--- Écriture des {len(packets)} paquets dans le fichier {PCAP_FILENAME} ---")
try:
    wrpcap(PCAP_FILENAME, packets)
    print(f"[+] Fichier PCAP '{PCAP_FILENAME}' généré avec succès.")
except Exception as e:
    print(f"[!] Erreur lors de l'écriture du fichier PCAP: {e}")

print("\n--- Fin de la simulation ---")