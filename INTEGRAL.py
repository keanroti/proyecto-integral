# ==========================================
# Proyecto: Aproximacion de integrales
# Metodo: Sumas inferiores y superiores
# Autor: Kevin Rojas
# Requiere: numpy, matplotlib
# ==========================================
 

import numpy as np
import matplotlib.pyplot as plt
import math
plt.switch_backend('TkAgg')
def resolver_expresion(texto):
    contexto_seguro = {
        'pi': math.pi, 'e': math.e, 'sqrt': math.sqrt,
        'sin': math.sin, 'cos': math.cos, 'exp': math.exp
    }
    try:
        return float(eval(texto.lower(), {"__builtins__": None}, contexto_seguro))
    except Exception:
        print("Entrada inválida. Se usó 0.")
        return 0.0

def evaluar_polinomio(coef, x):
    
    return sum(a_i * (x**i) for i, a_i in enumerate(coef))

def generar_particion_ingeniosa(a, b, nivel):
    
    puntos = [a, b]
    for _ in range(nivel):
        nuevos_puntos = []
        for i in range(len(puntos) - 1):
            x0, x1 = puntos[i], puntos[i+1]
            t1 = x0 + (x1 - x0) / 3
            t2 = x1 - (x1 - x0) / 3
            nuevos_puntos.extend([x0, t1, t2])
        nuevos_puntos.append(puntos[-1])
        puntos = sorted(list(set(nuevos_puntos)))
    return np.array(puntos)

def calcular_integrales_escalonadas(coef, particion):
    
    suma_izq = 0
    suma_der = 0
    for i in range(len(particion) - 1):
        dx = particion[i+1] - particion[i]
        suma_izq += evaluar_polinomio(coef, particion[i]) * dx
        suma_der += evaluar_polinomio(coef, particion[i+1]) * dx
    return min(suma_izq, suma_der), max(suma_izq, suma_der)

def ejecutar_proyecto():
    print("="*50)
    print("    FACULTAD DE INGENIERÍA - UDEC (PROYECTO 1)    ")
    print("="*50)
    print("Sugerencia: Puedes usar 'pi', 'e', 'sqrt(2)', '1/3'...")

    n_grado = int(resolver_expresion(input("Grado n del polinomio: ")))
    coef = [resolver_expresion(input(f"Coeficiente a_{i}: ")) for i in range(n_grado + 1)]
    a = resolver_expresion(input("Límite inferior a: "))
    b = resolver_expresion(input("Límite superior b: "))
    epsilon_target = resolver_expresion(input("Tolerancia epsilon (M-m): "))
    
    nivel = 1
    error = float('inf')
    plt.ion()
    fig, ax = plt.subplots(figsize=(11, 7))

    while error > epsilon_target and nivel <= 15:
        S = generar_particion_ingeniosa(a, b, nivel)
        m, M = calcular_integrales_escalonadas(coef, S)
        error = M - m 
        
        print(f"Iteración {nivel} | Particiones: {len(S)} | Error (M-m): {error:.6f}")
        

        ax.clear()
        x_plot = np.linspace(a, b, 500)
        y_plot = [evaluar_polinomio(coef, x) for x in x_plot]
        ax.plot(x_plot, y_plot, 'k', linewidth=2, label='p(x)', zorder=10)

        paso = max(1, len(S) // 2000)
        for i in range(0, len(S) - 1, paso):
            x0, x1 = S[i], S[min(i + paso, len(S) - 1)]
            y_izq, y_der = evaluar_polinomio(coef, x0), evaluar_polinomio(coef, x1)
            v_min, v_max = min(y_izq, y_der), max(y_izq, y_der)
            
            
            ax.add_patch(plt.Rectangle((x0, 0), x1-x0, v_min, color='skyblue', alpha=0.5))
            ax.add_patch(plt.Rectangle((x0, v_min), x1-x0, v_max - v_min, color='red', alpha=0.3))
            ax.hlines(y_izq, x0, x1, colors='blue', label='g_izq' if i == 0 else "")
            ax.hlines(y_der, x0, x1, colors='red', label='g_der' if i == 0 else "")
        
        info_txt = f"I ∈ [{m:.6f}, {M:.6f}]\nError: {error:.6f}\nParticiones: {len(S)}"
        ax.text(0.02, 0.95, info_txt, transform=ax.transAxes, verticalalignment='top', 
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.set_title(f"Aproximacion - Iteración {nivel}")
        
        if nivel <= 6:
            plt.pause(0.3)
        
        if error <= epsilon_target:
            break
        nivel += 1

    plt.ioff()
    
    if error > epsilon_target:
        print(f"\nNo se alcanzo el epsilon ({epsilon_target}) en 15 niveles// nivel 15  = 146 millones de particiones.")
    else:
        print(f"\nTolerancia alcanzada.")

    print(f"RESULTADO FINAL: I ∈ [{m:.6f}, {M:.6f}]")
    print(f"Finura alcanzada: {len(S)} particiones")
    print(f"acercamiento por debajo (m): {m:.6f} | por encima (M): {M:.6f} | error (M-m): {error:.6f}")
    print(f"epsilon objetivo: {epsilon_target:.6f}")
    ax.set_title(f"Resultado Final - I ∈ [{m:.6f}, {M:.6f}]")
    plt.show()

if __name__ == "__main__":
    ejecutar_proyecto()