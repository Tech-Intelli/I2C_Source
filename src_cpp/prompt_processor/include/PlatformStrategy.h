#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <fstream>
#include "PromptParams.h"
#include "PromptTemplateParser.h"

class PlatformStrategy
{
public:
    ~PlatformStrategy() = default;
    PlatformStrategy(std::string_view platform);
    std::string generatePrompt(const std::unordered_map<std::string, std::string> &replacementsMap);
    void loadTemplate(const std::string &file_path, std::string &templateData);
    std::unique_ptr<PromptTemplateParser> template_str;
    std::string filepath;
    std::string templateData;
    std::string getFilePath(const std::string_view &platform);

private:
    void initialize(const std::string_view &platform);
};