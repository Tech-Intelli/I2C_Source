#include <iostream>
#include <string_view>
#include "logging.h"
#include "SocialMediaConsts.h"

int main()
{
    Log::init();
    SocialMedia platform = SocialMedia::INSTAGRAM;
    std::string_view platformName = ToString(platform);
    log.info("Enum to string: ", platformName);

    try
    {
        std::string_view platformName = "twitter";
        SocialMedia platformEnum = FromString(platformName);
        log.info("String to enum: ", static_cast<int>(platformEnum));
    }
    catch (const std::invalid_argument &e)
    {
        log.error("Error: ", e.what());
    }

    try
    {
        std::string_view invalidPlatformName = "myspace";
        SocialMedia invalidPlatformEnum = FromString(invalidPlatformName);
        log.debug("String to enum: ", static_cast<int>(invalidPlatformEnum));
    }
    catch (const std::invalid_argument &e)
    {
        log.error("Error: ", e.what());
    }

    return 0;
}
