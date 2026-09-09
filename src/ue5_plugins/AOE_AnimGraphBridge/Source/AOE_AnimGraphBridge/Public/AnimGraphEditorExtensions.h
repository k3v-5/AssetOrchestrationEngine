#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "Animation/AnimBlueprint.h"
#include "AnimGraphEditorExtensions.generated.h"

/**
 * Exposes internal AnimGraph wiring functions to Python for the AOE Orchestrator.
 */
UCLASS()
class AOE_ANIMGRAPHBRIDGE_API UAnimGraphEditorExtensions : public UBlueprintFunctionLibrary
{
	GENERATED_BODY()

public:

	/**
	 * Creates a physics node (AnimDynamics or KawaiiPhysics) in the AnimGraph and wires it before the Output Pose.
	 *
	 * @param TargetAnimBP   The Animation Blueprint to modify.
	 * @param BoneName       The name of the bone to drive.
	 * @param PhysicsType    "AnimDynamics" or "KawaiiPhysics".
	 * @param Stiffness      Stiffness parameter.
	 * @param Damping        Damping parameter.
	 * @return               True if the node was successfully created and wired.
	 */
	UFUNCTION(BlueprintCallable, Category = "AOE|AnimGraph")
	static bool CreateAndWirePhysicsNode(UAnimBlueprint* TargetAnimBP, FName BoneName, FString PhysicsType, float Stiffness, float Damping);
};
