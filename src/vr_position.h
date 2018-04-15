#ifndef VR_POSITION_H
#define VR_POSITION_H
#include "position.h"

// Forward-declare
namespace vr {
    struct IVRSystem;
}

/**
 * Gets a position from a VR device
 */
class VrPosition {
public:
    VrPosition();

    /** Returns the next available position of the HMD. This may block. */
    Position get_position();

    ~VrPosition();
private:
    /** The VR system */
    vr::IVRSystem* vr;
};

#endif
