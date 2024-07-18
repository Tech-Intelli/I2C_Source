#include <array>
#include <string_view>
#include <unordered_map>
#include <optional>
#include <algorithm>
#include <memory>
#include <stdexcept>
#include "PersonaInfo.h"

template <size_t N>
class PlatformPersonas
{
protected:
    std::array<std::pair<const std::string_view, PersonaInfo>, N> personas;

public:
    PlatformPersonas(const std::array<std::pair<const std::string_view, PersonaInfo>, N> &init) : personas(init) {}

    std::optional<PersonaInfo> find(std::string_view key) const
    {
        for (const auto &persona : personas)
        {
            if (persona.first == key)
            {
                return persona.second;
            }
        }
        return std::nullopt;
    }

    std::optional<PersonaInfo> getPersonaInfo(std::string_view key) const
    {
        return find(key);
    }
};