# port_scanner.py

import socket
import threading
import csv

open_ports = []

# Function to scan individual port and grab banner
def scan_port(target_ip, port):
    global open_ports
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            try:
                sock.sendall(b'Hello\r\n')
                banner = sock.recv(1024).decode().strip()
            except:
                banner = 'Not Available'
            print(f"[OPEN] Port {port} | Banner: {banner}")
            open_ports.append((port, banner))
        sock.close()
    except:
        pass

# Function to perform threaded scanning
def threaded_port_scanner(target_ip, start_port, end_port):
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

# Function to export results to CSV
def export_to_csv(filename='scan_report.csv'):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Port', 'Banner'])
        writer.writerows(open_ports)
    print(f"\n[+] Scan report saved to {filename}")

# Main function
if __name__ == "__main__":
    print("TCP Port Scanner with Banner Grabbing\n")
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))

    threaded_port_scanner(target_ip, start_port, end_port)
    export_to_csv()
