#pragma once
/**
 * @enum CaptionSize
 * @brief Enumeration for defining the size of captions in content.
 *
 * The `CaptionSize` enum class is used to specify the size of captions in content such as social media posts,
 * marketing materials, or any other content where text size needs to be categorized. It provides three
 * distinct size options that can be utilized for formatting and display purposes.
 *
 * Example usage:
 * @code
 * CaptionSize size = CaptionSize::MEDIUM;
 * if (size == CaptionSize::LARGE) {
 *     // Apply large caption size formatting
 * }
 * @endcode
 */
enum class CaptionSize
{
    SMALL,
    MEDIUM,
    LARGE
};