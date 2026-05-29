def add(a, b): return a + b
def subtract(a, b): return a - b
def multiply(a, b): return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

operations = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide,
}

def calculate(expression):
    for op in ['/', '*', '-', '+']:
        parts = expression.split(op)
        if len(parts) == 2:
            a, b = float(parts[0].strip()), float(parts[1].strip())
            return operations[op](a, b)
    raise ValueError(f"Invalid expression: {expression}")

tests = [
    ("10 + 5",  15.0),
    ("10 - 3",  7.0),
    ("4 * 7",   28.0),
    ("20 / 4",  5.0),
    ("9 / 3",   3.0),
    ("2.5 * 4", 10.0),
]

print("Python Calculator")
print("-" * 30)
all_passed = True
for expr, expected in tests:
    result = calculate(expr)
    status = "PASS" if result == expected else "FAIL"
    if status == "FAIL":
        all_passed = False
    print(f"  {expr} = {result}  [{status}]")

print("-" * 30)
print("All tests passed!" if all_passed else "Some tests failed.")
