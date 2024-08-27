/*
 -- W.T.A
 -- SUDIO (https://github.com/MrZahaki/sudio)
 -- The Audio Processing Platform
 -- Mail: mrzahaki@gmail.com
 -- Software license: "Apache License 2.0". 
*/
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "rateshift.hpp"

namespace py = pybind11;

PYBIND11_MODULE(rateshift, m) {
    m.doc() = R"pbdoc(
        Python bindings for libsamplerate

        This module provides a Python interface to the libsamplerate library,
        allowing for high-quality audio resampling.

        Main Classes:
            Resampler: For resampling audio data.
            CallbackResampler: For resampling audio data using a callback function.

        Main Functions:
            resample: A convenience function for simple resampling tasks.
    )pbdoc";

    py::enum_<rateshift::ConverterType>(m, "ConverterType")
        .value("sinc_best", rateshift::ConverterType::sinc_best)
        .value("sinc_medium", rateshift::ConverterType::sinc_medium)
        .value("sinc_fastest", rateshift::ConverterType::sinc_fastest)
        .value("zero_order_hold", rateshift::ConverterType::zero_order_hold)
        .value("linear", rateshift::ConverterType::linear)
        .export_values();

    py::class_<rateshift::Resampler>(m, "Resampler")
        .def(py::init<rateshift::ConverterType, int>(), 
             py::arg("converter_type"), py::arg("channels") = 1,
             R"pbdoc(
             Initialize a Resampler object.

             Args:
                 converter_type (ConverterType): The type of converter to use.
                 channels (int, optional): Number of channels in the audio. Defaults to 1.
             )pbdoc")
        .def("process", [](rateshift::Resampler& self, py::array_t<float> input, double sr_ratio, bool end_of_input = false) {
            py::buffer_info buf = input.request();
            std::vector<float> input_vec(static_cast<float*>(buf.ptr), static_cast<float*>(buf.ptr) + buf.size);
            std::vector<float> output = self.process(input_vec, sr_ratio, end_of_input);
            return py::array_t<float>(output.size(), output.data());
        }, py::arg("input"), py::arg("sr_ratio"), py::arg("end_of_input") = false,
        R"pbdoc(
        Process audio data through the resampler.

        Args:
            input (numpy.ndarray): Input audio data as a NumPy array.
            sr_ratio (float): The ratio of output sample rate to input sample rate.
            end_of_input (bool, optional): Flag indicating if this is the last batch. Defaults to False.

        Returns:
            numpy.ndarray: Resampled audio data.
        )pbdoc")
        .def("set_ratio", &rateshift::Resampler::set_ratio, py::arg("ratio"),
             "Set a new resampling ratio.")
        .def("reset", &rateshift::Resampler::reset,
             "Reset the internal state of the resampler.");

    py::class_<rateshift::CallbackResampler>(m, "CallbackResampler")
        .def(py::init<rateshift::CallbackResampler::callback_t, double, rateshift::ConverterType, size_t>(),
             py::arg("callback"), py::arg("ratio"), py::arg("converter_type"), py::arg("channels"),
             R"pbdoc(
             Initialize a CallbackResampler object.

             Args:
                 callback (callable): A function that provides input audio data.
                 ratio (float): The initial resampling ratio.
                 converter_type (ConverterType): The type of converter to use.
                 channels (int): Number of channels in the audio.
             )pbdoc")
        .def("read", [](rateshift::CallbackResampler& self, size_t frames) {
            std::vector<float> output = self.read(frames);
            return py::array_t<float>(output.size(), output.data());
        }, py::arg("frames"),
        R"pbdoc(
        Read resampled audio data.

        Args:
            frames (int): Number of frames to read.

        Returns:
            numpy.ndarray: Resampled audio data.
        )pbdoc")
        .def("set_starting_ratio", &rateshift::CallbackResampler::set_starting_ratio, py::arg("ratio"),
             "Set a new starting ratio for the resampler.")
        .def("reset", &rateshift::CallbackResampler::reset,
             "Reset the internal state of the resampler.");

    m.def("resample", [](py::array_t<float> input, double sr_ratio, rateshift::ConverterType converter_type, int channels = 1) {
        py::buffer_info buf = input.request();
        std::vector<float> input_vec(static_cast<float*>(buf.ptr), static_cast<float*>(buf.ptr) + buf.size);
        std::vector<float> output = rateshift::resample(input_vec, sr_ratio, converter_type, channels);
        return py::array_t<float>(output.size(), output.data());
    }, py::arg("input"), py::arg("sr_ratio"), py::arg("converter_type"), py::arg("channels") = 1,
    R"pbdoc(
    Resample audio data.

    This is a convenience function for simple resampling tasks.

    Args:
        input (numpy.ndarray): Input audio data as a NumPy array.
        sr_ratio (float): The ratio of output sample rate to input sample rate.
        converter_type (ConverterType): The type of converter to use.
        channels (int, optional): Number of channels in the audio. Defaults to 1.

    Returns:
        numpy.ndarray: Resampled audio data.
    )pbdoc");
}