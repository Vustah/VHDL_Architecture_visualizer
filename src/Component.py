class Component:
    def __init__(self, name):
        self.generics = {}
        self.ports = {}
        self.name = name
    
    def get_name(self):
        return self.name

    def add_generic(self,generic,value):
        self.generics[generic] = value
    def get_generics(self):
        return self.generics

    def add_port(self,port_name,value):
        self.ports[port_name] = value
    def get_port(self):
        return self.ports

    def add_source(self,source):
        self.source = source
    def get_source(self):
        return self.source



    