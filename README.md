# StarkVerseAI

This repository houses the StarkVerse AI pipeline and the SkinZAI Control Panel dashboard.

## Unity Folder Layout

- `AI_Generated/` – Agents drop generated assets here.
- `Assets/`, `Scripts/`, `Animations/`, `Prefabs/`, `Audio/`, `Metadata/` – Standard Unity folders.
- `Editor/AssetWatcher.cs` – Unity editor script that tracks new files and appends events to `project_log.json`.
- `project_log.json` – JSON event feed consumed by the SkinZAI dashboard.

## Workflow

1. **Codex Agents** write files inside `AI_Generated/<AgentName>/`.
2. **AssetWatcher** detects new assets when Unity refreshes and logs an entry.
3. **project_log.json** grows with each event and is committed back to GitHub.
4. **SkinZAI Dashboard** (see `dashboard/`) polls `project_log.json` to visualise build progress.

Entries look like:
```json
{
  "timestamp": "2025-06-14T10:00:00Z",
  "agent": "StarkAssets_AI",
  "action": "generate_mesh",
  "file": "AI_Generated/MK47/Models/MK47_v1.glb",
  "status": "Completed"
}
```

Keep the logs concise and fun—Aydan is watching!
