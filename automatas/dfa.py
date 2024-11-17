class DFA:
    def __init__(self):
        self.states = []
        self.transitions = {}
        self.initial_state = "q0"
        self.accept_states = []
        self.alphabet = []

    def construir_desde_cadenas_validas(self, cadenas_validas):
        """
        Construye un NFA optimizado que acepte varias cadenas válidas.
        Si varias cadenas comparten un prefijo, utiliza un único conjunto de nodos para ese prefijo.
        """
        if not cadenas_validas:
            raise ValueError("No se proporcionaron cadenas válidas para construir el NFA.")

        self.states = ["q0"]
        self.initial_state = "q0"
        self.accept_states = []
        self.transitions = {}
        estado_count = 1

        for cadena in cadenas_validas:
            estado_actual = "q0"

            for simbolo in cadena:
                # Verificar si ya existe una transición para el símbolo actual
                if (estado_actual, simbolo) not in self.transitions:
                    # Si no existe, crear un nuevo estado
                    estado_siguiente = f"q{estado_count}"
                    self.states.append(estado_siguiente)
                    self.transitions[(estado_actual, simbolo)] = {estado_siguiente}
                    estado_count += 1
                else:
                    # Si ya existe una transición, seguimos al estado existente
                    estado_siguiente = list(self.transitions[(estado_actual, simbolo)])[0]

                # Avanzar al siguiente estado
                estado_actual = estado_siguiente

            # Marcar el último estado como de aceptación
            if estado_actual not in self.accept_states:
                self.accept_states.append(estado_actual)

        # Asegurarse de que el alfabeto contenga todos los símbolos de las cadenas
        for cadena in cadenas_validas:
            for simbolo in cadena:
                if simbolo not in self.alphabet:
                    self.alphabet.append(simbolo)

        return self

    def get_transitions(self):
        """Retorna las transiciones para el grafo."""
        return [(from_state, char, to_state) for (from_state, char), to_state_set in self.transitions.items() for to_state in to_state_set]