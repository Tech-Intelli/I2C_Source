#pragma once

#include <string_view>

/**
 * @struct PersonaInfo
 * @brief Represents detailed information about a persona.
 *
 * The `PersonaInfo` struct holds essential details about a persona, including:
 * - `niche`: The specific area or topic the persona focuses on.
 * - `style_description`: A description of the persona's style or approach.
 * - `content_focus`: The primary content areas or themes the persona is interested in.
 *
 * This struct is intended for use in various contexts where persona information is needed,
 * such as in content generation systems, user profiling, and analytics.
 */
struct PersonaInfo
{
    /**
     * @brief The niche of the persona.
     *
     * This represents the specific area or topic that the persona specializes in.
     * It is intended to give context about the persona's area of expertise or interest.
     */
    const std::string_view niche;

    /**
     * @brief The style description of the persona.
     *
     * This describes the style or approach that the persona uses in their content or interactions.
     * It provides insight into how the persona presents information or engages with their audience.
     */
    const std::string_view style_description;

    /**
     * @brief The content focus of the persona.
     *
     * This indicates the primary content areas or themes that the persona is interested in or addresses.
     * It helps in understanding what topics or types of content the persona produces or engages with most.
     */
    const std::string_view content_focus;
};
