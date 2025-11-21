def tem_par_soma_igual(lista, valor_alvo):
    elementos_vistos = set() 
    
    for numero in lista:
        complemento = valor_alvo - numero
        
        if complemento in elementos_vistos:
            return True, (numero, complemento)
        
        elementos_vistos.add(numero)
        
    return False, None


Complexidade de Tempo: O(N) (Linear)

Explicação e Análise

A complexidade de tempo deste algoritmo é Linear, denotada por O(N), onde N é o número de elementos na lista de entrada.

    Iteração: O algoritmo executa um único loop for, percorrendo a lista de N elementos exatamente uma vez.

    Operações em Tempo Constante: Dentro do loop, as operações principais utilizam um conjunto (hash set):

        Cálculo do complemento: O(1).

        Consulta de existência (complemento in elementos_vistos): Tempo médio O(1).

        Inserção do número (elementos_vistos.add(numero)): Tempo médio O(1).
