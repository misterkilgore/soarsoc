#!/bin/bash

# ------------ SETUP DELLA RETE -------------- #

# Reset delle regole esistenti
iptables -F
iptables -t nat -F
iptables -X

# Abilita il forwarding dei pacchetti
echo 1 > /proc/sys/net/ipv4/ip_forward

# Politiche di default: DROP tutto
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Accetta tutto il traffico sulla loopback
iptables -A INPUT -i lo -j ACCEPT

# Accetta connessioni già stabilite e correlate
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# ------------ SERVIZIO CONSENTITI IN INGRESSO -------------- #

# Permetti ping (ICMP echo request) in ingresso da eth1 (rete interna)
iptables -A INPUT -i eth1 -p icmp --icmp-type echo-request -j ACCEPT

# Permetti SSH (porta 22 TCP) da eth1
iptables -A INPUT -i eth1 -p tcp --dport 22 -j ACCEPT

# ------------ SERVIZIO NAT -------------- #

# NAT: mascheramento sull'interfaccia eth0 (internet)
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Permetti forwarding dei pacchetti dalla rete interna verso internet
iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT

# Permetti forwarding dei pacchetti di ritorno da internet verso la rete interna
iptables -A FORWARD -i eth0 -o eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT
