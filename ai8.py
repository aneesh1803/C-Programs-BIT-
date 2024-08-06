from typing import List, Tuple, Dict, Union

# Define data structures
Literal = Tuple[str, Tuple[str, ...]]  # A literal is a tuple (predicate, (arguments))
Clause = List[Literal]                 # A clause is a disjunction of literals
Substitution = Dict[str, str]          # A substitution maps variables to terms

# Unification algorithm
def unify(x: Union[str, Tuple[str, ...]], y: Union[str, Tuple[str, ...]], theta: Substitution) -> Union[Substitution, None]:
    if theta is None:
        return None
    elif x == y:
        return theta
    elif isinstance(x, str) and x.islower():  # x is a variable
        return unify_var(x, y, theta)
    elif isinstance(y, str) and y.islower():  # y is a variable
        return unify_var(y, x, theta)
    elif isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    else:
        return None

def unify_var(var: str, x: Union[str, Tuple[str, ...]], theta: Substitution) -> Union[Substitution, None]:
    if var in theta:
        return unify(theta[var], x, theta)
    elif x in theta:
        return unify(var, theta[x], theta)
    else:
        theta[var] = x
        return theta

# Apply substitution to a literal
def substitute_literal(literal: Literal, theta: Substitution) -> Literal:
    predicate, args = literal
    return (predicate, tuple(theta.get(arg, arg) for arg in args))

# Apply substitution to a clause
def substitute_clause(clause: Clause, theta: Substitution) -> Clause:
    return [substitute_literal(lit, theta) for lit in clause]

# Resolve two clauses
def resolve(c1: Clause, c2: Clause) -> List[Clause]:
    resolvents = []
    for lit1 in c1:
        for lit2 in c2:
            if (lit1[0] == lit2[0] and lit1[0].startswith('¬') and not lit2[0].startswith('¬')) or \
               (lit2[0] == lit1[0] and lit2[0].startswith('¬') and not lit1[0].startswith('¬')):
                theta = unify(lit1[1], lit2[1], {})
                if theta is not None:
                    new_c1 = [l for l in c1 if l != lit1]
                    new_c2 = [l for l in c2 if l != lit2]
                    new_clause = substitute_clause(new_c1 + new_c2, theta)
                    resolvents.append(new_clause)
    return resolvents

# Example problem: Colonel West is a criminal
clauses = [
    [('¬Sells',('x','y','z')),('¬Hostile',('z',)),('Criminal',('x',))],# Clause 1
    [('Missile',('M1',))],  # Clause 2
    [('¬Missile',('x',)),('Weapon',('x',))],  # Clause 3
    [('Enemy', ('Nono','America'))],  # Clause 4
    [('¬Owns', ('Nono','x')),('¬Missile',('x',)),('Hostile',('Nono',))],  # Clause 5
    [('Sells', ('West','Nono','M1'))],  # Clause 6
    [('Owns', ('Nono','M1'))]  # Clause 7
]

# Resolution algorithm
def resolution(clauses: List[Clause]) -> bool:
    new = set()
    while True:
        pairs = [(clauses[i], clauses[j])
                 for i in range(len(clauses)) 
                 for j in range(i + 1,len(clauses))]
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if [] in resolvents:  # Found an empty clause
                return True
            new.update(set(map(lambda clause:
                            tuple(map(tuple,clause)), resolvents)))
        if new.issubset(set(map(lambda clause:
                            tuple(map(tuple, clause)), clauses))):
            return False
        clauses.extend(map(list, new))

# Check if Colonel West is a criminal
goal = [('¬Criminal', ('West',))]
clauses.append(goal)
is_criminal = resolution(clauses)
print("Colonel West is a criminal:", not is_criminal)
