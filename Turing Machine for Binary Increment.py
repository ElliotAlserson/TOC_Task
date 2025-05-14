def increment_binary(binary_str):
    tape = list(binary_str)
    tape.append('_')
    head = len(binary_str) - 1
    state = 'q0'
    
    while True:
        if state == 'q0':
            if head < 0:
                tape.insert(0, '1')
                break
            if tape[head] == '0':
                tape[head] = '1'
                break
            elif tape[head] == '1':
                tape[head] = '0'
                head -= 1
            else:
                tape[head] = '1'
                break
    
    return ''.join(tape).rstrip('_')

binary_number = '1011'
result = increment_binary(binary_number)
print(f"{binary_number} + 1 = {result}")