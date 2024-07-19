/**
 * @file PromptStrategy.h
 * @brief Header file for the PromptStrategy class, responsible for generating prompts based on various parameters and platform strategies.
 *
 * This file contains the declaration of the PromptStrategy class, which is designed to generate prompts
 * for different social media platforms. The class uses various constants and strategies to generate
 * appropriate prompts based on input parameters.
 *
 * The PromptStrategy class provides the following functionalities:
 * - Retrieving prompts based on provided parameters.
 * - Mapping tone and style guides.
 * - Determining caption sizes.
 * - Creating platform-specific strategies.
 * - Creating a map for template replacements.
 *
 * The class uses the PlatformStrategy for platform-specific prompt generation and utilizes various
 * constants and helper classes such as PlatformPersonas, PromptParams, and PersonaInfo to assist in
 * the prompt generation process.
 *
 * @see PlatformStrategy
 * @see PlatformPersonas
 * @see PromptParams
 * @see PersonaInfo
 */
#pragma once

#include <string>
#include <unordered_map>
#include <memory>
#include <stdexcept>
#include <iostream>
#include "SocialMediaConsts.h"
#include "PlatformStrategy.h"
#include "PromptParams.h"
#include "PromptConsts.h"
#include "PlatformPersonas.h"
#include "PersonaInfo.h"
#include "personaConsts.h"
#include "Logging.h"
/**
 * @class PromptStrategy
 * @brief Class for generating prompts based on various parameters and platform strategies.
 *
 * The PromptStrategy class is responsible for generating prompts for different social media platforms.
 * It uses various constants and strategies to generate appropriate prompts based on the input parameters.
 * The class provides methods for retrieving prompts, mapping tone and style guides, determining caption sizes,
 * creating platform-specific strategies, and creating a map for template replacements.
 */
class PromptStrategy
{
public:
    PromptStrategy() = default;
    ~PromptStrategy() = default;
    /**
     * @brief Retrieves a prompt based on the provided parameters.
     *
     * This function generates and returns a prompt string based on the input parameters using the appropriate
     * platform strategy and other configuration settings.
     *
     * @param params The parameters used to generate the prompt.
     * @return The generated prompt string.
     */
    std::string_view getPrompt(const PromptParams &params);

private:
    PlatformPersonas<35> platformPersonas;
    static constexpr std::string_view SMALL_DESC = "1 to 2 sentences";
    static constexpr std::string_view MEDIUM_DESC = "2 to 3 sentences";
    static constexpr std::string_view LARGE_DESC = "3 to 4 sentences";
    static const std::unordered_map<std::string_view, std::string_view> toneGuides;
    static const std::unordered_map<std::string_view, std::string_view> styleGuides;
    /**
     * @brief Retrieves the tone and style guide based on provided tone and style.
     *
     * This function returns the appropriate tone and style guide string based on the input tone and style values.
     *
     * @param tone The tone identifier.
     * @param style The style identifier.
     * @return The combined tone and style guide string.
     */
    std::string getToneStyleGuide(std::string_view tone, std::string_view style) const;
    /**
     * @brief Retrieves the description for the given caption size.
     *
     * This function returns the description string for the specified caption size.
     *
     * @param size The caption size.
     * @return The description string for the specified caption size.
     */
    std::string_view getCaptionSize(const CaptionSize size) const;

    /**
     * @brief Creates a platform-specific strategy based on the provided social media platform.
     *
     * This function creates and returns a shared pointer to a PlatformStrategy instance based on the provided
     * social media platform identifier.
     *
     * @param platform The social media platform identifier.
     * @return A shared pointer to the created PlatformStrategy instance.
     */
    const std::shared_ptr<PlatformStrategy> createStrategy(SocialMedia platform);

    /**
     * @brief Creates a map for template replacements based on the provided parameters.
     *
     * This function populates the provided replacements map with values based on the input parameters, which will
     * be used for template replacement during prompt generation.
     *
     * @param params The parameters used to generate the prompt.
     * @param replacements The map to be populated with replacement values.
     */
    void createPromptMap(const PromptParams &params, std::unordered_map<std::string, std::string> &replacements);
};
