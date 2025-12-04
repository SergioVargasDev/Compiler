class MemoryManager:
    def __init__(self):
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
        
        self.constants_table = {}
    
    def get_global_address(self, var_type):
        if var_type == 'entero':
            address = self.global_int_counter
            self.global_int_counter += 1
            return address
        elif var_type == 'flotante':
            address = self.global_float_counter
            self.global_float_counter += 1
            return address
        else:
            raise ValueError(f"Tipo {var_type} no soportado en memoria global")
    
    def get_local_address(self, var_type):
        if var_type == 'entero':
            address = self.local_int_counter
            self.local_int_counter += 1
            return address
        elif var_type == 'flotante':
            address = self.local_float_counter
            self.local_float_counter += 1
            return address
        else:
            raise ValueError(f"Tipo {var_type} no soportado en memoria local")
    
    def get_temp_address(self, temp_type):
        if temp_type == 'entero':
            address = self.temp_int_counter
            self.temp_int_counter += 1
            return address
        elif temp_type == 'flotante':
            address = self.temp_float_counter
            self.temp_float_counter += 1
            return address
        elif temp_type == 'bool':
            address = self.temp_bool_counter
            self.temp_bool_counter += 1
            return address
        else:
            raise ValueError(f"Tipo {temp_type} no soportado en memoria temporal")
    
    def get_constant_address(self, value, const_type):
        key = f"{value}_{const_type}"
        if key in self.constants_table:
            return self.constants_table[key]
        
        if const_type == 'entero':
            address = self.const_int_counter
            self.const_int_counter += 1
        elif const_type == 'flotante':
            address = self.const_float_counter
            self.const_float_counter += 1
        elif const_type == 'letrero': 
            address = self.const_string_counter
            self.const_string_counter += 1
        else:
            raise ValueError(f"Tipo {const_type} no soportado en constantes")
        
        self.constants_table[key] = address
        return address
    
    def reset(self):
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
        self.constants_table.clear()
    
    def print_memory_distribution(self):
        print("\n=== DISTRIBUCIÓN DE MEMORIA VIRTUAL ===")
        
        print(f"Global Int:    {self.GLOBAL_INT_START} - {self.global_int_counter-1}")
        print(f" -> Total Usados: {self.global_int_counter - self.GLOBAL_INT_START}")
        
        print(f"Global Float:  {self.GLOBAL_FLOAT_START} - {self.global_float_counter-1}")
        print(f" -> Total Usados: {self.global_float_counter - self.GLOBAL_FLOAT_START}")
        
        print(f"Local Int:     {self.LOCAL_INT_START} - {self.local_int_counter-1}")
        print(f" -> Total Usados: {self.local_int_counter - self.LOCAL_INT_START}")
        
        print(f"Local Float:   {self.LOCAL_FLOAT_START} - {self.local_float_counter-1}")
        print(f" -> Total Usados: {self.local_float_counter - self.LOCAL_FLOAT_START}")
        
        print(f"Temp Int:      {self.TEMP_INT_START} - {self.temp_int_counter-1}")
        print(f" -> Total Usados: {self.temp_int_counter - self.TEMP_INT_START}")
        
        print(f"Temp Float:    {self.TEMP_FLOAT_START} - {self.temp_float_counter-1}")
        print(f" -> Total Usados: {self.temp_float_counter - self.TEMP_FLOAT_START}")
        
        print(f"Temp Bool:     {self.TEMP_BOOL_START} - {self.temp_bool_counter-1}")
        print(f" -> Total Usados: {self.temp_bool_counter - self.TEMP_BOOL_START}")
        
        print(f"Const Int:     {self.CONST_INT_START} - {self.const_int_counter-1}")
        print(f" -> Total Usados: {self.const_int_counter - self.CONST_INT_START}")
        
        print(f"Const Float:   {self.CONST_FLOAT_START} - {self.const_float_counter-1}")
        print(f" -> Total Usados: {self.const_float_counter - self.CONST_FLOAT_START}")
        
        print(f"Const String:  {self.CONST_STRING_START} - {self.const_string_counter-1}")
        print(f" -> Total Usados: {self.const_string_counter - self.CONST_STRING_START}")
        
        if self.constants_table:
            print("\n=== TABLA DE CONSTANTES ===")
            for key, address in self.constants_table.items():
                print(f"Dirección {address}: {key}")

memory_manager = MemoryManager()

if __name__ == "__main__":
    print("=== TESTEANDO MEMORY MANAGER ===")
    
    addr_x = memory_manager.get_global_address('entero')
    addr_y = memory_manager.get_global_address('entero')
    addr_z = memory_manager.get_global_address('entero')
    print(f"Globales Enteras (x,y,z): {addr_x}, {addr_y}, {addr_z}")

    addr_pi = memory_manager.get_global_address('flotante')
    print(f"Global Flotante (pi): {addr_pi}")

    addr_bool = memory_manager.get_temp_address('bool')
    print(f"Temporal Booleano: {addr_bool}")

    print("\n--- Test de Constantes ---")
    c1 = memory_manager.get_constant_address(10, 'entero')
    print(f"Constante 10 (1ra vez): {c1}")
    
    c2 = memory_manager.get_constant_address(10, 'entero')
    print(f"Constante 10 (2da vez): {c2}")
    
    c3 = memory_manager.get_constant_address(20, 'entero')
    print(f"Constante 20 (Nuevo):   {c3}")

    s1 = memory_manager.get_constant_address("Hola Mundo", 'letrero')
    print(f"Letrero 'Hola Mundo': {s1}")

    memory_manager.print_memory_distribution()
    
    print("\n--- Ejecutando RESET ---")
    memory_manager.reset()
    addr_new = memory_manager.get_global_address('entero')
    print(f"Nueva dirección tras reset: {addr_new}")