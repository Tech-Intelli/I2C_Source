#pragma once

#include "PromptStrategyFactory.h"
#include <string>
#include <unordered_map>
#include <stdexcept>
#include <iostream>
#include "logging.h"

class PromptFactory
{
public:
    PromptFactory() = default;

    std::string_view getPrompt(const std::unordered_map<std::string, std::string> &params);
};
