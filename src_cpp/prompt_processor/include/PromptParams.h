#pragma once
#include <string_view>
#include "SocialMediaConsts.h"
#include "PromptConsts.h"

struct PromptParams
{
  SocialMedia social_media;
  std::string_view visual_description;
  std::string_view context;
  int hashtag_limit;
  CaptionSize caption_size;

  PromptParams(SocialMedia social_media,
               std::string_view visual_description,
               std::string_view context,
               int hashtag_limit,
               CaptionSize caption_size)
      : social_media(social_media),
        visual_description(visual_description),
        context(context),
        hashtag_limit(hashtag_limit),
        caption_size(caption_size) {}
};
