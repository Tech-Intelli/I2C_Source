#include "PromptFactory.h"

std::string PromptFactory::getPrompt(const std::unordered_map<std::string, std::string> &params)
{
    try
    {
        // Convert string to SocialMedia enum
        SocialMedia socialMedia = FromString(params.at("social_media"));
        auto strategy = SocialMediaStrategyFactory::createStrategy(socialMedia);
        std::string prompt = strategy->generatePrompt(params);
        return prompt;
    }
    catch (const std::invalid_argument &e)
    {
        std::cerr << "Invalid social media platform or parameter: " << e.what() << std::endl;
        return "Error: Invalid social media platform or parameter specified.";
    }
    catch (const std::out_of_range &e)
    {
        std::cerr << "Missing required parameter: " << e.what() << std::endl;
        return "Error: Missing required parameter.";
    }
    catch (const std::exception &e)
    {
        std::cerr << "An unexpected error occurred: " << e.what() << std::endl;
        return "Error: An unexpected error occurred. Please try again later.";
    }
}