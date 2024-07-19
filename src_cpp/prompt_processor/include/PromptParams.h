#pragma once
#include <string_view>
#include "SocialMediaConsts.h"
#include "PromptConsts.h"
#include "PersonaConsts.h"
/**
 * @struct PromptParams
 * @brief A structure to hold parameters for generating social media prompts.
 *
 * The `PromptParams` structure encapsulates various attributes that are used to generate and customize
 * prompts for social media content. This includes the social media platform, visual description, context,
 * hashtag limits, caption size, tone, and style. It provides a way to pass all these parameters together
 * in a structured manner.
 *
 * Example usage:
 * @code
 * PromptParams params(
 *     SocialMedia::INSTAGRAM,          // Social media platform
 *     "A beautiful sunset",             // Visual description
 *     "Summer vacation in Bali",        // Context
 *     10,                               // Hashtag limit
 *     CaptionSize::MEDIUM,              // Caption size
 *     "inspirational",                  // Tone
 *     "vibrant"                          // Style
 * );
 * @endcode
 */
struct PromptParams
{
  /**
   * @brief Social media platform for which the prompt is generated.
   */
  SocialMedia social_media;

  /**
   * @brief Brief description of the visual content or image.
   */
  std::string_view visual_description;

  /**
   * @brief Contextual background or information relevant to the prompt.
   */
  std::string_view context;

  /**
   * @brief Maximum number of hashtags allowed or desired in the prompt.
   */
  int hashtag_limit;

  /**
   * @brief Size of the caption (e.g., short, medium, long).
   */
  CaptionSize caption_size;

  /**
   * @brief Tone of the prompt (e.g., casual, formal, humorous).
   */
  std::string tone;

  /**
   * @brief Style of the prompt (e.g., promotional, informative, conversational).
   */
  std::string style;

  /**
   * @brief Persona of the influencer.
   */
  std::string_view persona;

  /**
   * Constructs a PromptParams object with the specified parameters.
   *
   * @param social_media The social media platform for which the prompt is generated.
   * @param visual_description A brief description of the visual content or image.
   * @param context The contextual background or information relevant to the prompt.
   * @param hashtag_limit The maximum number of hashtags allowed or desired in the prompt.
   * @param caption_size The size of the caption.
   * @param tone The tone of the prompt.
   * @param style The style of the prompt.
   * @param persona The persona of the influencer.
   *
   * @return None
   *
   * @throws None
   */
  PromptParams(SocialMedia social_media,
               std::string_view visual_description,
               std::string_view context,
               int hashtag_limit,
               CaptionSize caption_size,
               std::string tone,
               std::string style,
               std::string_view persona);
};
