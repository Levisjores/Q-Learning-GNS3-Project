from pysnmp.hlapi import *
import csv
from datetime import datetime

routeurs = [
    {"ip": "192.168.1.1", "community": "public", "nom": "R1"},
    {"ip": "192.168.2.1", "community": "public", "nom": "R2"},
    # Ajoute R3 à R6
]

oids = {
    "ifInOctets": '1.3.6.1.2.1.2.2.1.10.1',
    "ifOutOctets": '1.3.6.1.2.1.2.2.1.16.1'
}

def snmp_get(ip, community, oid):
    iterator = getCmd(SnmpEngine(),
                      CommunityData(community),
                      UdpTransportTarget((ip, 161)),
                      ContextData(),
                      ObjectType(ObjectIdentity(oid)))
    errorIndication, errorStatus, _, varBinds = next(iterator)
    if errorIndication or errorStatus:
        return None
    return int(varBinds[0][1])

def collecter_snmp():
    with open("metriques_fusionnees.csv", "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for r in routeurs:
            try:
                in_octets = snmp_get(r["ip"], r["community"], oids["ifInOctets"])
                out_octets = snmp_get(r["ip"], r["community"], oids["ifOutOctets"])
                writer.writerow([
                    datetime.now(), r["nom"], "SNMP",
                    f"{in_octets} octets IN", f"{out_octets} octets OUT", "-", "-"
                ])
            except Exception as e:
                print(f"[Erreur SNMP] {r['nom']} : {e}")

if __name__ == "__main__":
    collecter_snmp()
