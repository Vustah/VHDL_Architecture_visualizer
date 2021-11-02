from N2G import drawio_diagram

class Block:
  def __init__(self, name):
    self.set_name(name)
    self.input_signals = []
    self.output_signals = []
    self.block_type = "rounded_rectangle"

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

  def set_block_type(self, block_type):
    self.block_type = block_type
  
  def get_block_type(self):
    return self.block_type
    
class Wire:
  def __init__(self, name, width, bit_width = 1):
    self.name = name
    self.width = width
    self.bit_width = bit_width

  def get_name(self):
    return self.name
  
  def get_width(self):
    return self.width
  


def draw_diagram(diagram_name, blocks, wires):
  diagram = drawio_diagram()
  diagram.add_diagram(diagram_name)
  INPUT_BLOCK = blocks[0]
  OUTPUT_BLOCK = blocks[-1]
  
  internal_blocks = blocks[1:-1]

  diagram = place_nodes(diagram, blocks)

  for block in internal_blocks:
    for signal in block.get_input_signals():
      for jdx, another_block in enumerate( internal_blocks):
        diagram = draw_wire(diagram,block,another_block,signal)
  
  for block in internal_blocks:
    for signal in block.get_input_signals():
        diagram = draw_wire(diagram,block,INPUT_BLOCK,signal)
  
  for signal in OUTPUT_BLOCK.get_input_signals():
    for jdx, another_block in enumerate(internal_blocks):
      diagram = draw_wire(diagram,OUTPUT_BLOCK,another_block,signal)

  # diagram.layout(algo="fr")
  diagram.dump_file(filename="DrawIO_diagram.drawio")
  return 0

def place_nodes(diagram,list_of_nodes):
  x_pos = 0
  y_pos = 0
  inverter_style = "shape=mxgraph.electrical.logic_gates.inverter_2;align=left;spacingLeft=25;"
  buffer_style = "shape=mxgraph.electrical.logic_gates.buffer2;align=left;spacingLeft=25;"
  normal_style = "rounded=1"
  number_of_nodes = 0
  node_height = 100
  for idx,node in enumerate(list_of_nodes):
    if node.get_name() == "INPUT" or node.get_name() == "OUTPUT":
      y_pos = 0
    else:
      number_of_nodes += 1



    if node.get_block_type() == "not":
      diagram.add_node(id=node.get_name(), x_pos=x_pos, y_pos=y_pos,  style = inverter_style, height = node_height)
    elif node.get_block_type() == "buffer":
      diagram.add_node(id=node.get_name(), x_pos=x_pos, y_pos=y_pos,  style = buffer_style, height = node_height)
    else:
      diagram.add_node(id=node.get_name(), x_pos=x_pos, y_pos=y_pos,  style = normal_style, height = node_height)

    if idx == 0 or idx == len(list_of_nodes)-2:
      x_pos += 200
    else:
      x_pos += 200
      y_pos += 150
      
  
  diagram.update_node(id="INPUT",height = number_of_nodes*150)
  diagram.update_node(id="OUTPUT",height = number_of_nodes*150)  

  return diagram
  
def draw_wire(diagram,input_block,output_block, signal_name):
  arrow_style = "endArrow=classic;endFill=1;edgeStyle=orthogonalEdgeStyle;jumpStyle=arc;strokeWidth=2;"
  red_color = "fillColor=#f8cecc;strokeColor=#b85450;"
  blue_color = "fillColor=#dae8fc;strokeColor=#6c8ebf;"
  if signal_name in output_block.get_output_signals():
    output_block_name = output_block.get_name()
    input_block_name = input_block.get_name()
    if input_block_name != output_block_name:
      if "rst" in  signal_name :
        arrow_style = arrow_style+red_color
      if "clk" in signal_name:
        arrow_style = arrow_style+blue_color
      diagram.add_link(source=output_block_name,target=input_block_name,label=signal_name, style=arrow_style)
  
      #print(output_block_name,signal_name,input_block_name)
  
  return diagram

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
