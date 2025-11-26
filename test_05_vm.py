import unittest
import io
import sys
from patito_parser import parser
from patito_lexer import lexer
from symbol_table import function_directory
from quadruples import quadruple_manager
from memory_manager import memory_manager
from virtual_machine import VirtualMachine

def reset_compiler():
    function_directory.functions = {}
    function_directory.current_function = 'global'
    function_directory.global_scope.variables = {}
    function_directory.add_function('global', 'nula', [])
    quadruple_manager.clear()
    memory_manager.reset()

class TestVM(unittest.TestCase):
    def setUp(self):
        reset_compiler()
        print(f"\n{'-'*60}")
        print(f"Running VM Test: {self._testMethodName}")
        print(f"{'-'*60}")

    def run_vm(self, code):
        print("[INFO] Compilando código...")
        parser.parse(code, lexer=lexer)
        print("[INFO] Iniciando Máquina Virtual...")
        # Nota para el usuario: La VM recibe cuádruplos con DIRECCIONES DE MEMORIA (ej. 1000, 5000).
        # Imprimimos los cuádruplos "crudos" para verificar esto.
        quadruple_manager.print_quadruples_raw()
        
        vm = VirtualMachine(quadruple_manager.quadruples, memory_manager.constants_table)
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        try:
            vm.run()
        finally:
            sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue().strip().split('\n')
        print(f"[INFO] Salida de la VM: {output}")
        return output

    def test_arithmetic_precedence(self):
        print("[INFO] Probando precedencia aritmética...")
        code = '''
        programa aritmetica;
        vars x : entero;
        inicio
            x = 10 + 5 * 2;
            escribe(x);
            x = (10 + 5) * 2;
            escribe(x);
        fin
        '''
        output = self.run_vm(code)
        self.assertEqual(output, ['20', '30'])
        print("[SUCCESS] Precedencia aritmética verificada.")

    def test_factorial_iterative(self):
        print("[INFO] Probando Factorial Iterativo...")
        code = '''
        programa FactorialIterativo;
        vars
            n, resultado : entero;

        entero factorial(numero : entero) {
            vars
                i, acumulador : entero;
            {
                acumulador = 1;
                i = 1;
                
                mientras (i < numero) haz {
                    i = i + 1;
                    acumulador = acumulador * i;
                };
                
                factorial = acumulador;
            }
        }

        inicio
            n = 5;
            resultado = factorial(n);
            escribe(resultado);
        fin
        '''
        output = self.run_vm(code)
        self.assertEqual(output[-1], '120')
        print("[SUCCESS] Factorial iterativo verificado.")

    def test_fibonacci_recursive(self):
        print("[INFO] Probando Fibonacci Recursivo...")
        code = '''
        programa FibonacciRecursivo;
        vars
            n, resultado : entero;

        entero fibonacci(numero : entero) {
            vars
                fib1, fib2, temp : entero;
            {
                si (numero < 2) {
                    fibonacci = numero;
                } sino {
                    temp = numero - 1;
                    fib1 = fibonacci(temp);
                    temp = numero - 2;
                    fib2 = fibonacci(temp);
                    fibonacci = fib1 + fib2;
                };
            }
        }

        inicio
            n = 5;
            resultado = fibonacci(n);
            escribe(resultado);
        fin
        '''
        output = self.run_vm(code)
        self.assertEqual(output[-1], '5')
        print("[SUCCESS] Fibonacci recursivo verificado.")

    def test_complex_case(self):
        print("[INFO] Probando Caso Complejo (Recursión + Ciclos + Globales)...")
        code = '''
        programa PatitoComplejo;
        vars
            i, j, k : entero;
            f : flotante;

        nula uno(a : entero, b : entero) {
            {
                si (a > 0) {
                    i = a + b * j + i;
                    escribe(i + j);
                    uno(a - i, i);
                } sino {
                    escribe(a + b);
                };
            }
        }

        entero dos(a : entero, g : flotante) {
            vars
                i : entero;
            {
                i = a;
                mientras (a > 0) haz {
                    a = a - k * j;
                    uno(a * 2, a + k);
                    g = g * j - k;
                };
                dos = i + k * j;
            }
        }

        inicio
            i = 2;
            j = 1; 
            k = 20; 
            f = 3.14;
            
            mientras (i > 0) haz {
                escribe(dos(i + k, f * 3) + 3);
                escribe(i, j * 2, f * 2 + 1.5);
                i = i - k * 5; 
            };
        fin
        '''
        output = self.run_vm(code)
        expected_output = ['29', '4', '-34', '45', '28', '2', '7.78']
        
        # Filter out empty lines if any
        actual_output = [line for line in output if line]
        
        self.assertEqual(actual_output, expected_output)
        print("[SUCCESS] Caso complejo verificado.")

if __name__ == '__main__':
    unittest.main()
