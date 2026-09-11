using UnrealBuildTool;

public class AOE_AnimGraphBridge : ModuleRules
{
	public AOE_AnimGraphBridge(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = ModuleRules.PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(
			new string[]
			{
				"Core",
			}
		);

		PrivateDependencyModuleNames.AddRange(
			new string[]
			{
				"CoreUObject",
				"Engine",
				"Slate",
				"SlateCore",
				"UnrealEd",
				"AnimGraph",
				"BlueprintGraph",
				"ToolMenus"
			}
		);
	}
}
