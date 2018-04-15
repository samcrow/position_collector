#ifndef RATE_PRINTER_H
#define RATE_PRINTER_H
#include <thread>
#include <atomic>

/**
 * Prints rates of events
 */
class RatePrinter {
public:
    /** Creates a rate printer and starts the printer thread */
    RatePrinter(const std::string& event_name);
    /** Records an event */
    void record_event();

    ~RatePrinter();
private:
    /**
     * The name of events
     */
    const std::string name;
    /**
     * The flag that indicates that the printer thread should keep running
     */
    std::atomic_bool running;
    /**
     * The number of events that have happened in the last second
     */
    std::atomic_uint event_count;
    /**
     * The printer thread
     */
    std::thread printer_thread;
    /** Prints rates (run in a separate thread) */
    void rate_printer_thread();
};

#endif
