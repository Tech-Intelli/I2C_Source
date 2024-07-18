#include "PromptTemplateParser.h"

/**
 * @brief Constructs a PromptTemplateParser with a given template string.
 *
 * @param template_str The template string containing placeholders to be replaced.
 */
PromptTemplateParser::PromptTemplateParser(std::string template_str) : template_str(template_str), placeholder_regex(R"(\{([^}]+)\})")
{
}

/**
 * Renders a template string by replacing placeholders with corresponding values from a map.
 *
 * @param replacements A map of placeholders and their corresponding values.
 *
 * @return The rendered template string.
 *
 * @throws std::runtime_error If a placeholder is not found in the replacements map.
 */
std::string PromptTemplateParser::render(const std::unordered_map<std::string, std::string> replacements) const
{
    std::string result = template_str;
    std::smatch match;
    std::string::const_iterator search_start(result.cbegin());

    while (std::regex_search(search_start, result.cend(), match, placeholder_regex))
    {
        std::string placeholder = match[1];

        // Find the replacement in the map
        auto it = replacements.find(placeholder);
        if (it == replacements.end())
        {
            throw std::runtime_error("Unknown placeholder: " + placeholder);
        }

        std::string replacement = it->second;
        result.replace(match.position() + (search_start - result.cbegin()), match.length(), replacement);
        search_start = result.cbegin() + (match.position() + replacement.length());
    }

    return result;
}