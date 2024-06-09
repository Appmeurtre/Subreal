#include "SubrealCore.h"
#include "Modules/ModuleManager.h"

#include "Log.h"

void FSubrealCore::StartupModule()
{
	UE_LOG(LogSubrealCore, Log, TEXT("SubrealCore module starting up"));
}

void FSubrealCore::ShutdownModule()
{
	UE_LOG(LogSubrealCore, Log, TEXT("SubrealCore module shutting down"));
}

IMPLEMENT_PRIMARY_GAME_MODULE(FSubrealCore, SubrealCore, "SubrealCore");
