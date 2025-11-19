class MemoryManager:
    def __init__(self):
        # Rangos de direcciones virtuales
        self.GLOBAL_INT_START = 1000
        self.GLOBAL_FLOAT_START = 2000
        
        self.LOCAL_INT_START = 3000
        self.LOCAL_FLOAT_START = 4000
        
        self.TEMP_INT_START = 5000
        self.TEMP_FLOAT_START = 6000
        self.TEMP_BOOL_START = 7000  
        
        self.CONST_INT_START = 8000
        self.CONST_FLOAT_START = 9000
        self.CONST_STRING_START = 10000  
        
        # Contadores actuales
        self.global_int_counter = self.GLOBAL_INT_START
        self.global_float_counter = self.GLOBAL_FLOAT_START
        
        self.local_int_counter = self.LOCAL_INT_START
        self.local_float_counter = self.LOCAL_FLOAT_START
        
        self.temp_int_counter = self.TEMP_INT_START
        self.temp_float_counter = self.TEMP_FLOAT_START
        self.temp_bool_counter = self.TEMP_BOOL_START
        
        self.const_int_counter = self.CONST_INT_START
        self.const_float_counter = self.CONST_FLOAT_START
        self.const_string_counter = self.CONST_STRING_START
        
        # Tabla de constantes
        self.constants_table = {}
    
    def get_global_address(self, var_type):
        """Obtiene dirección para variable global (solo int y float)"""
        if var_type == 'entero' or var_type == 'int':
            address = self.global_int_counter
            self.global_int_counter += 1
            return address
        elif var_type == 'flotante' or var_type == 'float':
            address = self.global_float_counter
            self.global_float_counter += 1
            return address
        else:
            raise ValueError(f"Tipo {var_type} no soportado en memoria global")
    
    def get_local_address(self, var_type):
        """Obtiene dirección para variable local (solo int y float)"""
        if var_type == 'entero' or var_type == 'int':
            address = self.local_int_counter
            self.local_int_counter += 1
            return address
        elif var_type == 'flotante' or var_type == 'float':
            address = self.local_float_counter
            self.local_float_counter += 1
            return address
        else:
            raise ValueError(f"Tipo {var_type} no soportado en memoria local")
    
    def get_temp_address(self, temp_type):
        """Obtiene dirección para variable temporal (int, float, bool)"""
        if temp_type == 'entero' or temp_type == 'int':
            address = self.temp_int_counter
            self.temp_int_counter += 1
            return address
        elif temp_type == 'flotante' or temp_type == 'float':
            address = self.temp_float_counter
            self.temp_float_counter += 1
            return address
        elif temp_type == 'bool' or temp_type == 'booleano':
            address = self.temp_bool_counter
            self.temp_bool_counter += 1
            return address
        else:
            raise ValueError(f"Tipo {temp_type} no soportado en memoria temporal")
    
    def get_constant_address(self, value, const_type):
        """Obtiene dirección para constante (int, float, string)"""
        key = f"{value}_{const_type}"
        if key in self.constants_table:
            return self.constants_table[key]
        
        if const_type == 'entero' or const_type == 'int':
            address = self.const_int_counter
            self.const_int_counter += 1
        elif const_type == 'flotante' or const_type == 'float':
            address = self.const_float_counter
            self.const_float_counter += 1
        elif const_type == 'string' or const_type == 'cadena':
            address = self.const_string_counter
            self.const_string_counter += 1
        else:
            raise ValueError(f"Tipo {const_type} no soportado en constantes")
        
        self.constants_table[key] = address
        return address
    
    def print_memory_distribution(self):
        """Muestra la distribución de memoria"""
        print("\n=== DISTRIBUCIÓN DE MEMORIA VIRTUAL ===")
        print(f"Variables Globales Enteras: {self.GLOBAL_INT_START} - {self.global_int_counter-1}")
        print(f"Variables Globales Flotantes: {self.GLOBAL_FLOAT_START} - {self.global_float_counter-1}")
        print(f"Variables Locales Enteras: {self.LOCAL_INT_START} - {self.local_int_counter-1}")
        print(f"Variables Locales Flotantes: {self.LOCAL_FLOAT_START} - {self.local_float_counter-1}")
        print(f"Temporales Enteros: {self.TEMP_INT_START} - {self.temp_int_counter-1}")
        print(f"Temporales Flotantes: {self.TEMP_FLOAT_START} - {self.temp_float_counter-1}")
        print(f"Temporales Booleanos: {self.TEMP_BOOL_START} - {self.temp_bool_counter-1}")
        print(f"Constantes Enteras: {self.CONST_INT_START} - {self.const_int_counter-1}")
        print(f"Constantes Flotantes: {self.CONST_FLOAT_START} - {self.const_float_counter-1}")
        print(f"Constantes String: {self.CONST_STRING_START} - {self.const_string_counter-1}")
        
        if self.constants_table:
            print("\n=== TABLA DE CONSTANTES ===")
            for key, address in self.constants_table.items():
                print(f"Dirección {address}: {key}")

memory_manager = MemoryManager()