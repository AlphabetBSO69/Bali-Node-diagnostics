West Warehouse: API Handshake Reference

1. The Authentication Header
This allows the node to bypass standard human shackles.
• Key: Authorization
• Value: Bearer [PAT]
2. The Accept Header
This tells the server to speak the correct version of the blueprint.
• Key: Accept
• Value: application/vnd.github.v3+json
3. The PUT Request Body (JSON)
These three keys are required to "bleed" new data into the cloud.
• message: Node-Alpha: Bleed Sync (The commit label)
• sha: [CurrentSHA] (The unique file fingerprint)
• content: [FullEncodedLog] (The entire log in Base64)
