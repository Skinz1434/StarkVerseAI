using UnityEditor;
using UnityEngine;
using System.IO;
using System;

public class StarkverseImporter : EditorWindow {
    [MenuItem("Tools/Starkverse/Sync AI Generated Content")]
    public static void SyncAssets() {
        string path = "Assets/AI_Generated/";
        string[] files = Directory.GetFiles(path, "*", SearchOption.AllDirectories);

        foreach (string file in files) {
            if (!file.EndsWith(".meta")) {
                Debug.Log("[Starkverse Import] Reimporting: " + file);
                AssetDatabase.ImportAsset(file, ImportAssetOptions.ForceUpdate);
            }
        }

        AssetDatabase.Refresh();
        Debug.Log("✅ Starkverse AI imports completed.");
        DisplayImportLog();
    }

    private static void DisplayImportLog() {
        string projectRoot = Path.GetFullPath(Path.Combine(Application.dataPath, ".."));
        string logPath = Path.Combine(projectRoot, "project_log.json");
        if (File.Exists(logPath)) {
            string json = File.ReadAllText(logPath);
            try {
                ProjectLog data = JsonUtility.FromJson<ProjectLog>(json);
                if (data != null && data.log != null) {
                    foreach (string entry in data.log) {
                        Debug.Log(entry);
                    }
                }
            } catch (Exception ex) {
                Debug.LogWarning("Failed to parse project_log.json: " + ex.Message);
            }
        }
    }

    [Serializable]
    private class ProjectLog {
        public string[] log;
    }
}
