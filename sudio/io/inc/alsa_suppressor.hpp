#pragma once

namespace suio {
    class AlsaErrorSuppressor {
    public:
        AlsaErrorSuppressor();
        ~AlsaErrorSuppressor();

    private:
        #ifdef __has_include
            #if __has_include(<alsa/asoundlib.h>)
                #define HAS_ALSA 1
                using error_handler_t = void(*)(const char*, int, const char*, int, const char*, ...);
                error_handler_t original_handler;
                
                static void silent_error_handler(const char* file, int line, const char* function, 
                                              int err, const char* fmt, ...) 
                                              __attribute__((format(printf, 5, 6)));
            #else
                #define HAS_ALSA 0
            #endif
        #else
            #define HAS_ALSA 0
        #endif
    };
}