import sys
import os
from tkinter import filedialog
from Entity import Entity
from Process import Process
from Procedure import Procedure
from Component import Component


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


def find_entity_with_signals(content):
    entity = None
    entity_name = ""    
    inside_entity_declaration = False

    for line in content:
        line = line.replace(";", "").replace("\t", "  ").replace("\n", "")
        if "entity" in line:
            entity_name = line.split(" ")[1]
            entity = Entity(entity_name)            
            inside_entity_declaration = True
            # entity["name"] = entity_name
            # entity["IN"] = {}
            # entity["OUT"] = {}

        if " in " in line and inside_entity_declaration:
            line = line.replace("port(", "")
            signal_name = line.split(" in ")[0].replace(":", "").replace(" ", "")
            signal_type = line.split(" in ")[1].replace(":", "")
            entity.set_input_signals(input_signal_name=signal_name,input_signal_type=signal_type)
            # entity["IN"][signal_name] = signal_type

        if " out " in line and inside_entity_declaration:
            line = line.replace("port(", "")
            signal_name = line.split(" out ")[0].replace(":", "").replace(" ", "")
            signal_type = line.split(" out ")[1].replace(":", "")
            entity.set_output_signals(output_signal_name=signal_name,output_signal_type=signal_type)
            # entity["OUT"][signal_name] = signal_type

        if ("end " + entity_name) in line:
            inside_entity_declaration = False

    return entity

def find_internal_signals(content,entity = None):
    if entity == None:
        entity = find_entity_with_signals(content)
    for line in content:
        if "signal " in line:
            signal_declaration = line.split(": ")
            signal_name = signal_declaration[0].split("signal ")[1].replace(" ","")
            signal_type = signal_declaration[1].split(":=")
            signal_value = None
            if len(signal_type) > 1:
                signal_value = signal_type[1].replace(" ","")
            entity.set_internal_signals(signal_name, signal_type[0].replace("; ", ""), signal_value)
    return entity

def find_sensitivity_signals(process_line):
    starting_bracket = process_line.index("(")
    ending_bracket = process_line.index(")")
    signals = process_line[starting_bracket + 1:ending_bracket].replace(
        " ", "").split(",")
    return signals


def find_processes(content):
    list_of_prosesses = []
    current_process = None
    process_started = False
    inside_procedure = False
    procedure_started = False
    for line in content:

        if current_process == None:
            process_started = False

        if "process" in line and "end" not in line:
            end_process_name = line.index(":")
            process_name = line[0:end_process_name].replace(" ", "").replace("\t", "")
            current_process = Process(process_name)
            sensitivity_signals = find_sensitivity_signals(line)
            for signal in sensitivity_signals:
                current_process.set_sensitivity_signal(signal)
        
        # Procedure detection
        if "procedure" in line:
            inside_procedure = True
        if "end procedure" in line:
            inside_procedure = False
            procedure_started = False

        if "begin" in line:
            if inside_procedure:
                procedure_started = True
            else:
                process_started = True

        if "variable" in line and current_process != None:
            variable_declaration = line.split(": ")
            variable_name = variable_declaration[0].split("variable")[1].replace(" ", "")
            variable_type = variable_declaration[1].split(":=")
            variable_value = None

            if len(variable_type) > 1:
                variable_value = variable_type[1].replace(" ", "")

            current_process.set_internal_variable(variable_name, value=variable_value, variable_type=variable_type[0].replace("; ", ""))

        if ":=" in line and process_started == True:
            target_variable = line.split(":=")[0].replace("\t","").replace(" ", "")
            target_value = line.split(":=")[1].replace("\n", "").replace(";","").replace(" ", "") 
            current_process.set_internal_variable(target_variable, value=target_value)

        if "<=" in line and process_started == True:
            target_signal = line.split("<=")[0].replace("\t","").replace(" ", "")
            value = line.split("<=")[1].replace("\n", "").replace(";","").replace(" ", "")
            current_process.set_assigned_signal(target_signal, value)

        if "end process" in line:
            list_of_prosesses.append(current_process)
            current_process = None

    return list_of_prosesses


def remove_comments(content):
    no_comment_content = []
    for line in content:
        comment_line_idx = line.find("--")
        line = line[0:comment_line_idx]
        no_comment_content.append(line)
    return no_comment_content

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
    print_all(entity,processes)
    return 0


if __name__ == "__main__":
    print("Start program")
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None
    exit(main(filename))
