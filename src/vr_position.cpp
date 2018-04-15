#include "vr_position.h"
#include <cassert>
#include <openvr.h>
#include <sstream>
#include <stdexcept>
#include <chrono>

VrPosition::VrPosition() {
    vr::HmdError error;
    this->vr = vr::VR_Init(&error, vr::EVRApplicationType::VRApplication_Overlay);
    if (error != vr::EVRInitError::VRInitError_None) {
        std::stringstream error_message;
        error_message << "Failed to initialize VR: " << vr::VR_GetVRInitErrorAsEnglishDescription(error);
        throw std::runtime_error(error_message.str().c_str());
    }
}

Position VrPosition::get_position() {
    assert(this->vr);
    vr::TrackedDevicePose_t pose;
    do {
        this->vr->GetDeviceToAbsoluteTrackingPose(
            vr::TrackingUniverseOrigin::TrackingUniverseStanding,
            0.0f,
            &pose,
            1);
    } while (!pose.bPoseIsValid);
    const auto time = std::chrono::high_resolution_clock::now();
    // Convert from matrix to position

    // Notes:
    // The VR coordinate system is similar to the screen coordinate system.
    // Looking toward the screen (in the direction of calibration):
    // +X is to the right
    // +Y is up
    // +Z is back (out of the screen)
    const auto x = pose.mDeviceToAbsoluteTracking.m[0][3];
    const auto y = pose.mDeviceToAbsoluteTracking.m[1][3];
    const auto z = pose.mDeviceToAbsoluteTracking.m[2][3];

    // Covert into the same coordinate system that the Pozyx tags use:
    // +X is back (out of the screen)
    // +Y is to the right
    // +Z is up
    const auto converted_x = z;
    const auto converted_y = x;
    const auto converted_z = y;

    return Position {
        "VR",
        converted_x,
        converted_y,
        converted_z,
        time
    };
}

VrPosition::~VrPosition() {
    vr::VR_Shutdown();
}
