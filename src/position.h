#ifndef POSITION_H
#define POSITION_H
#include <string>
#include <chrono>

/** The position of something */
struct Position {
    /** The source of this position measurement */
    std::string source;
    /** X coordinate, meters */
    double x;
    /** Y coordinate, meters */
    double y;
    /** Z coordinate, meters */
    double z;
    /** The time when this position was measured */
    std::chrono::time_point<std::chrono::high_resolution_clock> time;
};

#endif
