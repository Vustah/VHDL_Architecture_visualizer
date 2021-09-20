
class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.sensitivity_list = []
        self.internal_variables = {}
        self.assigned_signals = {}
        self.input_signal = []

    def set_sensitivity_signal(self, signal):
        self.sensitivity_list.append(signal)

    def get_sensitivity_signals(self):
        return self.sensitivity_list

    def set_internal_variable(self, variable, value=None, variable_type=None):
        if variable in self.internal_variables:
            if value != None:
                if not "value" in  self.internal_variables[variable]:
                    self.internal_variables[variable]["value"] = []
                if not value in self.internal_variables[variable]["value"]:
                    self.internal_variables[variable]["value"].append(value)
        else:
            self.internal_variables[variable] = {}

            if variable_type != None:
                self.internal_variables[variable]["type"] = variable_type
            if value != None:
                if not "value" in  self.internal_variables[variable]:
                    self.internal_variables[variable]["value"] = []
                self.internal_variables[variable]["value"].append(value)

    def get_internal_variables(self):
        return self.internal_variables

    def set_assigned_signal(self, signal, value):
        if signal in self.assigned_signals:
            if not value in self.assigned_signals[signal]:
                self.assigned_signals[signal].append(value)
        else:
            self.assigned_signals[signal] = [value]

    def get_assigned_signals(self):
        return self.assigned_signals

    def set_input_signals(self, signal):
      if signal not in self.input_signal:
        self.input_signal.append(signal)

    def get_input_signals(self):
      return self.input_signal


    def get_process_name(self):
        return self.process_name