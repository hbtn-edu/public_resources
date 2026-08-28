# Network Primitives Lab - starter bundle

```
starter/
├── reference_capture.pcap   # Task 4: the capture you analyse
├── make_capture.py          # how reference_capture.pcap is produced
├── docker-compose.yml       # Task 4 Option B: generate your own traffic
├── .env.example
└── README.md
```

---

## `reference_capture.pcap`

Twelve packets: one complete HTTP exchange over TCP (ten packets) and one DNS
lookup over UDP (two packets). All addresses are RFC 5737 documentation
addresses (`192.0.2.0/24`); no real host, no personal data, nothing captured
from a real network.

Read it exactly as:

```bash
tcpdump -r starter/reference_capture.pcap -nn
```

```
11:15:42.000000 IP 192.0.2.10.49722 > 192.0.2.20.80: Flags [S], seq 0, win 64240, length 0
11:15:42.000112 IP 192.0.2.20.80 > 192.0.2.10.49722: Flags [S.], seq 0, ack 1, win 65160, length 0
11:15:42.000138 IP 192.0.2.10.49722 > 192.0.2.20.80: Flags [.], ack 1, win 64240, length 0
11:15:42.000175 IP 192.0.2.10.49722 > 192.0.2.20.80: Flags [P.], seq 1:78, ack 1, win 64240, length 77: HTTP: GET /index.html HTTP/1.1
11:15:42.000283 IP 192.0.2.20.80 > 192.0.2.10.49722: Flags [.], ack 78, win 65160, length 0
11:15:42.000501 IP 192.0.2.20.80 > 192.0.2.10.49722: Flags [P.], seq 1:243, ack 78, win 65160, length 242: HTTP: HTTP/1.1 200 OK
11:15:42.000544 IP 192.0.2.10.49722 > 192.0.2.20.80: Flags [.], ack 243, win 64240, length 0
11:15:42.001220 IP 192.0.2.10.49722 > 192.0.2.20.80: Flags [F.], seq 78, ack 243, win 64240, length 0
11:15:42.001338 IP 192.0.2.20.80 > 192.0.2.10.49722: Flags [F.], seq 243, ack 79, win 65160, length 0
11:15:42.001371 IP 192.0.2.10.49722 > 192.0.2.20.80: Flags [.], ack 244, win 64240, length 0
11:15:42.010402 IP 192.0.2.10.51344 > 192.0.2.53.53: 26814+ A? example.com. (29)
11:15:42.011876 IP 192.0.2.53.53 > 192.0.2.10.51344: 26814 1/0/0 A 192.0.2.80 (45)
```

The timestamps print in *your* local timezone; the capture is stamped
2025-01-06 10:15:42 UTC. Everything else is identical on every machine.

Useful extra views:

```bash
tcpdump -r starter/reference_capture.pcap -nn -v      # IP headers, checksums
tcpdump -r starter/reference_capture.pcap -nn -A      # ASCII payloads
tcpdump -r starter/reference_capture.pcap -nn udp     # just the DNS pair
```

## `make_capture.py`

The capture is **synthesised**, not recorded..

```bash
python3 make_capture.py        # writes reference_capture.pcap
```

No dependencies - standard library only, so it runs anywhere. It self-checks
before writing: 12 packets, 10 TCP + 2 UDP, exactly 2 packets with a payload,
77-byte request, 242-byte response, 29-byte DNS query, 45-byte DNS answer.
If a future edit breaks one of those, the script fails instead of silently
shipping a capture the quiz no longer matches.

**One deliberate deviation from a real capture.** The initial sequence numbers
are 0. A real TCP stack randomises them, but tcpdump prints the SYN and
SYN-ACK sequence numbers *absolutely* (it only relativises later packets), so
a random ISN would make packets 1 and 2 read `seq 1000000000` instead of the
`seq 0`.

Everything else is faithful: valid IPv4/TCP/UDP checksums (`tcpdump -v` says
`cksum ... (correct)` on every packet), real DNS message encoding with a
compression pointer in the answer, DF set, TTL 64.

## `docker-compose.yml`

Task 4 Option B, the fallback when the supplied capture cannot be used: a
pinned nginx on `127.0.0.1:8080` to generate your own loopback traffic.

```bash
cd starter
docker compose up -d
curl http://localhost:8080
docker compose down
```

The image is pinned by patch version and digest. A capture you generate
yourself will have different ports, windows and packet counts.
