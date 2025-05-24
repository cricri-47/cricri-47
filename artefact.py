#!/usr/bin/env python3
import sys
import os
import math

def detect_constant_rho_segments(rhos, tol_rho=0.01, min_len=2):
    """
    Repère tous les segments contigus où rho reste constant (±tol_rho)
    et de longueur >= min_len. Retourne une liste de tuples
    (start_idx, end_idx, rho_ref).
    """
    segments = []
    N = len(rhos)
    i = 0
    while i < N:
        if rhos[i] is None:
            i += 1
            continue
        rho_ref = rhos[i]
        j = i + 1
        while j < N and rhos[j] is not None and abs(rhos[j] - rho_ref) <= tol_rho:
            j += 1
        if j - i >= min_len:
            segments.append((i, j - 1, rho_ref))
        i = j
    return segments

def filter_and_clean(input_path, output_path, tol_rho=0.01):
    """
    Lit input_path, supprime les segments où Δθ > π pour des runs à rho constant,
    corrige l'angle des points suivants pour éviter un nouveau saut,
    et écrit le résultat dans output_path. Retourne la liste des segments supprimés.
    """
    # lecture
    lines = open(input_path, 'r').read().splitlines(keepends=True)
    thetas, rhos = [], []
    for line in lines:
        s = line.strip()
        if not s or s.startswith('#'):
            thetas.append(None); rhos.append(None)
        else:
            parts = s.replace(',', ' ').split()
            thetas.append(float(parts[0]))
            rhos.append(float(parts[1]))

    # détection de tous les segments à rho constant
    segments = detect_constant_rho_segments(rhos, tol_rho=tol_rho, min_len=2)

    # filtrer ceux dont Δθ > π
    circle_segs = []
    for start, end, _ in segments:
        th1 = thetas[start]; th2 = thetas[end]
        if th1 is None or th2 is None:
            continue
        delta = th2 - th1
        if abs(delta) > math.pi:
            circle_segs.append((start, end, delta))

    # nettoyage + correction angulaire
    out_lines = []
    angle_offset = 0.0
    idx_circle = 0
    circle_segs_sorted = sorted(circle_segs, key=lambda x: x[0])
    N = len(lines)
    i = 0
    cs_len = len(circle_segs_sorted)
    while i < N:
        if idx_circle < cs_len and i == circle_segs_sorted[idx_circle][0]:
            _, end, delta = circle_segs_sorted[idx_circle]
            angle_offset += delta
            i = end + 1
            idx_circle += 1
            continue
        line = lines[i]
        s = line.strip()
        if s and not s.startswith('#'):
            parts = s.replace(',', ' ').split()
            theta = float(parts[0]) - angle_offset
            rho   = float(parts[1])
            out_lines.append(f"{theta:.6f} {rho:.6f}\n")
        else:
            out_lines.append(line)
        i += 1

    # écriture
    with open(output_path, 'w') as f:
        f.writelines(out_lines)

    return circle_segs_sorted

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <fichier.thr>")
        sys.exit(1)

    # voici la commande qui fonctionne chez moi :
    piste = sys.argv[1]
    base, _ = os.path.splitext(piste)
    outpath = f"{base}_center.thr"

    circles = filter_and_clean(piste, outpath, tol_rho=0.01)

    print(f"Output written to: {outpath}")
    print(f"Detected and removed {len(circles)} circle segment(s):")
    for idx, (st, ed, delta) in enumerate(circles, 1):
        print(f" {idx}. indices {st}→{ed}, Δθ={delta:.4f} rad")

if __name__ == "__main__":
    main()
