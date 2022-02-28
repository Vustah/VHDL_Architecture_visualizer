class Component:
    def __init__(self):
        self.generics = {}
        self.ports = {}
        return None
    def add_generic(self,generic,value):
        self.generics[generic] = value
    def add_port(self,port_name,value):
        self.ports[port_name] = value
    
    