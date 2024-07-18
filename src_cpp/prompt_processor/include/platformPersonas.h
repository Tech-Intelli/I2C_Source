#include <array>
#include <string_view>
#include <unordered_map>
#include <optional>
#include <algorithm>
#include <memory>
#include <stdexcept>
#include "personaInfo.h"
#include <cstring>

// Base class for platform personas
template <size_t N>
class PlatformPersonas
{
protected:
    std::array<std::pair<const char *, PersonaInfo>, N> personas;

public:
    PlatformPersonas(const std::array<std::pair<const char *, PersonaInfo>, N> &init) : personas(init) {}

    std::optional<PersonaInfo> find(const char *key) const
    {
        for (const auto &persona : personas)
        {
            if (std::strcmp(persona.first, key) == 0)
            {
                return persona.second;
            }
        }
        return std::nullopt;
    }

    std::optional<PersonaInfo> getPersonaInfo(const char *key) const
    {
        return find(key);
    }
};