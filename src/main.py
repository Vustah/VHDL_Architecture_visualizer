import sys
import os
from tkinter import filedialog
from Entity import Entity
from Process import Process,Inline_process
from Procedure import Procedure
from Component import Component
from Block_drawing import Block, Wire, draw_diagram
import re

def find_path(filename):
    path_end = filename.rfind("/")
    path = filename[0:path_end]
    return path


def importfile(filename):
    if filename == None:
        filename = filedialog.askopenfilename()

    path = find_path(filename)

    infile = open(filename, 'r')

    infile_content = []
    for line in infile.readlines():
        infile_content.append(line)
    return infile_content, path

def sort_system(entity, processes):
  block_list = []

  entity_inputs = entity.get_input_signals()
  INPUT = Block("INPUT")
  for signal in entity_inputs:
    INPUT.set_output_signal(signal)

  block_list.append(INPUT)


  for process in processes:
    if not (isinstance(process, Process) or isinstance(process, Inline_process)):
      return 1
    tmp_block = Block(process.get_process_name())
    for signal in process.get_assigned_signals():
      value = process.get_assigned_signals()[signal]
      tmp_block.set_output_signal(signal)
      for spesific_value in value:
        tmp_block.set_input_signal(spesific_value)
    for signal in process.get_input_signals():
        tmp_block.set_input_signal(signal)
    if isinstance(process,Inline_process):
      buffer_type = process.get_buffer_type()
      tmp_block.set_block_type(buffer_type)

    block_list.append(tmp_block)


  entity_outputs = entity.get_output_signals()
  OUTPUT = Block("OUTPUT")
  for signal in entity_outputs:
    OUTPUT.set_input_signal(signal)

  block_list.append(OUTPUT)

  return block_list



def find_entity_with_signals(content):
    entity = None
    entity_name = ""
    entity_string = ""
    inside_entity_declaration = False

    for line in content:
        if "entity" in line:
            entity_name = line.split(" ")[1]
            entity = Entity(entity_name)
            inside_entity_declaration = True
            
        if inside_entity_declaration:
            entity_string+= line

        if ("end " + entity_name) in line:
            inside_entity_declaration = False
            break
    
    input_compiled = re.compile(r"(?P<input>\w+)\s*:\s*in\s(?P<type>\w+)") 
    output_compiled = re.compile(r"(?P<output>\w+)\s*:\s*out\s(?P<type>\w+)") 

    input_signals = re.finditer(input_compiled,entity_string)
    output_signals = re.finditer(output_compiled,entity_string)

    for signal in input_signals:
        input_signal_name,input_signal_type = signal.group("input","type")
        entity.set_input_signals(input_signal_name=input_signal_name,input_signal_type=input_signal_type)
    for signal in output_signals:
        output_signal_name,output_signal_type = signal.group("output","type")
        entity.set_output_signals(output_signal_name=output_signal_name, output_signal_type=output_signal_type)
    
    return entity

def find_internal_signals(content,entity = None):
    if entity == None:
        entity = find_entity_with_signals(content)
    
    architecture_string = "" 
    inside_architecture = False
    for line in content:
        if "architecture" in line:
            inside_architecture = True
        if inside_architecture:
            architecture_string += line
        if "end architecture" in line:
            break
            
    signal_pattern = re.compile(r"\s*signal\s+(?P<signal_name>\w+)\s+:\s+(?P<signal_type>\w+)")
    signal_declaration = re.finditer(signal_pattern,architecture_string)
    for signal in signal_declaration:
        signal_name,signal_type = signal.group("signal_name","signal_type")
        entity.set_internal_signals(internal_signal_name=signal_name, internal_signal_type=signal_type)
    return entity

def find_sensitivity_signals(process_line):
    starting_bracket = process_line.index("(")
    ending_bracket = process_line.index(")")
    signals = process_line[starting_bracket + 1:ending_bracket].replace(
        " ", "").split(",")
    return signals


def find_processes(content):
    list_of_prosesses = []
    list_of_inline_processes = []
    current_process = None
    process_started = False
    inside_procedure = False
    procedure_started = False
    p_idx = 0
    for line in content:

        if current_process == None:
            process_started = False

        
        if " process " in line and "end" not in line:
            try:
                end_process_name = line.index(":")
                process_name = line[0:end_process_name].replace(" ", "").replace("\t", "")
            except ValueError:
                process_name = "Process_"+str(p_idx)
                p_idx+=1
            
            current_process = Process(process_name)
            sensitivity_signals = find_sensitivity_signals(line)
            for signal in sensitivity_signals:
                current_process.set_sensitivity_signal(signal)

        # Procedure detection
        if " procedure " in line:
            inside_procedure = True
        if " end procedure" in line:
            inside_procedure = False
            procedure_started = False

        if "begin" in line:
            if inside_procedure:
                procedure_started = True
            else:
                process_started = True

        if " if " in line and process_started == True:
          if_start = line.find("if")
          line_splitted = line[if_start:].split(" ")
          multiple_lines = []
          if "and" in line_splitted or "or" in line_splitted:
            split_idx = []
            for idx,item in enumerate(line_splitted):
              if item == "and" or item == "or":
                split_idx.append(idx)


            last_idx = 0
            for idx in split_idx:

              multiple_lines.append(line_splitted[last_idx+1:idx])
              last_idx = idx
            multiple_lines.append(line_splitted[last_idx+1:])

          else:
            multiple_lines.append(line_splitted)

          for multiple_line_splitted in multiple_lines:
            if "=" in multiple_line_splitted:
              equal_idx = multiple_line_splitted.index("=")
              first_signal = multiple_line_splitted[equal_idx-1].replace("(","")
              second_signal = multiple_line_splitted[equal_idx+1].replace(")","")
              current_process.set_input_signals(first_signal)
              current_process.set_input_signals(second_signal)

          if "rising_edge" in line:
            bracket_start = line.find("(")+1
            bracket_end = line.find(")")
            signal = line[bracket_start:bracket_end]
            current_process.set_input_signals(signal)

        if " variable " in line and current_process != None:
            variable_declaration = line.split(": ")
            variable_name = variable_declaration[0].split(" variable ")[1].replace(" ", "")
            variable_type = variable_declaration[1].split(":=")
            variable_value = None

            if len(variable_type) > 1:
                variable_value = variable_type[1].replace(" ", "")

            current_process.set_internal_variable(variable_name, value=variable_value, variable_type=variable_type[0].replace("; ", ""))

        if " := " in line and process_started == True:
            target_variable = line.split(":=")[0].replace("\t","").replace(" ", "")
            target_value = line.split(":=")[1].replace("\n", "").replace(";","").replace(" ", "")
            current_process.set_internal_variable(target_variable, value=target_value)

        if " <= " in line:
          if process_started  or procedure_started:
            target_signal = line.split("<=")[0].replace("\t","").replace(" ", "")
            value = line.split("<=")[1].replace("\n", "").replace(";","").replace(" ", "")
            
            current_process.set_assigned_signal(target_signal, value)
          elif not inside_procedure:
            list_of_inline_processes.append(define_inline_process(line))

        if "end process" in line:
            list_of_prosesses.append(current_process)
            current_process = None

    list_of_prosesses = list_of_prosesses+list_of_inline_processes
    return list_of_prosesses

def pop_elements_from_list(list_to_pop, item_to_pop):
  popped_list = []
  for idx,item in enumerate(list_to_pop):
    if item != item_to_pop:
      popped_list.append(item)
    
  return popped_list

def define_inline_process(line):
  target_signal = line.split("<=")[0].replace("\t","").replace(" ", "")
  value_list = line.split("<=")[1].replace("\n", "").replace(";","").split(" ")
  
  value_list = pop_elements_from_list(value_list,'')
  
  buffer_type = "buffer"
  value = None
  second_value = None
  trigger_signal = None
  
  
  if len(value_list)<4:
    if "not" in value_list:
      buffer_type = "not"
    value = value_list[-1]
  else:
    if "when" in value_list:
      value = value_list[0]
      second_value = value_list[-1]
      trigger_signal = value_list[2]


  inline_process = Inline_process(target_signal)  
  inline_process.set_buffer_type(gate_type=buffer_type)
  if value != None:
    inline_process.set_assigned_signal(target_signal,value)
  if second_value != None:
    inline_process.set_assigned_signal(target_signal,second_value,)
  if trigger_signal != None:
    inline_process.set_assigned_signal(target_signal,trigger_signal)


  return inline_process

def remove_comments(content):
    cleaned_content = []
    for line in content:
        line = line.replace("(", "\(").replace(")", "\)").replace("\n","")
        if re.match("^\s*--",line) == None:
            cleaned_content.append(line)
    
    return cleaned_content


def print_all(entity,processes):
    print(entity.get_name())

    print("Input")
    for signal in entity.get_input_signals():
        print(" ", signal,": ", entity.get_input_signals()[signal])

    print("Output")
    for signal in entity.get_output_signals():
        print(" ", signal,": ", entity.get_output_signals()[signal])

    print("Internal Signal")
    for signal in entity.get_internal_signals():
        signal_type = entity.get_internal_signals()[signal]["type"]
        if entity.get_internal_signals()[signal]["value"]:
            value = entity.get_internal_signals()[signal]["value"]
        else:
             value = None

        print(" ", signal,": ", signal_type, end="")
        if value!= None:
            print(" := ", value)
        else:
            print("")

    for process in processes:
        print("\n", process.get_process_name())

        print("   Sensitivity list:  ")
        for sens_signal in process.get_sensitivity_signals():
            print("    ", sens_signal)

        if len(process.get_internal_variables()) > 0:
            print("   Internal Variables:")
            for internal_variable in process.get_internal_variables():
                print("    ", internal_variable, ":", process.get_internal_variables()[internal_variable])

        print("   Assigned Signals:  ")
        for assigned_signal in process.get_assigned_signals():
            print("    ", assigned_signal, ":", process.get_assigned_signals()[assigned_signal])


def main(filename):

    try:
        file_content, path = importfile(filename)
    except:
        return 1

    file_content = remove_comments(file_content)

    entity = find_entity_with_signals(file_content)
    entity = find_internal_signals(file_content,entity)
    processes = find_processes(file_content)
    #print_all(entity,processes)
    block_list = sort_system(entity,processes)
    if block_list != 1:
      draw_diagram(entity.get_name(),block_list,None)
    else:
      return 1
    return 0


if __name__ == "__main__":
    print("Start program")
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None
    exit(main(filename))
