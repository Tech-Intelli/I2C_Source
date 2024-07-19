#include "PlatformStrategy.h"

/**
 * Loads a template file into a string.
 *
 * @param file_path The path to the file to load.
 * @param templateData The string where the file contents will be stored.
 *
 * @throws std::runtime_error If the file cannot be opened, is empty, or there is an error reading it.
 */
PlatformStrategy::PlatformStrategy(std::string_view platform)
{
    initialize(platform);
    template_str = std::make_unique<PromptTemplateParser>(templateData);
}
std::string PlatformStrategy::generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap)
{
    static thread_local std::string result;
    result = template_str->render(replacementsMap);
    return result;
}
void PlatformStrategy::loadTemplate(const std::string &file_path, std::string &templateData)
{

    std::ifstream file(file_path, std::ios::in | std::ios::binary | std::ios::ate);
    if (!file.is_open())
    {
        throw std::runtime_error("Could not open file: " + file_path);
    }

    // Get the size of the file
    std::streamsize file_size = file.tellg();
    if (file_size == 0)
    {
        throw std::runtime_error("File is empty: " + file_path);
    }

    file.seekg(0, std::ios::beg);

    // Create a string with enough capacity to hold the file contents
    templateData.resize(file_size);

    // Read the file into the string
    if (!file.read(&templateData[0], file_size))
    {
        throw std::runtime_error("Error reading file: " + file_path);
    }
}

std::string PlatformStrategy::getFilePath(const std::string_view &platform)
{
    // Construct the file path
    std::string filePath = "../templates/";
    filePath.append(platform);
    filePath.append("_template.txt");

    return filePath;
}

void PlatformStrategy::initialize(const std::string_view &platform)
{
    filepath = getFilePath(platform);
    loadTemplate(filepath, templateData);
}
