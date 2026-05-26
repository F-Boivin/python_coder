"""Validador de flujo de trabajo Git + Django.

TP final del Módulo 8 del curso de Python de Coderhouse.

Lee una secuencia de eventos por entrada estándar y determina si la secuencia
representa un flujo de trabajo válido para un proyecto Django gestionado con
Git, según las reglas de la consigna:

  - El repositorio debe iniciarse con INIT.
  - Debe existir al menos una rama feature creada, con commits, y mergeada
    a main (modelado como CHECKOUT_BRANCH a una rama no-main, COMMIT en ella,
    y luego CHECKOUT_BRANCH main).
  - Los mensajes de commit no pueden estar vacíos.
  - Deben crearse los archivos requirements.txt, README.md, views.py y
    template.html (cualquiera de estos dos últimos puede tener otro nombre
    siempre que coincida el sufijo .py / .html y la palabra view/template).
  - Debe haber al menos un PUSH al remoto.
  - Debe haber al menos un PULL_REQUEST.

Salida: 'VALID' si la secuencia cumple todas las reglas, 'INVALID' si no.
"""

from collections import defaultdict


# Archivos exigidos por la consigna y por el feedback del corrector.
ARCHIVOS_REQUERIDOS = {
    "views.py",
    "template.html",
    "requirements.txt",
    "README.md",
}

# Conjunto de tipos de evento válidos. Cualquier otro tipo invalida la entrada.
TIPOS_VALIDOS = {
    "INIT",
    "CREATE_BRANCH",
    "CHECKOUT_BRANCH",
    "CREATE_FILE",
    "COMMIT",
    "PUSH",
    "PULL_REQUEST",
}


def validar(eventos):
    """Valida una secuencia de eventos de un repo Git + Django.

    Implementa retorno temprano: en cuanto se detecta una violación, se
    interrumpe el recorrido y se devuelve el motivo. No se acumulan flags
    para evaluar al final, salvo las cuatro condiciones que solo pueden
    evaluarse después de procesar toda la secuencia (merge, archivos,
    push, pull request).

    Args:
        eventos (list[str]): Líneas de eventos, en orden de ejecución.

    Returns:
        tuple[bool, str]: Par (es_valido, motivo). El motivo es 'OK' si la
            secuencia es válida; en caso contrario, una descripción breve
            de la regla violada.
    """
    # --- Estado del repositorio simulado ---
    init_hecho = False
    rama_actual = None
    ramas_creadas = {"main"}  # main existe implícitamente tras INIT
    archivos = set()
    commits_por_rama = defaultdict(int)
    ramas_mergeadas = set()  # feature branches que volvieron a main con commits
    hubo_push = False
    hubo_pr = False

    # --- Recorrido con retorno temprano ---
    for indice, linea in enumerate(eventos):
        partes = linea.strip().split(maxsplit=1)
        if not partes:
            return False, f"Evento {indice + 1}: línea vacía."

        tipo = partes[0]
        detalle = partes[1].strip() if len(partes) > 1 else ""

        if tipo not in TIPOS_VALIDOS:
            return False, f"Evento {indice + 1}: tipo desconocido '{tipo}'."

        # Regla: cualquier evento previo a INIT es inválido.
        if not init_hecho and tipo != "INIT":
            return False, f"Evento {indice + 1}: '{tipo}' antes de INIT."

        if tipo == "INIT":
            if init_hecho:
                return False, f"Evento {indice + 1}: INIT duplicado."
            if indice != 0:
                return False, "INIT no es el primer evento."
            init_hecho = True
            rama_actual = "main"

        elif tipo == "CREATE_BRANCH":
            if not detalle:
                return False, f"Evento {indice + 1}: CREATE_BRANCH sin nombre."
            ramas_creadas.add(detalle)

        elif tipo == "CHECKOUT_BRANCH":
            if not detalle:
                return False, f"Evento {indice + 1}: CHECKOUT_BRANCH sin nombre."
            if detalle not in ramas_creadas:
                return False, (
                    f"Evento {indice + 1}: CHECKOUT_BRANCH a rama inexistente "
                    f"'{detalle}'."
                )

            # Detección de merge: solo cuenta si la rama de origen era una
            # feature branch (no-main) Y tenía al menos un commit. Esto
            # asegura que el "merge" depende de la persistencia real de
            # commits, no del simple historial de cambios de rama.
            if (
                rama_actual is not None
                and rama_actual != "main"
                and detalle == "main"
                and commits_por_rama[rama_actual] > 0
            ):
                ramas_mergeadas.add(rama_actual)

            rama_actual = detalle

        elif tipo == "CREATE_FILE":
            if not detalle:
                return False, f"Evento {indice + 1}: CREATE_FILE sin nombre."
            archivos.add(detalle)

        elif tipo == "COMMIT":
            if not detalle:
                return False, f"Evento {indice + 1}: COMMIT con mensaje vacío."
            commits_por_rama[rama_actual] += 1

        elif tipo == "PUSH":
            if sum(commits_por_rama.values()) == 0:
                return False, (
                    f"Evento {indice + 1}: PUSH sin commits previos."
                )
            hubo_push = True

        elif tipo == "PULL_REQUEST":
            hubo_pr = True

    # --- Validaciones finales (solo evaluables tras procesar todo) ---
    if not init_hecho:
        return False, "Falta INIT al inicio del repositorio."

    if not ramas_mergeadas:
        return False, "No hay una feature branch con commits mergeada a main."

    faltantes = ARCHIVOS_REQUERIDOS - archivos
    if faltantes:
        return False, (
            f"Faltan archivos requeridos: {', '.join(sorted(faltantes))}."
        )

    if not hubo_push:
        return False, "Falta al menos un PUSH al remoto."

    if not hubo_pr:
        return False, "Falta al menos un PULL_REQUEST."

    return True, "OK"


def main():
    """Punto de entrada: lee N y N eventos de stdin, imprime VALID o INVALID."""
    n = int(input())
    eventos = [input() for _ in range(n)]
    es_valido, _motivo = validar(eventos)
    print("VALID" if es_valido else "INVALID")


if __name__ == "__main__":
    main()
