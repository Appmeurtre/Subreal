using UnrealBuildTool;
using System.Collections.Generic;

public class SubrealEditorTarget : TargetRules
{
	public SubrealEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.V2;
		ExtraModuleNames.AddRange( new string[] { "SubrealCore" } );
	}
}
