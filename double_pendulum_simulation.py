import math
import time
import csv
from multiprocessing import Pool, cpu_count

# Parametri
g = 9.81
m1 = 1.0
m2 = 1.0
l1 = 1.0
l2 = 1.0
theta1_0 = math.radians(120)
theta2_0 = math.radians(-10)
omega1_0 = 0.0
omega2_0 = 0.0
dt = 0.001
T = 10.0
N = int(T / dt)
korak_za_upis = int(1.0 / dt) 


def izracunaj_derivate(theta1, theta2, omega1, omega2):
    delta = theta2 - theta1

    denom1 = (m1 + m2) * l1 - m2 * l1 * math.cos(delta) ** 2
    denom2 = (l2 / l1) * denom1

    theta1_dot = omega1
    theta2_dot = omega2

    omega1_dot = (
        m2 * l1 * omega1 ** 2 * math.sin(delta) * math.cos(delta)
        + m2 * g * math.sin(theta2) * math.cos(delta)
        + m2 * l2 * omega2 ** 2 * math.sin(delta)
        - (m1 + m2) * g * math.sin(theta1)
    ) / denom1

    omega2_dot = (
        -m2 * l2 * omega2 ** 2 * math.sin(delta) * math.cos(delta)
        + (m1 + m2) * g * math.sin(theta1) * math.cos(delta)
        - (m1 + m2) * l1 * omega1 ** 2 * math.sin(delta)
        - (m1 + m2) * g * math.sin(theta2)
    ) / denom2

    return theta1_dot, theta2_dot, omega1_dot, omega2_dot


def ojler_korak(theta1, theta2, omega1, omega2, dt):
    th1_dot, th2_dot, om1_dot, om2_dot = izracunaj_derivate(theta1, theta2, omega1, omega2)
    return (
        theta1 + th1_dot * dt,
        theta2 + th2_dot * dt,
        omega1 + om1_dot * dt,
        omega2 + om2_dot * dt,
    )


def simulacija_sekvencijalno():
    print("Pokretanje sekvencijalne simulacije...")
    start = time.time()

    theta1, theta2, omega1, omega2 = theta1_0, theta2_0, omega1_0, omega2_0
    podaci = []

    for i in range(N + 1):
        if i % korak_za_upis == 0:  
            t = i * dt
            podaci.append((t, theta1, theta2, omega1, omega2))
        theta1, theta2, omega1, omega2 = ojler_korak(theta1, theta2, omega1, omega2, dt)

    vreme = time.time() - start
    print(f"Sekvencijalna simulacija završena za {vreme:.3f} s.")

    with open("sekvencijalno.csv", "w", newline="") as f:
        f.write("t,theta1,theta2,omega1,omega2\n")
        f.writelines(f"{t},{th1},{th2},{om1},{om2}\n" for t, th1, th2, om1, om2 in podaci)

    return podaci, vreme


def simulacija_segment(args):
    theta1, theta2, omega1, omega2, pocetak, kraj = args
    lokalni_podaci = []

    for i in range(pocetak, kraj):
        if i % korak_za_upis == 0:
            t = i * dt
            lokalni_podaci.append((t, theta1, theta2, omega1, omega2))
        theta1, theta2, omega1, omega2 = ojler_korak(theta1, theta2, omega1, omega2, dt)

    return lokalni_podaci


def simulacija_paralelno():
    print("Pokretanje fizički ispravne simulacije sa nastavkom segmenata...")
    start = time.time()

    broj_procesa = min(cpu_count(), 4)
    segment = N // broj_procesa

    svi_podaci = []
    pocetak = 0

    t1, t2, w1, w2 = theta1_0, theta2_0, omega1_0, omega2_0

    for i in range(broj_procesa):
        kraj = (i + 1) * segment if i < broj_procesa - 1 else N
        args = (t1, t2, w1, w2, pocetak, kraj)

        with Pool(processes=1) as pool:
            rezultat = pool.map(simulacija_segment, [args])[0]

        svi_podaci.extend(rezultat)

        _, t1, t2, w1, w2 = rezultat[-1]
        pocetak = kraj

    svi_podaci.sort(key=lambda x: x[0])

    vreme = time.time() - start
    print(f"Simulacija završena za {vreme:.3f} s (nastavlja segmente).")

    with open("paralelno.csv", "w", newline="") as f:
        f.write("t,theta1,theta2,omega1,omega2\n")
        f.writelines(f"{t},{th1},{th2},{om1},{om2}\n" for t, th1, th2, om1, om2 in svi_podaci)

    return svi_podaci, vreme


if __name__ == "__main__":
    print("=== Simulacija dvostrukog klatna ===")
    print("Parametri: dt =", dt, " T =", T, " broj koraka =", N)

    podaci_seq, vreme_seq = simulacija_sekvencijalno()
    podaci_par, vreme_par = simulacija_paralelno()

    print("\n--- Poređenje vremena ---")
    print(f"Sekvencijalno vreme: {vreme_seq:.3f} s")
    print(f"Paralelno vreme: {vreme_par:.3f} s")

    min_len = min(len(podaci_seq), len(podaci_par))
    max_odstupanje = max(
        abs(podaci_seq[i][1] - podaci_par[i][1])
        + abs(podaci_seq[i][2] - podaci_par[i][2])
        for i in range(min_len)
    )

    print(f"Maksimalno numeričko odstupanje: {max_odstupanje:.6e}")
    print("\nRezultati su sačuvani u fajlove: 'sekvencijalno.csv' i 'paralelno.csv'")
