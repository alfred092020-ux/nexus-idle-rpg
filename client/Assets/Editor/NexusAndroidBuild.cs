using System;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.Build.Reporting;

public static class NexusAndroidBuild
{
    public static void PerformBuild()
    {
        string output = GetArgument("-buildOutput");
        if (string.IsNullOrWhiteSpace(output))
        {
            throw new ArgumentException("Missing required -buildOutput argument.");
        }

        string directory = Path.GetDirectoryName(output);
        if (!string.IsNullOrEmpty(directory))
        {
            Directory.CreateDirectory(directory);
        }

        string[] scenes = EditorBuildSettings.scenes
            .Where(scene => scene.enabled)
            .Select(scene => scene.path)
            .ToArray();
        if (scenes.Length == 0)
        {
            throw new InvalidOperationException("No enabled scenes are configured for the build.");
        }

        ConfigureInputBackends();
        EditorUserBuildSettings.buildAppBundle = false;
        PlayerSettings.SetScriptingBackend(BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
        var options = new BuildPlayerOptions
        {
            scenes = scenes,
            locationPathName = output,
            target = BuildTarget.Android,
            options = BuildOptions.None,
        };

        BuildReport report = BuildPipeline.BuildPlayer(options);
        if (report.summary.result != BuildResult.Succeeded)
        {
            throw new InvalidOperationException(
                $"Android build failed: {report.summary.result} ({report.summary.totalErrors} errors)."
            );
        }
    }

    private static void ConfigureInputBackends()
    {
        var getter = typeof(PlayerSettings)
            .GetMethods(BindingFlags.Static | BindingFlags.Public | BindingFlags.NonPublic)
            .FirstOrDefault(method =>
                method.Name == "GetSerializedObject" && method.GetParameters().Length == 0);
        if (getter == null || !(getter.Invoke(null, null) is SerializedObject settings))
        {
            throw new InvalidOperationException("Unable to access serialized PlayerSettings.");
        }

        settings.Update();
        SerializedProperty inputHandler = settings.FindProperty("activeInputHandler");
        if (inputHandler == null)
        {
            throw new InvalidOperationException("PlayerSettings.activeInputHandler is unavailable.");
        }
        inputHandler.intValue = 2; // Both: legacy Input Manager + new Input System.
        settings.ApplyModifiedProperties();
    }

    private static string GetArgument(string name)
    {
        string[] args = Environment.GetCommandLineArgs();
        for (int i = 0; i < args.Length - 1; i++)
        {
            if (string.Equals(args[i], name, StringComparison.Ordinal))
            {
                return args[i + 1];
            }
        }
        return null;
    }
}
