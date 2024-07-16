#include "PromptFactory.h"

std::string_view PromptFactory::getPrompt(const std::unordered_map<std::string, std::string> &params)
{
    try
    {
        // Convert string to SocialMedia enum
        SocialMedia socialMedia = FromString(params.at("social_media"));
        auto strategy = SocialMediaStrategyFactory::createStrategy(socialMedia);
        std::string_view prompt = strategy->generatePrompt(params);
        return prompt;
    }
    catch (const std::invalid_argument &e)
    {
        log.error("Invalid social media platform or parameter: ", e.what());
        return "Error: Invalid social media platform or parameter specified.";
    }
    catch (const std::out_of_range &e)
    {
        log.error("Missing required parameter: " << e.what(), std::endl);
        return "Error: Missing required parameter.";
    }
    catch (const std::exception &e)
    {
        log.error("An unexpected error occurred: " << e.what(), std::endl);
        return "Error: An unexpected error occurred. Please try again later.";
    }
}