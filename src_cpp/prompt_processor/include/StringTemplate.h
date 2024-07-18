#include <string>
#include <string_view>
#include <unordered_map>
#include <regex>
#include <stdexcept>

class StringTemplate
{
private:
    std::string template_str;
    const std::regex placeholder_regex;

public:
    explicit StringTemplate(std::string template_str) : template_str(template_str), placeholder_regex(R"(\{([^}]+)\})") {}

    std::string render(const std::unordered_map<std::string, std::string> replacements) const
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
};
