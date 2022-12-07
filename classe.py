class Pessoa:
    def __init__(self, name, height, weight):
        self.name = name
        self.height = height
        self.weight = weight
    
    def fala(self):
        print(f"Meu nome é {self.name}!")

print(Pessoa)

#Joao = Pessoa("João", 26, 180, 70)
#print(Joao)

#print(Joao.name)
#print(Joao.age)

#Maria = Pessoa("Maria Silva", 50, 150, 50)
#print(Maria)

#print(Maria.name)

#Joao.age = 30

#print(Joao.age)

Pessoa.age = 60

Carlos = Pessoa("Carlos", 176, 58)

print(Carlos.age)

Pessoa.sobrenome = "Veras"
print(Carlos.sobrenome)

Carlos.fala()