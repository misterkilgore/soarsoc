#!/bin/bash

### start_fw.sh - Configurazione firewall minima con iptables per rete MILKERS Inc.

# Pulizia regole esistenti per partire da zero
iptables -F
iptables -t nat -F
iptables -X

# Politiche di default: bloccare tutto il traffico in ingresso e inoltro, permettere tutto in uscita
iptables -P INPUT DROP    # Default: blocca tutto il traffico in ingresso
iptables -P FORWARD DROP  # Default: blocca inoltro pacchetti tra interfacce
iptables -P OUTPUT ACCEPT # Default: permetti tutto il traffico in uscita

# Permetti traffico in ingresso sulla loopback (interfaccia locale)
iptables -A INPUT -i lo -j ACCEPT
# Permetti traffico di ritorno per connessioni già stabilite
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Regola per permettere accesso SSH dalla rete IT-Office-Network (192.168.20.0/24)
# Serve per amministrare i server in Server-Farm-OnPrem in modo sicuro
iptables -A INPUT -p tcp -s 192.168.20.0/24 --dport 22 -j ACCEPT

# Regola per permettere accesso VPN dalla rete 172.16.0.0/24 (manutentori esterni)
iptables -A INPUT -p udp -s 172.16.0.0/24 --dport 1194 -j ACCEPT
# (Supponendo che la VPN usi UDP 1194, tipico per OpenVPN)

# Regola DNAT per port forwarding: es. accesso al server Logistics-DB (10.0.0.10) dalla rete IT-Office-Network
# Qui si mappa la porta 3306 (MySQL) del firewall verso il server interno
iptables -t nat -A PREROUTING -p tcp -s 192.168.20.0/24 --dport 3306 -j DNAT --to-destination 10.0.0.10:3306
iptables -A FORWARD -p tcp -d 10.0.0.10 --dport 3306 -m conntrack --ctstate NEW,ESTABLISHED,RELATED -j ACCEPT

# Regola per permettere traffico ICMP (ping) dalla rete IT-Office-Network per diagnostica
iptables -A INPUT -p icmp -s 192.168.20.0/24 -j ACCEPT

# Regola per permettere al firewall stesso (10.0.0.254) di inoltrare traffico NAT verso Internet (esempio)
# Abilitiamo il forwarding IP
echo 1 > /proc/sys/net/ipv4/ip_forward

# Mascheramento (SNAT) per traffico in uscita dalla Server-Farm-OnPrem verso Internet
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o eth0 -j MASQUERADE
# Nota: eth0 è l'interfaccia esterna verso Internet, adattare se diversa

# Fine script
echo "Firewall configurato con regole base per MILKERS Inc."