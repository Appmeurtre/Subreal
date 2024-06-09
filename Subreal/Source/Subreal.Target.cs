using UnrealBuildTool;

public class SubrealTarget : TargetRules
{
	public SubrealTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.V2;
		ExtraModuleNames.AddRange( new string[] { "SubrealCore" } );
	}
}
