#ifndef POZYX_POSITION_H
#define POZYX_POSITION_H
#include <cstdio>
#include "position.h"

/** Gets positions from Pozyx devices */
class PozyxPosition {
public:
    PozyxPosition(const char* print_positions_path);
    /** Returns the next available position of some Pozyx tag. This may block. */
    Position get_position();

    ~PozyxPosition();
private:
    /** Handle used to read from the child process */
    std::FILE* _child;
};

#endif
