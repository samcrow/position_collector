#include "pozyx_position.h"
#include <system_error>
#include <array>
#include <chrono>
#include <iostream>

namespace {
/**
 * Throws an std::system_error with an error code taken from errno and a
 * provided message
 */
void throw_errno(const std::string& message) {
    const auto code = std::error_code(errno, std::system_category());
    throw std::system_error(code, message);
}
}

PozyxPosition::PozyxPosition(const char* print_positions_path) {
    _child = ::popen(print_positions_path, "r");
    if (!_child) {
        throw_errno("failed to start Python subprocess");
    }
}

Position PozyxPosition::get_position() {
    std::array<char, 33> source;
    Position position;
    while (true) {
        const auto read = std::fscanf(_child, "%32[^,],%lf,%lf,%lf\n", source.data(), &position.x, &position.y, &position.z);
        if (read == EOF) {
            throw std::runtime_error("EOF reading from Python subprocess");
        }
        if (read == 4) {
            // Success
            break;
        } else {
            std::cerr << "Failed to read from child process, read only " << read << " things\n";
        }
    }
    position.time = std::chrono::high_resolution_clock::now();
    position.source = std::string(source.data());
    return position;
}

PozyxPosition::~PozyxPosition() {
    ::pclose(_child);
}
