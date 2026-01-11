### 1. Despachetarea Vectorului 

În cod, variabila noastră este compusă:



Unde  sunt coeficienții modelului, iar  sunt variabilele auxiliare (limitele superioare).

### 2. Termenul Pătratic: 

În cod, am pus . Hai să înmulțim:

Doiul de la numitor () se simplifică cu doiul din matrice (), și rămâne:


> **Rezultat partea 1:** Acest termen reprezintă "energia" semnalului prezis.

### 3. Termenul Liniar: 

În cod, am pus . (Notă: în cod  este ). Hai să înmulțim:

### 4. Punem totul împreună (Funcția Obiectiv)

Dacă adunăm Partea 1 și Partea 2, obținem exact ce minimizează solverul:

*Notă matematică fină:* Lipsește termenul  (care e o constantă) pentru a fi exact , dar în optimizare constantele nu contează, pentru că nu schimbă poziția minimului. Deci, solverul minimizează exact eroarea pătratică.

### 5. Constrângerile: 

În cod,  și .

Asta se traduce în sistemul de inegalități:

1. 
2. 

Combinate, înseamnă:


---

### Rezumatul Final

Ecuația completă, "tradusă" din limba solverului în limba noastră, este:

**Minimizează:**


**Supus la condiția:**


Solverul trage de  să scadă eroarea (primul termen), dar e obligat să țină  mare dacă  e mare (din cauza constrângerii). Dar, pentru că  costă bani (termenul ), solverul preferă să facă  zero ca să poată face și  zero.