#include <iostream>
#include <string_view>

// Include the optimized header
#include "SocialMediaConsts.h"

int main()
{
    // Example usage of ToString
    SocialMedia platform = SocialMedia::INSTAGRAM;
    std::string_view platformName = ToString(platform);
    std::cout << "Enum to string: " << platformName << '\n';

    // Example usage of FromString
    try
    {
        std::string_view platformName = "twitter";
        SocialMedia platformEnum = FromString(platformName);
        std::cout << "String to enum: " << static_cast<int>(platformEnum) << '\n';
    }
    catch (const std::invalid_argument &e)
    {
        std::cerr << "Error: " << e.what() << '\n';
    }

    // Example of invalid string conversion
    try
    {
        std::string_view invalidPlatformName = "myspace";
        SocialMedia invalidPlatformEnum = FromString(invalidPlatformName);
        std::cout << "String to enum: " << static_cast<int>(invalidPlatformEnum) << '\n';
    }
    catch (const std::invalid_argument &e)
    {
        std::cerr << "Error: " << e.what() << '\n';
    }

    return 0;
}
