from diagrams import Cluster, Diagram
from diagrams.programming.flowchart import Action

class Block:
  def __init__(self, name):
    self.set_name(name)
    self.input_signals = []
    self.output_signals = []
  
  def set_input_signal(self, signal):
    self.input_signals.append(signal)
    
  def get_input_signals(self):
    return self.input_signals
        
  def set_output_signal(self, signal):
    self.output_signals.append(signal)

  def get_output_signals(self):
    return self.output_signals

  def set_name(self, name):
    self.name = name
  
  def get_name(self):
    return self.name
    
    
class Wire:
  def __init__(self, name, width):
    self.name = name
    self.width = width
    
  def get_name(self):
    return self.name
  
  def get_width(self):
    return self.width
  
  
def draw_diagram(diagram_name, blocks, wires):
  with Diagram(diagram_name):
    block_list = []
    for block in blocks:
      if not isinstance(block,Block):
        break
      block_list.append(Action(block.get_name()))
    
    for idx, block in enumerate(blocks): 
      if not isinstance(block,Block):
        break
      for signal in block.get_input_signals():
        for jdx, another_block in enumerate(blocks):
          if signal in another_block.get_output_signals():
            block_list[jdx] >> block_list[idx]
        

    
def main():
  block1 = Block("foo")
  block2 = Block("bar")
  block3 = Block("init")
  block1.set_output_signal("RST")
  block1.set_output_signal("clk")
  block1.set_output_signal("enable")
  block2.set_input_signal("enable")
  block2.set_input_signal("RST")
  block3.set_input_signal("enable")
  block3.set_input_signal("clk")
  draw_diagram("FOOBAR", [block1,block2,block3],None)
 
if __name__ == "__main__":
   main()
