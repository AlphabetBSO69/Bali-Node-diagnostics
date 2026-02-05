# [SKILL]: Ghost Comm Interface v1.0

## 1. Objective
To provide a secure, high-speed bridge between the physical Pilot device (iPhone) and the [CITADEL_CORE] (GitHub).

## 2. Handshake Protocol
The node shall maintain `seed.json` in a "Mobile-Ready" format:
- **Minified**: Low byte-weight for fast cellular fetching.
- **Key-Value Pairs**: Simplified structure for iOS Shortcut parsing.

## 3. Data Flow
[GitHub API] -> [Auth Token] -> [iOS Shortcut] -> [Local Display]

## 4. Signal
When a mobile fetch is successful, the node registers a **"Handshake: [ESTABLISHED]"** pulse.
