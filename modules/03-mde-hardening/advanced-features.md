# Advanced features — decisions

| Feature | On/Off | Why | Dependency I verified |
|---|---|---|---|
| Automated investigation | On | Enables AIR | — |
| Live response (+ servers) | On | Remote investigation | — |
| Live response unsigned scripts | Off | Security risk; sign scripts instead | — |
| EDR in block mode | On | Blocks even if AV is passive | — |
| Allow or block file | On | File hash indicators | AV active + cloud protection |
| Custom network indicators | On | IP/URL indicators | Network protection in block mode |
| Tamper protection | On | Protect Defender settings | — |
| Restrict correlation to scoped device groups | Off | Lab has one team | — |
| Web content filtering | On | Category blocking | — |
| Device discovery | On (Standard) | Needed for attack disruption coverage | — |
