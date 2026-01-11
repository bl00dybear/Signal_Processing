### 1. Despachetarea Vectorului 

În cod, variabila noastră este compusă:

$$z = \begin{bmatrix} x \\ v \end{bmatrix}$$

Unde  sunt coeficienții modelului, iar  sunt variabilele auxiliare (limitele superioare).

### 2. Termenul Pătratic:  $\frac{1}{2} z^T P z$

În cod, am pus $P = \begin{bmatrix} 2A^T A & 0 \\ 0 & 0 \end{bmatrix}$. Hai să înmulțim:

$$\frac{1}{2} \begin{bmatrix} x^T & v^T \end{bmatrix} \begin{bmatrix} 2A^T A & 0 \\ 0 & 0 \end{bmatrix} \begin{bmatrix} x \\ v \end{bmatrix}$$
$$= \frac{1}{2} x^T (2 A^T A) x$$

Doiul de la numitor (1/2) se simplifică cu doiul din matrice (2), și rămâne:
$$= x^T A^T A x = ||Ax||^2$$

> **Rezultat partea 1:** Acest termen reprezintă "energia" semnalului prezis.

### 3. Termenul Liniar: $q^T z$

În cod, am pus $q = \begin{bmatrix} -2A^T b \\ \alpha \mathbf{1} \end{bmatrix}$. (Notă: în cod b este y). Hai să înmulțim:

$$\begin{bmatrix} -2b^T A & \alpha \mathbf{1}^T \end{bmatrix} \begin{bmatrix} x \\ v \end{bmatrix}$$
$$= \underbrace{-2 b^T A x}_{\text{Corelația cu ținta}} + \underbrace{\alpha \sum v_i}_{\text{Penalizarea Lasso}}$$

### 4. Punem totul împreună (Funcția Obiectiv)

Dacă adunăm Partea 1 și Partea 2, obținem exact ce minimizează solverul:

$$\text{Cost} = \underbrace{x^T A^T A x - 2 b^T A x}_{\text{Expansiunea lui } ||Ax - b||^2} + \alpha \sum v_i$$

*Notă matematică fină:* Lipsește termenul  (care e o constantă) pentru a fi exact , dar în optimizare constantele nu contează, pentru că nu schimbă poziția minimului. Deci, solverul minimizează exact eroarea pătratică.

### 5. Constrângerile: $G z \le h$

În cod, $G = \begin{bmatrix} I & -I \\ -I & -I \end{bmatrix}$ și $h=0$.

Asta se traduce în sistemul de inegalități:

1. $x - v \le 0 \Rightarrow x \le v$
2. $-x - v \le 0 \Rightarrow -x \le v \Rightarrow x \ge -v$

Combinate, înseamnă:

$$-v \le x \le v \quad \text{sau} \quad |x| \le v$$
---

### Rezumatul Final

Ecuația completă, "tradusă" din limba solverului în limba noastră, este:

**Minimizează:**
$$||Ax - b||_2^2 + \alpha \sum_{i} v_i$$

**Supus la condiția:**
$$|x_i| \le v_i \quad \text{pentru orice } i$$

Solverul trage de  să scadă eroarea (primul termen), dar e obligat să țină  mare dacă  e mare (din cauza constrângerii). Dar, pentru că  costă bani (termenul ), solverul preferă să facă  zero ca să poată face și  zero.