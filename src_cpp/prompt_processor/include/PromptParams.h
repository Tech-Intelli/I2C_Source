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
  std::string tone;
  std::string style;

  PromptParams(SocialMedia social_media,
               std::string_view visual_description,
               std::string_view context,
               int hashtag_limit,
               CaptionSize caption_size,
               std::string tone,
               std::string style)
      : social_media(social_media),
        visual_description(visual_description),
        context(context),
        hashtag_limit(hashtag_limit),
        caption_size(caption_size),
        tone(tone),
        style(style) {}
};
