#pragma once
#include <string>
#include <tuple>

struct ModelSelectionConfig {
    std::string model_name;
};

struct ChromaDBConfig {
    std::string blip;
    std::string llava;
};

struct MultiModalConfig {
    std::string blip;
    std::string vit;
    std::string llava;
};

struct Variants {
    std::string phi3;
    std::string llama3;
    std::string gemma2;
};

struct OllamaConfig {
    Variants variants;
    std::string use;
    int temperature;
    float top_p;
    bool stream;
};

struct ImageCompressionConfig {
    std::string type;
    bool compress;
    int compression_quality;
    float resize_factor;
};

struct TransformConfig {
    std::tuple<int, int> resize;
    int center_crop;
};

struct AppConfig {
    MultiModalConfig multimodal;
    OllamaConfig ollama;
    ImageCompressionConfig image_compression;
    TransformConfig transform_config;
    ModelSelectionConfig model_selection;
    ChromaDBConfig chroma_db;

    void validate();
};
