/*
 * SUDIO - Audio Processing Platform
 * Copyright (C) 2024 Hossein Zahaki
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 *
 * - GitHub: https://github.com/MrZahaki/sudio
 */
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include "rateshift.hpp"

namespace py = pybind11;

PYBIND11_MODULE(_rateshift, m) {

    py::enum_<rateshift::ConverterType>(m, "ConverterType")
        .value("sinc_best", rateshift::ConverterType::sinc_best)
        .value("sinc_medium", rateshift::ConverterType::sinc_medium)
        .value("sinc_fastest", rateshift::ConverterType::sinc_fastest)
        .value("zero_order_hold", rateshift::ConverterType::zero_order_hold)
        .value("linear", rateshift::ConverterType::linear)
        .export_values();

    py::class_<rateshift::Resampler>(m, "Resampler")
        .def(py::init<rateshift::ConverterType, int>(), 
             py::arg("converter_type"), py::arg("channels") = 1
             )
        .def("process", [](rateshift::Resampler& self, py::array_t<float> input, double sr_ratio, bool end_of_input = false) {
            py::buffer_info buf = input.request();
            std::vector<float> input_vec(static_cast<float*>(buf.ptr), static_cast<float*>(buf.ptr) + buf.size);
            std::vector<float> output = self.process(input_vec, sr_ratio, end_of_input);
            return py::array_t<float>(output.size(), output.data());
        }, py::arg("input"), py::arg("sr_ratio"), py::arg("end_of_input") = false
        )
        .def("set_ratio", &rateshift::Resampler::set_ratio, py::arg("ratio"),
             "Set a new resampling ratio.")
        .def("reset", &rateshift::Resampler::reset,
             "Reset the internal state of the resampler.");

    py::class_<rateshift::CallbackResampler>(m, "CallbackResampler")
        .def(py::init<rateshift::CallbackResampler::callback_t, double, rateshift::ConverterType, size_t>(),
             py::arg("callback"), py::arg("ratio"), py::arg("converter_type"), py::arg("channels")
             )
        .def("read", [](rateshift::CallbackResampler& self, size_t frames) {
            std::vector<float> output = self.read(frames);
            return py::array_t<float>(output.size(), output.data());
        }, py::arg("frames"))
        .def("set_starting_ratio", &rateshift::CallbackResampler::set_starting_ratio, py::arg("ratio"),
             "Set a new starting ratio for the resampler.")
        .def("reset", &rateshift::CallbackResampler::reset,
             "Reset the internal state of the resampler.");

    m.def("resample", [](py::array_t<float> input, double sr_ratio, rateshift::ConverterType converter_type, int channels = 1) {
        py::buffer_info buf = input.request();
        std::vector<float> input_vec(static_cast<float*>(buf.ptr), static_cast<float*>(buf.ptr) + buf.size);
        std::vector<float> output = rateshift::resample(input_vec, sr_ratio, converter_type, channels);
        return py::array_t<float>(output.size(), output.data());
    }, py::arg("input"), py::arg("sr_ratio"), py::arg("converter_type"), py::arg("channels") = 1
    );
}