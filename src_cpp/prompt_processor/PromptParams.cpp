#include "PromptParams.h"

/**
 * @brief Constructs a PromptParams object with the specified parameters.
 *
 * @param social_media The social media platform for which the prompt is generated.
 * @param visual_description A brief description of the visual content or image.
 * @param context The contextual background or information relevant to the prompt.
 * @param hashtag_limit The maximum number of hashtags allowed or desired in the prompt.
 * @param caption_size The size of the caption.
 * @param tone The tone of the prompt.
 * @param style The style of the prompt.
 * @param persona The persona of the influencer.
 */
PromptParams::PromptParams(SocialMedia social_media, std::string_view visual_description, std::string_view context, int hashtag_limit, CaptionSize caption_size, std::string tone, std::string style, std::string_view persona) : social_media(social_media),
                                                                                                                                                                                                                                  visual_description(visual_description),
                                                                                                                                                                                                                                  context(context),
                                                                                                                                                                                                                                  hashtag_limit(hashtag_limit),
                                                                                                                                                                                                                                  caption_size(caption_size),
                                                                                                                                                                                                                                  tone(tone),
                                                                                                                                                                                                                                  style(style),
                                                                                                                                                                                                                                  persona(persona) {}
