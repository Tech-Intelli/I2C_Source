
#include <iostream>
#include <string_view>
#include "Logging.h"
#include "SocialMediaConsts.h"
#include "PromptStrategy.h"
#include "PlatformPersonas.h"
#include "PersonaConsts.h"

int main()
{
    Log::init();

    PromptStrategy prompt;

    PromptParams params = PromptParams(SocialMedia::INSTAGRAM, // social media platform to use
                                       "visual description",   // visual description of the content
                                       "context",              // context of the content
                                       3,                      // limit on the number of hashtags to include in the prompt
                                       CaptionSize::SMALL,     // caption size
                                       "tone",                 // tone of the content
                                       "style",
                                       Personas::BEAUTY_GURU // style of the content
    );
    prompt.getPrompt(params);

    PromptParams params1 = PromptParams(SocialMedia::TWITTER, // social media platform to use
                                        "visual description", // visual description of the content
                                        "context",            // context of the content
                                        3,                    // limit on the number of hashtags to include in the prompt
                                        CaptionSize::SMALL,   // caption size
                                        "tone",               // tone of the content
                                        "style",
                                        Personas::BEAUTY_GURU // style of the content
    );
    prompt.getPrompt(params1);

    return 0;
}
