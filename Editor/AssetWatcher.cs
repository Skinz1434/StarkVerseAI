using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;

public class AssetWatcher : AssetPostprocessor
{
    private const string LogPath = "project_log.json";
    private static readonly object FileLock = new object();

    static void OnPostprocessAllAssets(
        string[] importedAssets,
        string[] deletedAssets,
        string[] movedAssets,
        string[] movedFromAssetPaths)
    {
        foreach (string path in importedAssets)
        {
            if (path.StartsWith("AI_Generated/", StringComparison.OrdinalIgnoreCase))
            {
                string agent = GetAgentFromPath(path);
                LogToProjectLog(agent, "import", path, "Completed");
                Debug.Log($"[AssetWatcher] Imported {path} by {agent}");
            }
        }
    }

    private static string GetAgentFromPath(string path)
    {
        // Expecting path AI_Generated/AgentName/...  fallback UnknownAgent
        string[] parts = path.Split('/');
        return parts.Length > 1 ? parts[1] : "UnknownAgent";
    }

    /// <summary>
    /// Appends a structured entry to project_log.json for dashboard consumption.
    /// </summary>
    /// <param name="agent">Agent responsible for the action</param>
    /// <param name="action">Action performed (import, move, etc.)</param>
    /// <param name="filePath">Path to the asset</param>
    /// <param name="status">Status string</param>
    public static void LogToProjectLog(string agent, string action, string filePath, string status)
    {
        lock (FileLock)
        {
            List<LogEntry> log = new List<LogEntry>();
            if (File.Exists(LogPath))
            {
                try
                {
                    string json = File.ReadAllText(LogPath);
                    log = JsonUtility.FromJson<LogWrapper>(json)?.entries ?? new List<LogEntry>();
                }
                catch (Exception ex)
                {
                    Debug.LogError($"[AssetWatcher] Failed to parse project log: {ex.Message}");
                }
            }
            log.Add(new LogEntry
            {
                timestamp = DateTime.UtcNow.ToString("o"),
                agent = agent,
                action = action,
                file = filePath.Replace("\\", "/"),
                status = status
            });

            string output = JsonUtility.ToJson(new LogWrapper { entries = log }, true);
            File.WriteAllText(LogPath, output);
            AssetDatabase.Refresh();
        }
    }

    [Serializable]
    private class LogWrapper
    {
        public List<LogEntry> entries = new List<LogEntry>();
    }

    [Serializable]
    private class LogEntry
    {
        public string timestamp;
        public string agent;
        public string action;
        public string file;
        public string status;
    }
}
