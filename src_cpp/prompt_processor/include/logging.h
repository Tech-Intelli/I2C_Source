/**
 * @file Log.h
 * @brief A singleton logger class for logging messages at various severity levels.
 *
 * This class provides a thread-safe singleton logger implementation using the spdlog library.
 * It allows logging messages with different severity levels, including trace, debug, info, warn, error, and critical.
 *
 * Usage:
 * 1. Initialize the logger by calling `Log::init()` with an optional logger name.
 * 2. Use the logging methods (e.g., `log.trace()`, `log.info()`, etc.) to log messages.
 *
 * Example:
 * @code
 * Log::init("MyLogger");
 * log.info("This is an info message: {}", some_variable);
 * log.error("An error occurred: {}", error_message);
 * @endcode
 *
 * @note The logger is initialized only once and will be reused throughout the application lifecycle.
 *
 * @throw None
 * @see spdlog documentation for more details on configuration and usage.
 */
#pragma once

#include <spdlog/spdlog.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <memory>
#include <string>

class Log
{
public:
    /**
     * Initializes the logger with the specified logger name.
     *
     * @param logger_name The name of the logger. Defaults to "logger".
     *
     * @return void
     *
     * @throws None
     */
    static void init(const std::string &logger_name = "logger")
    {
        // Create a console sink with color support
        auto console_sink = std::make_shared<spdlog::sinks::stdout_color_sink_mt>();
        console_sink->set_level(spdlog::level::trace);
        console_sink->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%s:%#] [%^%-5l%$] [T%t] %v");

        // Create a logger with the specified name
        auto logger = std::make_shared<spdlog::logger>(logger_name, console_sink);
        logger->set_level(spdlog::level::trace);

        // Set the default logger
        spdlog::set_default_logger(logger);
    }

    /**
     * Logs a trace message with the specified format and arguments.
     *
     * @param fmt The format string for the trace message.
     * @param args The arguments to be formatted.
     *
     * @throws None.
     */
    template <typename... Args>
    void trace(const char *fmt, const Args &...args)
    {
        spdlog::trace(fmt, args...);
    }

    /**
     * Logs a debug message with the specified format and arguments.
     *
     * @param fmt The format string for the debug message.
     * @param args The arguments to be formatted.
     *
     * @throws None.
     */
    template <typename... Args>
    void debug(const char *fmt, const Args &...args)
    {
        spdlog::debug(fmt, args...);
    }

    /**
     * Logs an informational message with the specified format and arguments.
     *
     * @param fmt The format string for the informational message.
     * @param args The arguments to be formatted.
     *
     * @throws None
     */
    template <typename... Args>
    void info(const char *fmt, const Args &...args)
    {
        spdlog::info(fmt, args...);
    }

    /**
     * Logs a warning message with the specified format and arguments.
     *
     * @param fmt The format string for the warning message.
     * @param args The arguments to be formatted.
     *
     * @throws None.
     */
    template <typename... Args>
    void warn(const char *fmt, const Args &...args)
    {
        spdlog::warn(fmt, args...);
    }

    /**
     * Logs an error message with the specified format and arguments.
     *
     * @param fmt The format string for the error message.
     * @param args The arguments to be formatted.
     *
     * @throws None.
     */
    template <typename... Args>
    void error(const char *fmt, const Args &...args)
    {
        spdlog::error(fmt, args...);
    }

    /**
     * Logs a critical message with the specified format and arguments.
     *
     * @param fmt The format string for the critical message.
     * @param args The arguments to be formatted.
     *
     * @return void
     *
     * @throws None
     */
    template <typename... Args>
    void critical(const char *fmt, const Args &...args)
    {
        spdlog::critical(fmt, args...);
    }

    // Macro for convenience
    static Log &getInstance()
    {
        static Log instance;
        return instance;
    }

private:
    Log() = default;
    Log(const Log &) = delete;
    Log &operator=(const Log &) = delete;
};

// Macro for convenience
#define log Log::getInstance()
