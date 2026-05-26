# Guía de captura de screenshots — TP Módulo 8a

Lista ordenada de comandos para ejecutar en la **terminal de VS Code** y capturar con **Win + Shift + S** (selección rectangular del Snipping Tool de Windows). Pegá cada imagen en la carpeta `evidencia/` con el nombre indicado.

> **Antes de empezar:**
> 1. Abrí VS Code en la carpeta del repo: `C:\Users\Felipe\OneDrive\Documentos\Coder_Curso_Python\Claude\python_coder\`
> 2. Abrí una terminal nueva (`Ctrl + Shift + ñ`)
> 3. Si las tildes se ven mal, ejecutá `chcp 65001` una sola vez

---

## 1. Versión de Git instalada

```powershell
git --version
```

- **Screenshot:** `evidencia/01-git-version.png`
- **Qué capturar:** la línea del comando + la respuesta con la versión.
- **Esperado:** algo como `git version 2.47.0.windows.2`

---

## 2. Configuración global de usuario

Ejecutá los dos comandos **uno después del otro**:

```powershell
git config --global user.name
git config --global user.email
```

- **Screenshot 2a:** `evidencia/02a-config-name.png` — el comando del nombre y su respuesta (`Felipe Boivin`)
- **Screenshot 2b:** `evidencia/02b-config-email.png` — el comando del email y su respuesta (`felipe.epes@gmail.com`)
- Podés capturar ambos en una sola imagen si entran juntos en la ventana — en ese caso usá solo `02-config.png` y mencionalo en el Google Doc.

---

## 3. Estructura del repo `python_coder`

```powershell
ls
```

- **Screenshot:** `evidencia/03-estructura-repo.png`
- **Qué capturar:** la lista de archivos y carpetas (debería incluir `README.md`, `.gitignore`, `TP_Modulo_7b/`, `TP_Modulo_7c/`, `TP_Modulo_7_Final/`, `TP_Modulo_8a/`).

---

## 6-7. Mini-demo de transición de estados ⚠️ Leer antes

**Por qué:** la consigna pide demostrar `git add` y `git commit`. Este mini-demo crea un commit local, captura los tres estados, y al final **revierte el commit** para no ensuciar el repo. **NO HAGAS `git push`** durante este demo.

**Es seguro hacer esto porque:**
- El commit se queda solo en tu máquina local.
- `git reset --hard HEAD~1` deshace ese commit local antes de pushear.
- El historial remoto en GitHub no cambia.

Ejecutá los pasos en orden:

### 6.1 Crear archivo de prueba

```powershell
"Archivo de prueba para demo de estados de Git." | Out-File -FilePath prueba.txt -Encoding utf8
```

### 6.2 Verificar estado: untracked

```powershell
git status
```

- **Screenshot:** `evidencia/06a-status-untracked.png`
- **Qué capturar:** la sección que dice **"Untracked files"** con `prueba.txt` listado en rojo.

### 6.3 Mover a staging

```powershell
git add prueba.txt
```

(No tiene output. Continuá.)

### 6.4 Verificar estado: staged

```powershell
git status
```

- **Screenshot:** `evidencia/06b-status-staged.png`
- **Qué capturar:** la sección que dice **"Changes to be committed"** con `prueba.txt` listado en verde.

### 6.5 Hacer el commit

```powershell
git commit -m "Demo: agregar prueba.txt para mostrar transicion de estados"
```

- **Screenshot opcional:** `evidencia/06c-commit-realizado.png` — captura la respuesta de git con el hash del commit nuevo.

### 6.6 Verificar estado: limpio

```powershell
git status
```

- **Screenshot:** `evidencia/06d-status-clean.png`
- **Qué capturar:** el mensaje **"nothing to commit, working tree clean"** (también puede decir que tu rama está adelantada por 1 commit respecto a `origin/main`, eso está bien).

### 6.7 Cleanup: revertir el demo

⚠️ **Crítico:** ejecutar este paso para no contaminar el repo.

```powershell
git reset --hard HEAD~1
```

Esto borra el archivo `prueba.txt` Y revierte el commit que acabamos de hacer. Confirmá que volvió a su estado normal con:

```powershell
git status
git log --oneline -3
```

El último commit del log debería ser el que vos hiciste antes de este demo (el del TP 7-Final con la nota del 94% o lo que sea más reciente).

---

## 8. Estado actual del repo

```powershell
git status
```

- **Screenshot:** `evidencia/08-git-status.png`
- **Qué capturar:** la salida completa. Debería decir que estás en `main`, al día con `origin/main` (o con cambios pendientes si todavía no se pushearon los archivos de este TP).

---

## 9. Historial de commits reales

```powershell
git log --oneline -10
```

- **Screenshot:** `evidencia/09-git-log.png`
- **Qué capturar:** la lista de los 10 commits más recientes. Esto muestra el uso real y continuo de Git a lo largo del Módulo 7 (commits del 7b, 7c, 7-Final, registro de notas, etc.).

---

## Después de tomar todos los screenshots

1. Revisá que estén todas las imágenes en `evidencia/` (deberían ser 9-10 archivos `.png`).
2. Abrí un Google Doc nuevo y copiá el contenido del `README.md` de este TP.
3. Para cada sección "Screenshot: evidencia/XX.png", insertá la imagen correspondiente con **Insertar → Imagen → Subir desde la computadora**.
4. Compartí el doc con acceso público y subí el link.

**Tip:** podés convertir el README a Google Doc en un paso usando el flujo de `.docx`: si querés, después te genero un .docx con todo el formato listo para importar.
