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
    explicit PromptTemplateParser(std::string template_str);
    std::string render(const std::unordered_map<std::string, std::string> replacements) const;
};
