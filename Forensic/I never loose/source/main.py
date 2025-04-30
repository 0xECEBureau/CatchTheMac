#!/usr/bin/env python3
from scapy.all import (
    Ether, IP, UDP, TCP, ARP, ICMP, DNS, DNSQR, Raw,
    wrpcap
)
import random, time

# ─── Configuration ──────────────────────────────────────────────────────────────
NUM_PLAYERS           = 5
HEALTH_PACKETS_PER    = 20
EVENT_PACKETS_PER     = 15
NUM_ROUNDS            = 3
KILL_PACKETS_PER_ROUND = 5
SERVER_IP             = "192.168.1.100"
CLIENT_NET            = "192.168.1."
CS_UDP_PORT           = 27015
OUTPUT_PCAP           = "cs_lan_with_junk_and_events.pcap"

NUM_JUNK_PACKETS      = 200
JUNK_TYPES_WEIGHTS    = {"arp": 10, "icmp": 30, "tcp": 40, "dns": 10, "http": 10}

bad_player = random.randint(1, NUM_PLAYERS)

# ─── Helpers ───────────────────────────────────────────────────────────────────
def rand_client_ip():
    return CLIENT_NET + str(random.randint(2, 254))

# ─── Generate Counter-Strike health packets ────────────────────────────────────
def gen_cs_health_packets():
    cs_pkts = []
    for player_id in range(1, NUM_PLAYERS+1):
        src_ip = rand_client_ip()
        for seq in range(HEALTH_PACKETS_PER):
            hp = random.randint(0, 100)
            payload = f"PLAYER:{player_id};HP:{hp};SEQ:{seq}"
            pkt = (
                Ether() /
                IP(src=src_ip, dst=SERVER_IP) /
                UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
                Raw(load=payload.encode())
            )
            cs_pkts.append(pkt)
    # inject one HP anomaly
    bad_src_ip = rand_client_ip()
    bad_payload = f"PLAYER:{bad_player};HP:9999;SEQ:999"
    bad_pkt = (
        Ether() /
        IP(src=bad_src_ip, dst=SERVER_IP) /
        UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
        Raw(load=bad_payload.encode())
    )
    cs_pkts.insert(random.randint(0, len(cs_pkts)), bad_pkt)
    return cs_pkts

# ─── Generate game event packets (shoot events) ────────────────────────────────
def gen_game_event_packets():
    ev_pkts = []
    for player_id in range(1, NUM_PLAYERS+1):
        src_ip = rand_client_ip()
        for seq in range(EVENT_PACKETS_PER):
            victim = random.choice([i for i in range(1, NUM_PLAYERS+1) if i != player_id])
            payload = f"PLAYER:{player_id};EVENT:SHOOT;TARGET:{victim};SEQ:{seq};AMMO:1"
            pkt = (
                Ether() /
                IP(src=src_ip, dst=SERVER_IP) /
                UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
                Raw(load=payload.encode())
            )
            ev_pkts.append(pkt)
    # cheater anomaly: shoots all players at once
    cheat_src = rand_client_ip()
    targets = ",".join(str(i) for i in range(1, NUM_PLAYERS+1))
    cheat_payload = (
        f"PLAYER:{bad_player};CMD:KILL_ALL;TARGETS:{targets};AMMO:999;SEQ:999"
    )
    cheat_pkt = (
        Ether() /
        IP(src=cheat_src, dst=SERVER_IP) /
        UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
        Raw(load=cheat_payload.encode())
    )
    ev_pkts.insert(random.randint(0, len(ev_pkts)), cheat_pkt)
    return ev_pkts

# ─── Generate round control & kill packets ─────────────────────────────────────
def gen_round_control_packets():
    rounds = []
    for rnd in range(1, NUM_ROUNDS+1):
        # Round start
        start_payload = f"EVENT:ROUND_START;ROUND:{rnd}"
        rounds.append(
            Ether() /
            IP(src=rand_client_ip(), dst=SERVER_IP) /
            UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
            Raw(load=start_payload.encode())
        )
        # Kill events
        for k in range(KILL_PACKETS_PER_ROUND):
            killer = random.randint(1, NUM_PLAYERS)
            victim = random.choice([i for i in range(1, NUM_PLAYERS+1) if i != killer])
            kill_payload = (
                f"PLAYER:{killer};EVENT:KILL;TARGET:{victim};ROUND:{rnd};SEQ:{k}"
            )
            rounds.append(
                Ether() /
                IP(src=rand_client_ip(), dst=SERVER_IP) /
                UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
                Raw(load=kill_payload.encode())
            )
        # Round end
        winner = random.choice(list(range(1, NUM_PLAYERS+1)))
        end_payload = f"EVENT:ROUND_END;ROUND:{rnd};WINNER:PLAYER:{winner}"
        rounds.append(
            Ether() /
            IP(src=rand_client_ip(), dst=SERVER_IP) /
            UDP(sport=random.randint(1024,65535), dport=CS_UDP_PORT) /
            Raw(load=end_payload.encode())
        )
    return rounds

# ─── Generate junk packets ──────────────────────────────────────────────────────
def gen_arp():
    return Ether() / ARP(
        op=1,
        hwsrc="02:00:00:%02x:%02x:%02x" % tuple(random.randint(0,255) for _ in range(3)),
        psrc=rand_client_ip(),
        pdst=CLIENT_NET + str(random.randint(1,254))
    )

def gen_icmp():
    return Ether() / IP(
        src=rand_client_ip(),
        dst=SERVER_IP
    ) / ICMP() / Raw(load=b"PING" * random.randint(1,5))

def gen_tcp_handshake():
    src = rand_client_ip()
    sport = random.randint(1024, 65535)
    syn = Ether() / IP(src=src, dst=SERVER_IP) / TCP(sport=sport, dport=80, flags="S", seq=1000)
    synack = Ether() / IP(src=SERVER_IP, dst=src) / TCP(sport=80, dport=sport, flags="SA", seq=2000, ack=1001)
    ack = Ether() / IP(src=src, dst=SERVER_IP) / TCP(sport=sport, dport=80, flags="A", seq=1001, ack=2001)
    return [syn, synack, ack]

def gen_dns_query():
    return Ether() / IP(
        src=rand_client_ip(),
        dst="8.8.8.8"
    ) / UDP(sport=random.randint(1024,65535), dport=53) / DNS(
        rd=1,
        qd=DNSQR(qname=f"www.{random.choice(['example','test','foo','bar'])}.com")
    )

def gen_http_get():
    src = rand_client_ip()
    sport = random.randint(1024, 65535)
    payload = (
        f"GET /{random.choice(['index.html','favicon.ico','status','data'])} HTTP/1.1\r\n"
        f"Host: {random.choice(['example.com','test.local','foo.bar'])}\r\n\r\n"
    ).encode()
    return Ether() / IP(src=src, dst=SERVER_IP) / TCP(sport=sport, dport=80, flags="PA", seq=1, ack=1) / Raw(load=payload)

# prepare weighted pool
JUNK_GENS = {"arp": gen_arp, "icmp": gen_icmp, "tcp": gen_tcp_handshake,
             "dns": gen_dns_query, "http": gen_http_get}
JUNK_POOL = []
for t, w in JUNK_TYPES_WEIGHTS.items(): JUNK_POOL += [t]*w

def gen_junk_packets(n):
    junk_list = []
    for _ in range(n):
        typ = random.choice(JUNK_POOL)
        pkt = JUNK_GENS[typ]()
        if isinstance(pkt, list): junk_list.extend(pkt)
        else: junk_list.append(pkt)
    return junk_list

# ─── Build and write pcap ───────────────────────────────────────────────────────
cs_pkts    = gen_cs_health_packets()
ev_pkts    = gen_game_event_packets()
round_pkts = gen_round_control_packets()
junk_pkts  = gen_junk_packets(NUM_JUNK_PACKETS)

all_pkts = cs_pkts + ev_pkts + round_pkts + junk_pkts
random.shuffle(all_pkts)

base = time.time()
for i, p in enumerate(all_pkts): p.time = base + i * 0.001

wrpcap(OUTPUT_PCAP, all_pkts)
print(f"Wrote {len(all_pkts)} packets: {len(cs_pkts)} health + {len(ev_pkts)} shoot + {len(round_pkts)} rounds + {len(junk_pkts)} junk → {OUTPUT_PCAP}")
