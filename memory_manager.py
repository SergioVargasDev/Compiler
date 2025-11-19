# memory_manager.py

class MemoryManager:
    def __init__(self):
        # Rangos de direcciones virtuales
        self.GLOBAL_INT_START = 1000
        self.GLOBAL_FLOAT_START = 2000
        self.LOCAL_INT_START = 3000
        self.LOCAL_FLOAT_START = 4000
        self.TEMP_INT_START = 5000
        self.TEMP_FLOAT_START = 6000
        self.CONST_INT_START = 7000
        self.CONST_FLOAT_START = 8000
        
        # Contadores actuales
        self.global_int_counter = self.GLOBAL_INT_START
        self.global_float_counter = self.GLOBAL_FLOAT_START
        self.local_int_counter = self.LOCAL_INT_START
        self.local_float_counter = self.LOCAL_FLOAT_START
        self.temp_int_counter = self.TEMP_INT_START
        self.temp_float_counter = self.TEMP_FLOAT_START
        self.const_int_counter = self.CONST_INT_START
        self.const_float_counter = self.CONST_FLOAT_START
        
        # Tabla de constantes
        self.constants_table = {}
    
    def get_global_address(self, var_type):
        """Obtiene dirección para variable global"""
        if var_type == 'entero':
            address = self.global_int_counter
            self.global_int_counter += 1
            return address
        else:  # flotante
            address = self.global_float_counter
            self.global_float_counter += 1
            return address
    
    def get_local_address(self, var_type):
        """Obtiene dirección para variable local"""
        if var_type == 'entero':
            address = self.local_int_counter
            self.local_int_counter += 1
            return address
        else:  # flotante
            address = self.local_float_counter
            self.local_float_counter += 1
            return address
    
    def get_temp_address(self, temp_type):
        """Obtiene dirección para variable temporal"""
        if temp_type == 'entero':
            address = self.temp_int_counter
            self.temp_int_counter += 1
            return address
        else:  # flotante
            address = self.temp_float_counter
            self.temp_float_counter += 1
            return address
    
    def get_constant_address(self, value, const_type):
        """Obtiene dirección para constante (evita duplicados)"""
        key = f"{value}_{const_type}"
        if key in self.constants_table:
            return self.constants_table[key]
        
        if const_type == 'entero':
            address = self.const_int_counter
            self.const_int_counter += 1
        else:  # flotante
            address = self.const_float_counter
            self.const_float_counter += 1
        
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
        print(f"Constantes Enteras: {self.CONST_INT_START} - {self.const_int_counter-1}")
        print(f"Constantes Flotantes: {self.CONST_FLOAT_START} - {self.const_float_counter-1}")
        
        if self.constants_table:
            print("\n=== TABLA DE CONSTANTES ===")
            for key, address in self.constants_table.items():
                print(f"Dirección {address}: {key}")

# Instancia global
memory_manager = MemoryManager()