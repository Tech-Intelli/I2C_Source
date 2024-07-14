#include "ConfigModels.h"
#include <stdexcept>

void AppConfig::validate() {
    // Validate MultiModalConfig
    if (multimodal.blip.empty()) {
        throw std::invalid_argument("The 'blip' field in MultiModalConfig must be a non-empty string.");
    }
    if (multimodal.vit.empty()) {
        throw std::invalid_argument("The 'vit' field in MultiModalConfig must be a non-empty string.");
    }

    // Validate OllamaConfig
    if (ollama.variants.phi3.empty()) {
        throw std::invalid_argument("The 'phi3' field in Variants must be a non-empty string.");
    }
    if (ollama.variants.llama3.empty()) {
        throw std::invalid_argument("The 'llama3' field in Variants must be a non-empty string.");
    }
    if (ollama.variants.gemma2.empty()) {
        throw std::invalid_argument("The 'gemma2' field in Variants must be a non-empty string.");
    }
    if (ollama.use.empty()) {
        throw std::invalid_argument("The 'use' field in OllamaConfig must be a non-empty string.");
    }

    // Validate ImageCompressionConfig
    if (image_compression.type.empty()) {
        throw std::invalid_argument("The 'type' field in ImageCompressionConfig must be a non-empty string.");
    }

    // Validate ModelSelectionConfig
    if (model_selection.model_name.empty()) {
        throw std::invalid_argument("The 'model_name' field in ModelSelectionConfig must be a non-empty string.");
    }

    // Validate ChromaDBConfig
    if (chroma_db.blip.empty()) {
        throw std::invalid_argument("The 'blip' field in ChromaDBConfig must be a non-empty string.");
    }
    if (chroma_db.llava.empty()) {
        throw std::invalid_argument("The 'llava' field in ChromaDBConfig must be a non-empty string.");
    }
}
