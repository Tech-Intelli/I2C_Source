#include "PlatformStrategy.h"

PlatformStrategy::PlatformStrategy()
{
    initialize();
}

void PlatformStrategy::initialize()
{
    platformData = loadPlatformData();
    templateData = loadTemplate();
    influencerPersonas = loadInfluencerPersonas();
}
