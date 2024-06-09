#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleInterface.h"

class FSubrealCore : public IModuleInterface
{
public:
	static inline FSubrealCore& Get()
	{
		return FModuleManager::LoadModuleChecked<FSubrealCore>("SubrealCore");
	}

	static inline bool IsAvailable()
	{
		return FModuleManager::Get().IsModuleLoaded("SubrealCore");
	}

	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};
