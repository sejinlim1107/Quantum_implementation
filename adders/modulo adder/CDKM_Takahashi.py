# n-bit + n-bit = n-bit

from projectq import MainEngine
from projectq.ops import H, CNOT, Measure, Toffoli, X, All, Swap, Z, T, Tdag, S, Tdagger
from projectq.backends import CircuitDrawer, ResourceCounter, CommandPrinter, ClassicalSimulator
from projectq.meta import Loop, Compute, Uncompute, Control, Dagger

def Toffoli_gate(eng, a, b, c):
    if (NCT):
        Toffoli | (a, b, c)
    else:
        if(resource_check ==1):
            Tdag | a
            Tdag | b
            H | c
            CNOT | (c, a)
            T | a
            CNOT | (b, c)
            CNOT | (b, a)
            T  | c
            Tdag | a
            CNOT | (b, c)
            CNOT | (c, a)
            T | a
            Tdag | c
            CNOT | (b, a)
            H | c
        else:
            Toffoli | (a, b, c)

def Round_constant_XOR(rc, qubits, n):
    for i in range(n):
        if ((rc >> i) & 1):
            X | qubits[i]

def print_vector(eng, element, length):
    All(Measure) | element
    for k in range(length):
        print(int(element[length - 1 - k]), end='')
    print()

def CDKM(eng, a, b, c, n):
    for i in range(1, n-1):
        CNOT | (a[i], b[i])

    CNOT | (a[1], c)
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])

    for i in range(2, n-3):
        Toffoli_gate(eng, a[i-1], b[i], a[i])
        CNOT | (a[i + 2], a[i +1])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])
    CNOT | (a[n - 2], b[n - 1])
    Toffoli_gate(eng, a[n - 3], b[n - 2], b[n - 1])

    for i in range(1, n-2):
        X | b[i]

    CNOT | (c, b[1])

    for i in range(2,n-1):
        CNOT | (a[i-1], b[i])
    #CNOT | (a[n - 1], b[n - 1])

    Toffoli_gate(eng, a[n - 4], b[n - 3], a[n - 3])

    for i in range(n-4,1,-1):
        Toffoli_gate(eng, a[i-1], b[i], a[i])
        CNOT | (a[i+2], a[i+1])
        X | (b[i+1])

    Toffoli_gate(eng, c, b[1], a[1])
    CNOT | (a[3], a[2])
    X | b[2]
    Toffoli_gate(eng, a[0], b[0], c)
    CNOT | (a[2], a[1])
    X | b[1]
    CNOT | (a[1], c)

    for i in range(n):
        CNOT | (a[i], b[i])

def takahashi(eng,a,b,n): # modular adder

    for i in range(1,n):
        CNOT | (a[i], b[i])

    CNOT | (a[n-2], b[n-1])


    for i in range(n-3,0,-1):
        CNOT | (a[i], a[i+1])

    for i in range(n-2):
        Toffoli_gate(eng, a[i], b[i], a[i+1])

    Toffoli_gate(eng, a[n-2], b[n-2], b[n-1])

    for i in range(n-2,0,-1):
        CNOT | (a[i], b[i])
        Toffoli_gate(eng, a[i-1], b[i-1], a[i])

    for i in range(1,n-2):
        CNOT | (a[i], a[i+1])

    for i in range(n-1):
        CNOT | (a[i], b[i])

def test(eng):
    n = 5 # bit length
    a = eng.allocate_qureg(n)
    b = eng.allocate_qureg(n)
    ancilla = eng.allocate_qubit()

    if (resource_check != 1):
        Round_constant_XOR(0b10101, a, n)
        Round_constant_XOR(0b01010, b, n)

    if (resource_check != 1):
        print('a: ', end='')
        print_vector(eng, a, n)
        print('b: ', end='')
        print_vector(eng, b, n)

    CDKM(eng, a, b, ancilla, n)
    #takahashi(eng, a, b, n)

    if (resource_check != 1):
        print('sum: ', end='')
        print_vector(eng, b, n)

global resource_check
global NCT # NOT CNOT Toffoli (NCT == 1, 토폴리 분해 X)


print("--- adder_check ---")
resource_check = 0
NCT = 1
Resource = ClassicalSimulator()
eng = MainEngine(Resource)
test(eng)
eng.flush()

print()
print("--- resource_check ---")
resource_check = 1
Resource = ResourceCounter()
eng = MainEngine(Resource)
test(eng)
print(Resource)
