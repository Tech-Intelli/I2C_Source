#pragma once

#include <array>
#include <string_view>
#include <optional>
#include "PersonaInfo.h"

/**
 * @brief A template class for managing and retrieving persona information associated with specific string keys.
 *
 * This class template provides a mechanism to store and retrieve `PersonaInfo` objects indexed by `std::string_view` keys.
 * It uses a fixed-size array of key-value pairs to store the data and provides methods to find and access the `PersonaInfo`
 * based on the given key.
 *
 * @tparam N The number of elements in the `personas` array.
 */
template <size_t N>
class PlatformPersonas
{
protected:
    /**
     * @brief An array of pairs where each pair contains a key (std::string_view) and the associated PersonaInfo.
     */
    std::array<std::pair<const std::string_view, PersonaInfo>, N> personas;

public:
    PlatformPersonas() = default;
    /**
     * @brief Constructs a PlatformPersonas object with the provided initialization data.
     *
     * @param init An array of key-value pairs to initialize the personas array.
     */
    PlatformPersonas(const std::array<std::pair<const std::string_view, PersonaInfo>, N> &init);

    /**
     * @brief Retrieves the PersonaInfo associated with the specified key.
     *
     * This method is an alias for the `find` method and provides the same functionality.
     *
     * @param key The key for which the PersonaInfo is to be retrieved.
     * @return std::optional<PersonaInfo> The PersonaInfo associated with the key, or std::nullopt if not found.
     */
    std::optional<PersonaInfo> getPersonaInfo(std::string_view key) const;

private:
    /**
     * @brief Finds the PersonaInfo associated with the specified key.
     *
     * Searches the array for a pair with the given key and returns the corresponding PersonaInfo if found.
     *
     * @param key The key for which the PersonaInfo is to be found.
     * @return std::optional<PersonaInfo> The PersonaInfo associated with the key, or std::nullopt if not found.
     */
    std::optional<PersonaInfo> find(std::string_view key) const;
};

// Definitions for the template class member functions
template <size_t N>
PlatformPersonas<N>::PlatformPersonas(const std::array<std::pair<const std::string_view, PersonaInfo>, N> &init) : personas(init) {}

template <size_t N>
std::optional<PersonaInfo> PlatformPersonas<N>::find(std::string_view key) const
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

template <size_t N>
std::optional<PersonaInfo> PlatformPersonas<N>::getPersonaInfo(std::string_view key) const
{
    return find(key);
}
