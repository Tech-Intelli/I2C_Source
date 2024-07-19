/**
 * @file PromptTemplateParser.h
 * @brief Header file for the PromptTemplateParser class, responsible for parsing and rendering template strings with placeholders.
 *
 * This file contains the declaration of the PromptTemplateParser class, which is designed to allow the creation
 * of a template string with placeholders. These placeholders, denoted by curly braces (e.g., {placeholder}),
 * can be replaced with actual values provided in a map during the rendering process.
 *
 * The class provides functionalities to:
 * - Initialize with a template string containing placeholders.
 * - Render the template string by replacing placeholders with actual values from a replacements map.
 *
 * Example usage:
 * @code
 * std::string template_str = "Hello, {name}! Welcome to {place}.";
 * PromptTemplateParser parser(template_str);
 * std::unordered_map<std::string, std::string> replacements = {
 *     {"name", "Alice"},
 *     {"place", "Wonderland"}
 * };
 * std::string result = parser.render(replacements);
 * // result: "Hello, Alice! Welcome to Wonderland."
 * @endcode
 */

#pragma once

#include <string>
#include <string_view>
#include <unordered_map>
#include <regex>
#include <stdexcept>
#include <iostream>

/**
 * @class PromptTemplateParser
 * @brief A class to parse and render template strings with placeholders.
 *
 * The `PromptTemplateParser` class allows for the creation of a template string with placeholders,
 * which can be replaced with actual values provided in a map. The placeholders are denoted with curly
 * braces (e.g., {placeholder}) and are replaced with corresponding values during the rendering process.
 *
 * Example usage:
 * @code
 * std::string template_str = "Hello, {name}! Welcome to {place}.";
 * PromptTemplateParser parser(template_str);
 * std::unordered_map<std::string, std::string> replacements = {
 *     {"name", "Alice"},
 *     {"place", "Wonderland"}
 * };
 * std::string result = parser.render(replacements);
 * // result: "Hello, Alice! Welcome to Wonderland."
 * @endcode
 */
class PromptTemplateParser
{
private:
    std::string template_str;
    const std::regex placeholder_regex;

public:
    /**
     * @brief Constructs a PromptTemplateParser with the given template string.
     *
     * This constructor initializes the PromptTemplateParser with a template string containing placeholders.
     *
     * @param template_str The template string with placeholders.
     */
    explicit PromptTemplateParser(std::string template_str);
    /**
     * @brief Renders the template string with replacements from the provided map.
     *
     * This function replaces the placeholders in the template string with corresponding values from the
     * replacements map. If a placeholder does not have a corresponding value in the map, it is left unchanged.
     *
     * @param replacements A map containing placeholder-value pairs for template replacement.
     * @return The rendered string with placeholders replaced by actual values.
     */
    std::string render(const std::unordered_map<std::string, std::string> replacements) const;
};
