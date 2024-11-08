#include "alsa_suppressor.hpp"

#if HAS_ALSA
    #include <alsa/asoundlib.h>
#endif

namespace suio {

#if HAS_ALSA

AlsaErrorSuppressor::AlsaErrorSuppressor() {
    original_handler = (error_handler_t)snd_lib_error_set_handler((snd_lib_error_handler_t)silent_error_handler);
}

AlsaErrorSuppressor::~AlsaErrorSuppressor() {
    snd_lib_error_set_handler((snd_lib_error_handler_t)original_handler);
}

void AlsaErrorSuppressor::silent_error_handler(const char* file, int line, 
                                             const char* function, int err, 
                                             const char* fmt, ...) {
}

#else // Non-Linux systems or no ALSA

AlsaErrorSuppressor::AlsaErrorSuppressor() {
}

AlsaErrorSuppressor::~AlsaErrorSuppressor() {
}

#endif

} // namespace suio