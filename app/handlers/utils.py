import random

def generate_question():
    operations = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "//": lambda x, y: x // y,
        "%": lambda x, y: x % y,
    }
    
    operation = random.choice(list(operations.keys()))
    x = random.randint(1, 20)
    y = random.randint(1, 20)
    
    y, x = sorted([x, y])
    
    answer = operations[operation](x, y)
    
    additional = [answer + answer + random.randint(-(answer//2), answer//2) for _ in range(3)] if answer != 0 else [random.randint(1, 10) for _ in range(3)]
    
    variants = [answer] + additional
    
    variants = {variant: answer for variant in variants}
    
    return f"{x} {operation} {y} = ?", variants