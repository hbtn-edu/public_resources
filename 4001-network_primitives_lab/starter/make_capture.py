#!/usr/bin/env python3
"""Generate `reference_capture.pcap` for project 101, Task 4.

The Task 4 quiz (`evaluation/101/101-task4-tcp-capture.fill_in_the_blank.md`)
asks for values read straight out of this file, so the capture cannot be a
"whatever came off the wire" recording: every port, flag, window, sequence
number, payload length and packet count is fixed by the quiz. This script is
the single source of truth for them, which is why it ships next to the pcap.

Nothing is captured. The twelve packets are synthesised byte by byte, with
RFC 5737 documentation addresses (192.0.2.0/24) and no real hosts, so the file
is safe to hand out and identical for every student.

    python3 make_capture.py                 # writes ./reference_capture.pcap
    python3 make_capture.py -o other.pcap

Dependencies: none. The Python standard library only, on purpose: the capture
must be reproducible on any machine, in a container, or in CI, without a
`pip install`.

Verify the result with the exact command the task gives the student:

    tcpdump -r reference_capture.pcap -nn
"""

from __future__ import annotations

import argparse
import struct
import sys

# --------------------------------------------------------------------------
# The canonical values. These are quoted in projects/101-network_primitives_lab.md
# ("Starter Assets" -> reference_capture.pcap) and asserted by the Task 4 quiz.
# Changing anything here means changing the quiz.
# --------------------------------------------------------------------------
CLIENT_IP = "192.0.2.10"
SERVER_IP = "192.0.2.20"
DNS_IP = "192.0.2.53"
RESOLVED_IP = "192.0.2.80"

CLIENT_PORT = 49722          # quiz Q1  - ephemeral source port
SERVER_PORT = 80             # quiz Q2  - destination port
DNS_SRC_PORT = 51344         # quiz alt Q1
DNS_DST_PORT = 53            # quiz Q8

CLIENT_WINDOW = 64240        # quiz Q5
SERVER_WINDOW = 65160        # quiz alt Q5

DNS_TXID = 26814
DNS_QNAME = "example.com"
DNS_TTL = 300

# Initial sequence numbers.
#
# These are 0 on purpose, and it is the one place where this capture is less
# realistic than a recorded one (a real TCP stack picks a random ISN).
# tcpdump renders sequence numbers relative to the ISN it learns from the SYN,
# but it prints the SYN and SYN-ACK themselves *absolutely* - so a random ISN
# would make packets 1 and 2 read
#     Flags [S], seq 1000000000, win 64240
#     Flags [S.], seq 2000000000, ack 1000000001, win 65160
# while the project's canonical listing and Task 4 quiz questions 3 and 4 both
# show `seq 0` / `seq 0, ack 1`. Every quiz answer has to be readable straight
# out of this file, so the file matches the quiz.
CLIENT_ISN = 0
SERVER_ISN = 0

# Locally-administered MAC addresses; nothing real.
CLIENT_MAC = "02:00:00:00:00:0a"
SERVER_MAC = "02:00:00:00:00:14"
DNS_MAC = "02:00:00:00:00:35"

# 2025-01-06 10:15:42 UTC, fixed so two runs produce identical bytes.
BASE_EPOCH = 1_736_158_542

# TCP flag bits
FIN, SYN, RST, PSH, ACK = 0x01, 0x02, 0x04, 0x08, 0x10

LINKTYPE_ETHERNET = 1
PCAP_MAGIC = 0xA1B2C3D4
SNAPLEN = 262144


# --------------------------------------------------------------------------
# Application payloads
# --------------------------------------------------------------------------
# Exactly 77 bytes: quiz Q9 reads the method out of this packet, and the
# project's canonical listing shows "seq 1:78 ... length 77".
HTTP_REQUEST = (
    "GET /index.html HTTP/1.1\r\n"
    "Host: 192.0.2.20\r\n"
    "User-Agent: curl\r\n"
    "Accept: */*\r\n"
    "\r\n"
).encode()

# Exactly 242 bytes: quiz Q10 reads the status code, quiz alt Q10 reads the
# payload length ("length 242").
_HTTP_BODY = (
    "<html>\r\n"
    "<head><title>netlab reference page</title></head>\r\n"
    "<body><h1>It works!</h1></body>\r\n"
    "</html>\r\n"
).encode()
HTTP_RESPONSE = (
    "HTTP/1.1 200 OK\r\n"
    "Date: Mon, 06 Jan 2025 10:15:42 GMT\r\n"
    "Server: nginx/1.25\r\n"
    "Content-Type: text/html\r\n"
    f"Content-Length: {len(_HTTP_BODY)}\r\n"
    "Connection: close\r\n"
    "\r\n"
).encode() + _HTTP_BODY


# --------------------------------------------------------------------------
# Byte-level helpers
# --------------------------------------------------------------------------
def mac(text: str) -> bytes:
    return bytes(int(part, 16) for part in text.split(":"))


def ipv4(text: str) -> bytes:
    return bytes(int(part) for part in text.split("."))


def checksum16(data: bytes) -> int:
    """The one's-complement checksum used by IPv4, TCP and UDP."""
    if len(data) % 2:
        data += b"\x00"
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) | data[i + 1]
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def ip_header(src: str, dst: str, proto: int, payload_len: int, ident: int) -> bytes:
    total_length = 20 + payload_len
    header = struct.pack(
        "!BBHHHBBH4s4s",
        0x45,            # version 4, IHL 5 (no options)
        0x00,            # DSCP / ECN
        total_length,
        ident,
        0x4000,          # Don't Fragment
        64,              # TTL
        proto,
        0,               # checksum placeholder
        ipv4(src),
        ipv4(dst),
    )
    csum = checksum16(header)
    return header[:10] + struct.pack("!H", csum) + header[12:]


def l4_checksum(src: str, dst: str, proto: int, segment: bytes) -> int:
    pseudo = ipv4(src) + ipv4(dst) + struct.pack("!BBH", 0, proto, len(segment))
    return checksum16(pseudo + segment)


def tcp_segment(sport: int, dport: int, seq: int, ack: int, flags: int,
                window: int, payload: bytes, src: str, dst: str) -> bytes:
    # Data offset 5 (20 bytes, no options). Options are deliberately omitted:
    # without a window-scale option tcpdump prints the raw window value on
    # every packet, so `win 64240` / `win 65160` read the same everywhere,
    # exactly as the project's canonical listing shows them.
    header = struct.pack(
        "!HHIIBBHHH",
        sport, dport, seq, ack,
        0x50,            # data offset 5 << 4
        flags,
        window,
        0,               # checksum placeholder
        0,               # urgent pointer
    )
    csum = l4_checksum(src, dst, 6, header + payload)
    return header[:16] + struct.pack("!H", csum) + header[18:] + payload


def udp_datagram(sport: int, dport: int, payload: bytes, src: str, dst: str) -> bytes:
    header = struct.pack("!HHHH", sport, dport, 8 + len(payload), 0)
    csum = l4_checksum(src, dst, 17, header + payload)
    csum = csum or 0xFFFF          # 0 means "no checksum" in UDP
    return header[:6] + struct.pack("!H", csum) + payload


def ethernet(src_mac: str, dst_mac: str, payload: bytes) -> bytes:
    return mac(dst_mac) + mac(src_mac) + struct.pack("!H", 0x0800) + payload


# --------------------------------------------------------------------------
# DNS message building
# --------------------------------------------------------------------------
def dns_name(name: str) -> bytes:
    out = b""
    for label in name.split("."):
        out += bytes([len(label)]) + label.encode()
    return out + b"\x00"


def dns_query(txid: int, name: str) -> bytes:
    header = struct.pack("!HHHHHH", txid, 0x0100, 1, 0, 0, 0)  # RD set
    question = dns_name(name) + struct.pack("!HH", 1, 1)       # A, IN
    return header + question


def dns_response(txid: int, name: str, address: str, ttl: int) -> bytes:
    header = struct.pack("!HHHHHH", txid, 0x8180, 1, 1, 0, 0)  # QR + RD + RA
    question = dns_name(name) + struct.pack("!HH", 1, 1)
    # 0xC00C: compression pointer back to the question name at offset 12.
    answer = struct.pack("!HHHIH", 0xC00C, 1, 1, ttl, 4) + ipv4(address)
    return header + question + answer


# --------------------------------------------------------------------------
# The twelve packets
# --------------------------------------------------------------------------
def build_packets() -> list[tuple[float, bytes, str]]:
    """Return [(timestamp_offset, ethernet_frame, description)] in capture order."""
    c2s_ident = iter(range(0x1B00, 0x1B00 + 32))
    s2c_ident = iter(range(0x7A00, 0x7A00 + 32))

    def c2s(seq_off: int, ack_off: int | None, flags: int, payload: bytes = b"") -> bytes:
        seq = CLIENT_ISN + seq_off
        ack = 0 if ack_off is None else SERVER_ISN + ack_off
        seg = tcp_segment(CLIENT_PORT, SERVER_PORT, seq, ack, flags,
                          CLIENT_WINDOW, payload, CLIENT_IP, SERVER_IP)
        return ethernet(CLIENT_MAC, SERVER_MAC,
                        ip_header(CLIENT_IP, SERVER_IP, 6, len(seg), next(c2s_ident)) + seg)

    def s2c(seq_off: int, ack_off: int, flags: int, payload: bytes = b"") -> bytes:
        seg = tcp_segment(SERVER_PORT, CLIENT_PORT, SERVER_ISN + seq_off,
                          CLIENT_ISN + ack_off, flags, SERVER_WINDOW, payload,
                          SERVER_IP, CLIENT_IP)
        return ethernet(SERVER_MAC, CLIENT_MAC,
                        ip_header(SERVER_IP, CLIENT_IP, 6, len(seg), next(s2c_ident)) + seg)

    req_len = len(HTTP_REQUEST)      # 77
    rsp_len = len(HTTP_RESPONSE)     # 242

    packets: list[tuple[float, bytes, str]] = [
        # --- three-way handshake (quiz Q1-Q5) ---
        (0.000000, c2s(0, None, SYN), "SYN"),
        (0.000112, s2c(0, 1, SYN | ACK), "SYN-ACK"),
        (0.000138, c2s(1, 1, ACK), "ACK (handshake complete)"),
        # --- request / response (quiz Q7, Q9, Q10, alt Q10) ---
        (0.000175, c2s(1, 1, PSH | ACK, HTTP_REQUEST), "HTTP GET /index.html"),
        (0.000283, s2c(1, 1 + req_len, ACK), "ACK of the request"),
        (0.000501, s2c(1, 1 + req_len, PSH | ACK, HTTP_RESPONSE), "HTTP/1.1 200 OK"),
        (0.000544, c2s(1 + req_len, 1 + rsp_len, ACK), "ACK of the response"),
        # --- teardown, 3 packets (quiz alt Q6) ---
        (0.001220, c2s(1 + req_len, 1 + rsp_len, FIN | ACK), "FIN-ACK from the client"),
        (0.001338, s2c(1 + rsp_len, 2 + req_len, FIN | ACK), "FIN-ACK from the server"),
        (0.001371, c2s(2 + req_len, 2 + rsp_len, ACK), "final ACK"),
    ]

    # --- the UDP half: one DNS query and its answer (quiz Q8, alt Q1) ---
    query = dns_query(DNS_TXID, DNS_QNAME)
    answer = dns_response(DNS_TXID, DNS_QNAME, RESOLVED_IP, DNS_TTL)

    dgram = udp_datagram(DNS_SRC_PORT, DNS_DST_PORT, query, CLIENT_IP, DNS_IP)
    packets.append((0.010402, ethernet(
        CLIENT_MAC, DNS_MAC,
        ip_header(CLIENT_IP, DNS_IP, 17, len(dgram), 0x2C01) + dgram), "DNS query A? example.com"))

    dgram = udp_datagram(DNS_DST_PORT, DNS_SRC_PORT, answer, DNS_IP, CLIENT_IP)
    packets.append((0.011876, ethernet(
        DNS_MAC, CLIENT_MAC,
        ip_header(DNS_IP, CLIENT_IP, 17, len(dgram), 0x9F31) + dgram), "DNS response"))

    return packets


# --------------------------------------------------------------------------
# pcap container
# --------------------------------------------------------------------------
def write_pcap(path: str, packets: list[tuple[float, bytes, str]]) -> None:
    with open(path, "wb") as handle:
        handle.write(struct.pack(
            "<IHHiIII",
            PCAP_MAGIC, 2, 4, 0, 0, SNAPLEN, LINKTYPE_ETHERNET))
        for offset, frame, _ in packets:
            seconds = BASE_EPOCH + int(offset)
            micros = int(round((offset - int(offset)) * 1_000_000))
            handle.write(struct.pack("<IIII", seconds, micros, len(frame), len(frame)))
            handle.write(frame)


def self_check(packets: list[tuple[float, bytes, str]]) -> None:
    """Fail loudly if the capture ever stops matching the Task 4 quiz."""
    assert len(HTTP_REQUEST) == 77, f"HTTP request must be 77 bytes, got {len(HTTP_REQUEST)}"
    assert len(HTTP_RESPONSE) == 242, f"HTTP response must be 242 bytes, got {len(HTTP_RESPONSE)}"
    assert len(_HTTP_BODY) == 101, f"body must be 101 bytes, got {len(_HTTP_BODY)}"
    assert len(dns_query(DNS_TXID, DNS_QNAME)) == 29, "DNS query must be 29 bytes"
    assert len(dns_response(DNS_TXID, DNS_QNAME, RESOLVED_IP, DNS_TTL)) == 45, \
        "DNS response must be 45 bytes"
    assert len(packets) == 12, f"capture must hold 12 packets, got {len(packets)}"
    tcp = [p for p in packets if p[1][23] == 6]
    udp = [p for p in packets if p[1][23] == 17]
    assert len(tcp) == 10, f"10 TCP packets expected, got {len(tcp)}"
    assert len(udp) == 2, f"2 UDP packets expected, got {len(udp)}"
    with_payload = [p for p in tcp if len(p[1]) > 54]
    assert len(with_payload) == 2, \
        f"exactly 2 TCP packets carry a payload, got {len(with_payload)}"
    # Timestamps must be strictly increasing, or tcpdump's ordering is undefined.
    offsets = [p[0] for p in packets]
    assert offsets == sorted(offsets), "packet timestamps must increase"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-o", "--output", default="reference_capture.pcap",
                        help="output path (default: reference_capture.pcap)")
    args = parser.parse_args()

    packets = build_packets()
    self_check(packets)
    write_pcap(args.output, packets)

    print(f"wrote {args.output}: {len(packets)} packets")
    for number, (offset, frame, description) in enumerate(packets, start=1):
        print(f"{number:3d}  +{offset:.6f}s  {len(frame):4d} bytes  {description}")
    print("\nverify with:  tcpdump -r %s -nn" % args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
