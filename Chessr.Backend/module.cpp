#include <pybind11/pybind11.h>

namespace py = pybind11;

class SomeClass {
    float multiplier;
public:
    SomeClass(float multiplier_) : multiplier(multiplier_) {};

    float multiply(float input) {
        return multiplier * input;
    }

    std::vector<float> multiply_list(std::vector<float> items) {
        for (auto i = 0; i < items.size(); i++) {
            items[i] = multiply(items.at(i));
        }
        return items;
    }

    void set_mult(float val) {
        multiplier = val;
    }

    float get_mult() {
        return multiplier;
    }
};

PYBIND11_MODULE(backend, m) {
    py::class_<SomeClass>(m, "SomeClass").def(py::init<float>())
        .def_property("multiplier", &SomeClass::get_mult, &SomeClass::set_mult)
        .def("multiply", &SomeClass::multiply)
        .def("multiply_list", &SomeClass::multiply_list);
}
