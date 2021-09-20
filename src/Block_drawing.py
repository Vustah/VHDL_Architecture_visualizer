from N2G import drawio_diagram

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
  diagram = drawio_diagram()
  diagram.add_diagram(diagram_name)
  INPUT_BLOCK = blocks[0]
  OUTPUT_BLOCK = blocks[-1]
  diagram.add_node(id=INPUT_BLOCK.get_name())
  diagram.add_node(id=OUTPUT_BLOCK.get_name())
  internal_blocks = blocks[1:-1]
  for block in internal_blocks:
    diagram.add_node(id=block.get_name())

  for block in internal_blocks:
    for signal in block.get_input_signals():
      for jdx, another_block in enumerate(internal_blocks):
        if signal in another_block.get_output_signals():
          block1 = block.get_name()
          block2 = another_block.get_name()
          diagram.add_link(block1,block2,label=signal)
  
  for signal in INPUT_BLOCK.get_output_signals():
    for jdx, another_block in enumerate(internal_blocks):
      if signal in another_block.get_input_signals():
        block1 = INPUT_BLOCK.get_name()
        block2 = another_block.get_name()
        diagram.add_link(block1,block2,label=signal)

  
  for signal in OUTPUT_BLOCK.get_input_signals():
    for jdx, another_block in enumerate(internal_blocks):
      if signal in another_block.get_output_signals():
        block1 = OUTPUT_BLOCK.get_name()
        block2 = another_block.get_name()
        diagram.add_link(block1,block2,label=signal)


  diagram.dump_file(filename="DrawIO_diagram.drawio")
  return 0
    
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
