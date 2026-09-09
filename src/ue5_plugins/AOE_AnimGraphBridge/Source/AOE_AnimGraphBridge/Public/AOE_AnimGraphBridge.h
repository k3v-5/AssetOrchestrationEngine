#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

class FAOE_AnimGraphBridgeModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
