from scapy.all import sniff
from models import LogEntry, db_session

def packet_callback(packet):
    log_entry = LogEntry(log_type='packet', message=str(packet))
    db_session.add(log_entry)
    db_session.commit()

def start_sniffing():
    sniff(prn=packet_callback, store=0)
