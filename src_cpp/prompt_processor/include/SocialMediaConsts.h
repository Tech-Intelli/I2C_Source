#pragma once

#include <string_view>
#include <array>
#include <stdexcept>

enum class SocialMedia
{
    INSTAGRAM,
    TWITTER,
    LINKEDIN,
    FACEBOOK,
    TIKTOK,
    COUNT
};

constexpr std::array<std::string_view, static_cast<size_t>(SocialMedia::COUNT)> socialMediaNames = {
    "instagram",
    "twitter",
    "linkedin",
    "facebook",
    "tiktok"};

constexpr std::string_view ToString(SocialMedia platform)
{
    size_t index = static_cast<size_t>(platform);
    if (index < socialMediaNames.size())
    {
        return socialMediaNames[index];
    }
    throw std::out_of_range("Invalid SocialMedia enum value");
}

constexpr SocialMedia FromString(std::string_view str)
{
    for (size_t i = 0; i < socialMediaNames.size(); ++i)
    {
        if (socialMediaNames[i] == str)
        {
            return static_cast<SocialMedia>(i);
        }
    }
    throw std::invalid_argument("Invalid social media string");
}
