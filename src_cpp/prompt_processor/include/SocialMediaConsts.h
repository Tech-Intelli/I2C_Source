
#pragma once

#include <string_view>
#include <array>
#include <stdexcept>

/**
 * @file SocialMedia.h
 * @brief Defines enumeration for social media platforms and provides conversion functions.
 *
 * This file defines an enumeration `SocialMedia` for various social media platforms and provides
 * utility functions to convert between `SocialMedia` enum values and their corresponding string
 * representations.
 *
 * The `SocialMedia` enum class includes the following platforms:
 * - INSTAGRAM
 * - TWITTER
 * - LINKEDIN
 * - FACEBOOK
 * - TIKTOK
 *
 * Additionally, functions are provided for:
 * - Converting from `SocialMedia` enum to `std::string_view` using the `ToString` function.
 * - Converting from `std::string_view` to `SocialMedia` enum using the `FromString` function.
 *
 * @enum SocialMedia
 * @brief Enum class for representing various social media platforms.
 *
 * Enumerators:
 * - INSTAGRAM: Represents Instagram.
 * - TWITTER: Represents Twitter.
 * - LINKEDIN: Represents LinkedIn.
 * - FACEBOOK: Represents Facebook.
 * - TIKTOK: Represents TikTok.
 * - COUNT: Represents the number of social media platforms. This is used for sizing arrays.
 *
 */

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

/**
 * @function constexpr std::string_view ToString(SocialMedia platform)
 * @brief Converts a `SocialMedia` enum value to its string representation.
 *
 * @param platform The `SocialMedia` enum value to convert.
 *
 * @return Corresponding string representation of the `SocialMedia` enum value.
 *
 * @throws std::out_of_range if the enum value is not within the valid range.
 */
constexpr std::string_view ToString(SocialMedia platform)
{
    size_t index = static_cast<size_t>(platform);
    if (index < socialMediaNames.size())
    {
        return socialMediaNames[index];
    }
    throw std::out_of_range("Invalid SocialMedia enum value");
}

/**
 * @function constexpr SocialMedia FromString(std::string_view str)
 * @brief Converts a string representation of a social media platform to the corresponding `SocialMedia` enum value.
 *
 * @param str The string representation of the social media platform.
 *
 * @return The corresponding `SocialMedia` enum value.
 *
 * @throws std::invalid_argument If the input string is not a valid social media platform.
 *
 */
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
