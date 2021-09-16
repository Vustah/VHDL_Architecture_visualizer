class Entity:
  def __init__(self, name):
    self.name = name
    self.input_signals = {}
    self.output_signals = {}
    self.internal_signals = {}
    
  def set_input_signals(self, input_signal_name, input_signal_type):
    self.input_signals[input_signal_name] = input_signal_type
  
  def get_input_signals(self):
    return self.input_signals

  def set_output_signals(self, output_signal_name, output_signal_type):
    self.output_signals[output_signal_name] = output_signal_type
  
  def get_output_signals(self):
    return self.output_signals

  def set_internal_signals(self, internal_signal_name, internal_signal_type,internal_signal_value = None ):

    self.internal_signals[internal_signal_name] = {}
    self.internal_signals[internal_signal_name]["type"] = internal_signal_type
    if internal_signal_value == None:
      self.internal_signals[internal_signal_name]["value"] = 0
    else:
      self.internal_signals[internal_signal_name]["value"] = internal_signal_value
    

  def get_internal_signals(self):
    return self.internal_signals

  def get_name(self):
    return self.name