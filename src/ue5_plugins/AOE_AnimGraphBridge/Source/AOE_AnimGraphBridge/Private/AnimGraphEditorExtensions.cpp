#include "AnimGraphEditorExtensions.h"
#include "Kismet2/BlueprintEditorUtils.h"
#include "AnimationGraph.h"
#include "AnimGraphNode_Root.h"
#include "AnimGraphNode_AnimDynamics.h"
// Soft reference to KawaiiPhysics to avoid fatal link errors if the plugin is missing
// #include "AnimGraphNode_KawaiiPhysics.h"

bool UAnimGraphEditorExtensions::CreateAndWirePhysicsNode(UAnimBlueprint* TargetAnimBP, FName BoneName, FString PhysicsType, float Stiffness, float Damping)
{
	if (!TargetAnimBP)
	{
		UE_LOG(LogTemp, Error, TEXT("AOE Bridge: TargetAnimBP is null."));
		return false;
	}

	// 1. Get the AnimGraph
	UAnimationGraph* AnimGraph = nullptr;
	for (UEdGraph* Graph : TargetAnimBP->UbergraphPages)
	{
		if (Graph && Graph->GetFName() == UEdGraphSchema_K2::GN_AnimGraph)
		{
			AnimGraph = Cast<UAnimationGraph>(Graph);
			break;
		}
	}

	if (!AnimGraph)
	{
		UE_LOG(LogTemp, Error, TEXT("AOE Bridge: AnimGraph not found in %s."), *TargetAnimBP->GetName());
		return false;
	}

	// 2. Find the Output Pose (Root Node)
	UAnimGraphNode_Root* RootNode = nullptr;
	for (UEdGraphNode* Node : AnimGraph->Nodes)
	{
		RootNode = Cast<UAnimGraphNode_Root>(Node);
		if (RootNode)
		{
			break;
		}
	}

	if (!RootNode)
	{
		UE_LOG(LogTemp, Error, TEXT("AOE Bridge: Output Pose (Root Node) not found."));
		return false;
	}

	// 3. Find the pin connected to the Output Pose
	UEdGraphPin* ResultPin = RootNode->GetPinAt(0); // The "Result" input pin
	if (!ResultPin) return false;

	UEdGraphPin* PreviousOutputPin = nullptr;
	if (ResultPin->LinkedTo.Num() > 0)
	{
		PreviousOutputPin = ResultPin->LinkedTo[0];
		ResultPin->BreakAllPinLinks(); // Disconnect to insert our new node in between
	}

	// 4. Instantiate the requested Physics Node
	UAnimGraphNode_Base* NewPhysicsNode = nullptr;

	if (PhysicsType == TEXT("KawaiiPhysics"))
	{
		// RN-03: Soft Dependency Check for KawaiiPhysics
		UClass* KawaiiClass = FindObject<UClass>(ANY_PACKAGE, TEXT("AnimGraphNode_KawaiiPhysics"));
		if (KawaiiClass)
		{
			NewPhysicsNode = Cast<UAnimGraphNode_Base>(FBlueprintEditorUtils::CreateNode(KawaiiClass, AnimGraph, FVector2D(RootNode->NodePosX - 300, RootNode->NodePosY), false));
			// Reflection could be used here to set Stiffness/Damping dynamically since we don't link the header directly
		}
		else
		{
			UE_LOG(LogTemp, Warning, TEXT("AOE Bridge ADVERTENCIA: KawaiiPhysics no esta habilitado. Por favor, instale/habilite el plugin KawaiiPhysics en Editar > Plugins para soportar estas dinamicas."));
			// Fallback: Reconnect original link so we don't break the graph
			if (PreviousOutputPin)
			{
				ResultPin->MakeLinkTo(PreviousOutputPin);
			}
			return false;
		}
	}
	else // Default to AnimDynamics
	{
		UAnimGraphNode_AnimDynamics* DynamicsNode = Cast<UAnimGraphNode_AnimDynamics>(FBlueprintEditorUtils::CreateNode(UAnimGraphNode_AnimDynamics::StaticClass(), AnimGraph, FVector2D(RootNode->NodePosX - 300, RootNode->NodePosY), false));
		if (DynamicsNode)
		{
			// Map parameters
			DynamicsNode->Node.BoundBone.BoneName = BoneName;
			// DynamicsNode->Node.Setup.SpringStiffness = Stiffness; (Requires Engine >= 5.1 structural mapping)

			NewPhysicsNode = DynamicsNode;
		}
	}

	if (!NewPhysicsNode) return false;

	// 5. Wire the new node
	UEdGraphPin* NewInputPin = NewPhysicsNode->GetPinAt(0); // ComponentPose In
	UEdGraphPin* NewOutputPin = NewPhysicsNode->GetPinAt(1); // Pose Out

	if (PreviousOutputPin && NewInputPin)
	{
		NewInputPin->MakeLinkTo(PreviousOutputPin);
	}

	if (NewOutputPin)
	{
		NewOutputPin->MakeLinkTo(ResultPin);
	}

	// 6. Compile the Blueprint
	NewPhysicsNode->ReconstructNode();
	FBlueprintEditorUtils::MarkBlueprintAsStructurallyModified(TargetAnimBP);

	UE_LOG(LogTemp, Display, TEXT("AOE Bridge: Nodo %s inyectado y encadenado correctamente para el hueso %s."), *PhysicsType, *BoneName.ToString());

	return true;
}
