# Dashboard Agent Data Contract

This document defines how Unity writes progress data for the SkinZAI dashboard.

## Log Entry Format (`project_log.json`)

`project_log.json` contains an object with a single `entries` array. Each entry has:

| Field      | Type   | Description                                  |
| ---------- | ------ | -------------------------------------------- |
| `timestamp`| string | ISO8601 UTC timestamp                         |
| `agent`    | string | Name of the agent responsible                |
| `action`   | string | What happened (generate_mesh, write_script)  |
| `file`     | string | Relative path of the affected file           |
| `status`   | string | `Queued`, `InProgress`, `Completed`, `Error` |

Example entry:
```json
{
  "timestamp": "2025-06-14T10:00:00Z",
  "agent": "StarkAssets_AI",
  "action": "generate_mesh",
  "file": "AI_Generated/MK47/Models/MK47_v1.glb",
  "status": "Completed"
}
```

The dashboard reads this file periodically to display build progress, agent status cards, and the timeline feed.

Agents should keep file paths short and actions concise so that Aydan can follow along easily.
