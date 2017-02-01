from django.forms import TextInput

class RangeInput(TextInput):
    min = 0
    max = 100

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if attrs is not None:
            _min = attrs.pop('min', self.min)
            _max = attrs.pop('max', self.max)
        if "min" not in self.attrs:
            self.attrs["min"] = _min
        if "min" not in self.attrs:
            self.attrs["min"] = _min
    input_type = 'range'
