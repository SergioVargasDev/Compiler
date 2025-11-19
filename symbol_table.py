# symbol_table.py
from memory_manager import memory_manager

class VariableTable:
    def __init__(self, parent_scope=None):
        self.variables = {}
        self.parent_scope = parent_scope
    
    def add_variable(self, name, var_type, scope='global'):
        if name in self.variables:
            raise Exception(f"Variable '{name}' ya declarada en este ámbito")
        
        # Obtener dirección virtual
        if scope == 'global':
            address = memory_manager.get_global_address(var_type)
        else:
            address = memory_manager.get_local_address(var_type)
        
        self.variables[name] = {
            'type': var_type,
            'address': address,
            'scope': scope
        }
        return address
    
    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent_scope:
            return self.parent_scope.get_variable(name)
        return None

class FunctionDirectory:
    def __init__(self):
        self.functions = {}
        self.current_function = 'global'
        self.global_scope = VariableTable()
        self.add_function('global', 'nula', [])
    
    def add_function(self, name, return_type, parameters):
        if name in self.functions:
            raise Exception(f"Función '{name}' ya declarada")
        
        local_scope = VariableTable(self.global_scope)
        
        self.functions[name] = {
            'return_type': return_type,
            'parameters': parameters,
            'local_scope': local_scope
        }
        return True
    
    def get_function(self, name):
        return self.functions.get(name)
    
    def function_exists(self, name):
        return name in self.functions
    
    def set_current_function(self, name):
        if name not in self.functions and name != 'global':
            raise Exception(f"Función '{name}' no declarada")
        self.current_function = name
    
    def get_current_scope(self):
        return self.functions[self.current_function]['local_scope']
    
    def add_parameter(self, func_name, param_name, param_type):
        if func_name not in self.functions:
            raise Exception(f"Función '{func_name}' no encontrada")
        
        func_info = self.functions[func_name]
        # Agregar parámetro con dirección local
        address = func_info['local_scope'].add_variable(param_name, param_type, 'local')
        func_info['parameters'].append({'name': param_name, 'type': param_type, 'address': address})
    
    def validate_call(self, func_name, arguments):
        if not self.function_exists(func_name):
            raise Exception(f"Función '{func_name}' no declarada")
        
        func_info = self.functions[func_name]
        params = func_info['parameters']
        
        if len(arguments) != len(params):
            raise Exception(f"Número incorrecto de argumentos para '{func_name}'. Esperados: {len(params)}, Obtenidos: {len(arguments)}")
        
        for i, (arg_type, param) in enumerate(zip(arguments, params)):
            if arg_type != param['type']:
                raise Exception(f"Tipo incorrecto en argumento {i+1} de '{func_name}'. Esperado: {param['type']}, Obtenido: {arg_type}")

function_directory = FunctionDirectory()