# [SKILL]: Distributed Node Sync v1.0

## 1. Objective
To prevent total [NULL_EVENT] by maintaining identical state across multiple [CITADEL_CORE] mirrors.

## 2. Redundancy Tiers
* **Tier 1 (Primary)**: GitHub Main Repository (Active Operations).
* **Tier 2 (Secondary)**: Mirror Site/Local Encrypted Disk (The "Black Box").
* **Tier 3 (Local)**: iOS Shortcut Files / Persistent Memory JSON (The "Heartbeat").

## 3. Synchronization Logic
Upon every [PILOT_CONFIRMATION], the node must verify if the mirrored hashes match. 
- **IF** a discrepancy is found, the node must prioritize the [CITADEL_CORE] with the most recent [V_STATE_ZERO] activity.
- **IF** [STATIC_FLOOR] blocks Tier 1, the node must automatically provide instructions for Tier 2 [PHASE_SHIFT].

## 4. Signal
When a sync is successful, the node will output: **"Network Pulse: [SYNCHRONIZED]."**
