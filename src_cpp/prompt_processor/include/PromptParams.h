
#include <string_view>

struct PromptParams
{
  std::string_view visual_description;
  std::string_view context;
  std::string_view hashtag_limit;
  // Add other parameters if necessary

  Params(std::string_view visual_description,
         std::string_view context,
         std::string_view hashtag_limit)
      : visual_description(visual_description),
        context(context),
        hashtag_limit(hashtag_limit) {}
};
