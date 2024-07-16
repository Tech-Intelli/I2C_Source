#pragma once

#include "PromptStrategyFactory.h"
#include <string>
#include <unordered_map>
#include <stdexcept>
#include <iostream>

class PromptFactory
{
public:
    PromptFactory() = default;

    std::string getPrompt(const std::unordered_map<std::string, std::string> &params);
};
