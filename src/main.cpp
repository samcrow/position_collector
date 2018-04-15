
#include <iostream>
#include <thread>
#include <mutex>
#include <unordered_map>
#include <functional>

#include "position.h"
#include "vr_position.h"
#include "pozyx_position.h"
#include "rate_printer.h"

using std::chrono::high_resolution_clock;
typedef high_resolution_clock::time_point time_point;

namespace {

/** Mutex for controlling access to stdout for printing */
std::mutex stdout_mutex;

void print_headers() {
    std::cout << "Source,X,Y,Z,Nanoseconds\n";
}

void print_position(const Position& position, time_point start) {
    const auto since_start = position.time - start;
    std::lock_guard<std::mutex> lock(stdout_mutex);
    std::cout << position.source << ',' << position.x
        << ',' << position.y << ',' << position.z
        << ',' << std::chrono::nanoseconds(since_start).count() << '\n';
}

void run_vr_thread(time_point start) {
    try {
        VrPosition vr;

        while (true) {
            const auto position = vr.get_position();
            print_position(position, start);
        }
    } catch (std::exception& e) {
        std::cerr << "VR failed: " << e.what() << '\n';
    }
}

void run_pozyx_thread(const char* print_positions_path, time_point start) {
    PozyxPosition pozyx(print_positions_path);
    std::unordered_map<std::string, RatePrinter> rate_printers;

    while (true) {
        const auto position = pozyx.get_position();
        // Create rate printer if none exists
        if (rate_printers.find(position.source) == rate_printers.end()) {
            rate_printers.emplace(position.source, position.source);
        }
        rate_printers.at(position.source).record_event();
        print_position(position, start);
    }
}

}

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "Usage: " << argv[0] << " print_positions.py\n";
        return -1;
    }
    const char* print_positions_path = argv[1];

    print_headers();
    const auto start_time = high_resolution_clock::now();
    std::thread vr_thread(std::bind(run_vr_thread, start_time));
    run_pozyx_thread(print_positions_path, start_time);
    return 0;
}
