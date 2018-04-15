#include "rate_printer.h"
#include <functional>
#include <chrono>
#include <iostream>
#include <sstream>

RatePrinter::RatePrinter(const std::string& event_name) :
    name(event_name),
    running(true),
    event_count(0),
    printer_thread(std::bind(&RatePrinter::rate_printer_thread, this))
{
}

void RatePrinter::record_event() {
    event_count += 1;
}

void RatePrinter::rate_printer_thread() {
    auto previous_time = std::chrono::high_resolution_clock::now();
    while (running) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        const auto current_time = std::chrono::high_resolution_clock::now();
        const auto dt = std::chrono::nanoseconds(current_time - previous_time);
        const double seconds = double(dt.count()) * 1e-9;

        const auto events = event_count.exchange(0);
        const auto rate = double(events) / seconds;

        // Format everything as a string first to prevent output interleaving
        std::stringstream stream;
        stream << name << ": " << rate << " events/second\n";
        std::cerr << stream.str();

        previous_time = current_time;
    }
}

RatePrinter::~RatePrinter() {
    running = false;
    printer_thread.join();
}
