import sys
import os
from tkinter import filedialog


class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.sensitivity_list = []
        self.internal_variables = {}
        self.assigned_signals = {}

    def set_sensitivity_signal(self, signal):
        self.sensitivity_list.append(signal)

    def get_sensitivity_signals(self):
        return self.sensitivity_list

    def set_internal_variable(self, variable, value=None, variable_type=None):
        if variable in self.internal_variables:
            if value != None:
                self.internal_variables[variable]["value"].append(value)
        else:
            self.internal_variables[variable] = {}

            if variable_type != None:
                self.internal_variables[variable]["type"] = variable_type
            if value != None:
                self.internal_variables[variable]["value"].append(value)

    def get_internal_variables(self):
        return self.internal_variables

    def set_assigned_signal(self, signal, value):
        if signal in self.assigned_signals:
            self.assigned_signals[signal].append(value)
        else:
            self.assigned_signals[signal] = [value]

    def get_assigned_signals(self):
        return self.assigned_signals

    def get_process_name(self):
        return self.process_name


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
    entity = {}
    entity_name = ""
    for line in content:
        line = line.replace(";", "").replace("\t", "  ").replace("\n", "")
        if "entity" in line:
            entity_name = line.split(" ")[1]
            entity["name"] = entity_name
            entity["IN"] = {}
            entity["OUT"] = {}

        if " in " in line:
            line = line.replace("port(", "")
            # print(line)
            # print(line.split(" in "))
            signal_name = line.split(" in ")[0].replace(":",
                                                        "").replace(" ", "")
            signal_type = line.split(" in ")[1].replace(":", "")

            entity["IN"][signal_name] = signal_type

        if " out " in line:
            line = line.replace("port(", "")
            signal_name = line.split(" out ")[0].replace(":",
                                                         "").replace(" ", "")
            signal_type = line.split(" out ")[1].replace(":", "")
            entity["OUT"][signal_name] = signal_type

        if ("end " + entity_name) in line:
            break

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

    for line in content:

        if current_process == None:
            process_started = False

        if "process" in line and "end" not in line:
            end_process_name = line.index(":")
            process_name = line[0:end_process_name].replace(" ", "").replace(
                "\t", "")
            current_process = Process(process_name)
            sensitivity_signals = find_sensitivity_signals(line)
            for signal in sensitivity_signals:
                current_process.set_sensitivity_signal(signal)

        if "begin" in line:
            process_started = True

        if "variable" in line and current_process != None:
            variable_declaration = line.split(":")
            variable_name = variable_declaration[0].split(
                "variable")[1].replace(" ", "")
            variable_type = variable_declaration[1].split(":=")
            variable_value = None

            if len(variable_type) > 1:
                variable_value = variable_type[1].replace(" ", "")

            current_process.set_internal_variable(
                variable_name,
                value=variable_value,
                variable_type=variable_type[0].replace("; ", ""))

        if "<=" in line and process_started == True:
            target_signal = line.split("<=")[0].replace("\t",
                                                        "").replace(" ", "")
            value = line.split("<=")[1].replace("\n", "").replace(";",
                                                                  "").replace(
                                                                      " ", "")
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


def main(filename):

    try:
        file_content, path = importfile(filename)
    except:
        return 1

    file_content = remove_comments(file_content)

    entity = find_entity_with_signals(file_content)
    for key in entity:
        print(key, ": ", entity[key])

    processes = find_processes(file_content)
    for process in processes:
        print("\n", process.get_process_name())

        print("   Sensitivity list:  ")
        for sens_signal in process.get_sensitivity_signals():
            print("    ", sens_signal)

        if len(process.get_internal_variables()) > 0:
            print("   Internal Variables:")
            for internal_variable in process.get_internal_variables():
                print("    ", internal_variable, ":",
                      process.get_internal_variables()[internal_variable])

        print("   Assigned Signals:  ")
        for assigned_signal in process.get_assigned_signals():
            print("    ", assigned_signal, ":",
                  process.get_assigned_signals()[assigned_signal])

    return 0


if __name__ == "__main__":
    print("Start program")
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None
    exit(main(filename))
