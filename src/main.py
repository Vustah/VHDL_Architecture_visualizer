import sys
import os
from tkinter import filedialog


class Process:
    def __init__(self, process_name):
        self.process_name = process_name
        self.sensitivity_list = []
        self.internal_variables = []
        self.assigned_signals = {}

    def set_sensitivity_signal(self, signal):
        self.sensitivity_list.append(signal)

    def get_sensitivity_signals(self):
        return self.sensitivity_list

    def set_internal_variable(self, variable):
        self.internal_variables.append(variable)

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


def importfile(filename):
    if filename == None:
        filename = filedialog.askopenfilename()

    infile = open(filename, 'r')

    infile_content = []
    for line in infile.readlines():
        infile_content.append(line)
    return infile_content


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

        if "<=" in line and process_started != False:
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


def main(filename):

    # try:
    file_content = importfile(filename)
    # except:
    #     return 1

    entity = find_entity_with_signals(file_content)
    print(entity)
    processes = find_processes(file_content)
    for process in processes:
        print(process.get_process_name())
        print("Sensitivity list:", process.get_sensitivity_signals())
        print("Assigned Signals:", process.get_assigned_signals())

    return 0


if __name__ == "__main__":
    print("Start program")
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = None
    exit(main(filename))
