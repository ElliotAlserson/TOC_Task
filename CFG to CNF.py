from collections import defaultdict

def cfg_to_cnf(grammar):
    nullable = find_nullable(grammar)
    grammar = remove_epsilon(grammar, nullable)
    grammar = remove_unit_productions(grammar)
    grammar = convert_to_cnf(grammar)
    return grammar

def find_nullable(grammar):
    nullable = set()
    changed = True
    while changed:
        changed = False
        for lhs, productions in grammar.items():
            for prod in productions:
                if prod == 'ε' and lhs not in nullable:
                    nullable.add(lhs)
                    changed = True
                elif all(s in nullable for s in prod):
                    if lhs not in nullable:
                        nullable.add(lhs)
                        changed = True
    return nullable

def remove_epsilon(grammar, nullable):
    new_grammar = defaultdict(list)
    for lhs, productions in grammar.items():
        for prod in productions:
            if prod == 'ε':
                continue
            new_prods = ['']
            for symbol in prod:
                if symbol in nullable:
                    new_prods = [p + s for p in new_prods for s in ('', symbol)]
                else:
                    new_prods = [p + symbol for p in new_prods]
            new_grammar[lhs].extend(p for p in new_prods if p)
    return dict(new_grammar)

def remove_unit_productions(grammar):
    unit_pairs = {lhs: {lhs} for lhs in grammar}
    changed = True
    while changed:
        changed = False
        for lhs in unit_pairs:
            for rhs in grammar.get(lhs, []):
                if len(rhs) == 1 and rhs.isupper() and rhs not in unit_pairs[lhs]:
                    unit_pairs[lhs].add(rhs)
                    changed = True
    
    new_grammar = defaultdict(list)
    for lhs, productions in grammar.items():
        for prod in productions:
            if len(prod) == 1 and prod.isupper():
                for B in unit_pairs[prod]:
                    new_grammar[lhs].extend(
                        p for p in grammar.get(B, []) 
                        if not (len(p) == 1 and p.isupper())
                    )
            else:
                new_grammar[lhs].append(prod)
    return dict(new_grammar)

def convert_to_cnf(grammar):
    terminal_map = {}
    var_counter = 0
    new_grammar = defaultdict(list)
    
    for lhs, productions in grammar.items():
        for prod in productions:
            if len(prod) == 1:
                new_grammar[lhs].append(prod)
            else:
                new_prod = []
                for s in prod:
                    if s.islower():
                        if s not in terminal_map:
                            new_var = f'T{var_counter}'
                            var_counter += 1
                            terminal_map[s] = new_var
                            new_grammar[new_var].append(s)
                        new_prod.append(terminal_map[s])
                    else:
                        new_prod.append(s)
                new_grammar[lhs].append(''.join(new_prod))
    
    grammar = dict(new_grammar)
    new_grammar = defaultdict(list)
    var_counter = 0
    
    for lhs, productions in grammar.items():
        for prod in productions:
            if len(prod) <= 2:
                new_grammar[lhs].append(prod)
            else:
                current = lhs
                remaining = prod
                while len(remaining) > 2:
                    new_var = f'N{var_counter}'
                    var_counter += 1
                    new_grammar[current].append(remaining[0] + new_var)
                    current = new_var
                    remaining = remaining[1:]
                new_grammar[current].append(remaining)
                
    return dict(new_grammar)

grammar = {
    'S': ['aB', 'bA', 'A'],
    'A': ['a', 'aS', 'bAA'],
    'B': ['b', 'bS', 'aBB']
}

cnf_grammar = cfg_to_cnf(grammar)
for lhs, prods in cnf_grammar.items():
    for prod in prods:
        print(f"{lhs} → {prod}")