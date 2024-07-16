#pragma once
#include <string_view>
#include "SocialMediaConsts.h"

struct PromptParams
{
  SocialMedia social_media;
  std::string_view visual_description;
  std::string_view context;
  int hashtag_limit;
  // Add other parameters if necessary

  PromptParams(SocialMedia social_media,
               std::string_view visual_description,
               std::string_view context,
               int hashtag_limit)
      : social_media(social_media),
        visual_description(visual_description),
        context(context),
        hashtag_limit(hashtag_limit) {}
};
