#pragma once

#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <memory>

class Log
{
public:
    static Log &getInstance()
    {
        static Log instance;
        return instance;
    }

    static void init(const std::string &logger_name = "fast_logger")
    {
        auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
        console_sink->set_level(spdlog::level::trace);
        console_sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%s:%#] %!() [%^%-5l%$] [t%t] %v");

        auto logger = std::make_shared<spdlog::logger>(logger_name, console_sink);
        logger->set_level(spdlog::level::trace);
        spdlog::set_default_logger(logger);
    }

    template <typename... Args>
    void trace(const char *fmt, const Args &...args)
    {
        spdlog::trace(fmt, args...);
    }

    template <typename... Args>
    void debug(const char *fmt, const Args &...args)
    {
        spdlog::debug(fmt, args...);
    }

    template <typename... Args>
    void info(const char *fmt, const Args &...args)
    {
        spdlog::info(fmt, args...);
    }

    template <typename... Args>
    void warn(const char *fmt, const Args &...args)
    {
        spdlog::warn(fmt, args...);
    }

    template <typename... Args>
    void error(const char *fmt, const Args &...args)
    {
        spdlog::error(fmt, args...);
    }

    template <typename... Args>
    void critical(const char *fmt, const Args &...args)
    {
        spdlog::critical(fmt, args...);
    }

private:
    Log() = default;
    Log(const Log &) = delete;
    Log &operator=(const Log &) = delete;
};

#define log Log::getInstance()
