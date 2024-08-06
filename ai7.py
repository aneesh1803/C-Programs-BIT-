class ForwardChaining:
    def __init__(self):
        self.facts = set()
        self.rules = []

    def add_fact(self, fact):
        self.facts.add(fact)

    def add_rule(self, conditions, conclusion):
        self.rules.append((conditions, conclusion))

    def infer(self):
        inferred = True
        new_facts = set()

        while inferred:
            inferred = False

            for conditions, conclusion in self.rules:
                if all(cond in self.facts for cond in conditions):
                    if conclusion not in self.facts:
                        new_facts.add(conclusion)
                        inferred = True
            self.facts.update(new_facts)

    def get_facts(self):
        return self.facts

fc = ForwardChaining()

fc.add_fact('Nation(Nono)')
fc.add_fact('Enemy(Nono,America)')
fc.add_fact('American(West)')
fc.add_fact('Missile(m1)')
fc.add_fact('Owns(Nono, m1)')
fc.add_fact('Sells(West,m1,Nono)')

fc.add_rule(['Missile(m1)'],'Weapon(m1)')
fc.add_rule(['Weapon(m1)', 'Sells(West,m1,Nono)', 'Enemy(Nono,America)','American(West)'], 'Criminal(West)')

fc.infer()

print("Final Facts: ")

for fact in fc.get_facts():
    print(fact)

if 'Criminal(West)' in fc.get_facts():
    print("Colonel west is a criminal")

else:
    print("Not criminal")
