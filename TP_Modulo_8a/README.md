# TP Módulo 8 — Unidad 1: Git desde Cero

Trabajo práctico de la primera unidad del Módulo 8 del curso de Python de Coderhouse. Introducción a Git: estados, instalación, configuración y comandos básicos.

## Consigna

El ejercicio propone seguir paso a paso un tutorial básico de Git:

1. Instalar Git según el sistema operativo.
2. Configurar nombre y correo con `git config`.
3. Crear una carpeta nueva para un proyecto y navegar a ella.
4. Ejecutar `git init` para iniciar un repositorio local.
5. Crear un archivo `README.md` con texto.
6. Usar `git add` para preparar el archivo.
7. Realizar un commit con `git commit -m "..."`.
8. Ejecutar `git status` para verificar el estado actual.
9. Usar `git log` para ver el historial de commits.

> **Decisión de enfoque:** en lugar de armar un demo artificial "desde cero" (los pasos 3-7 ya los completé en su momento al iniciar este mismo repositorio `python_coder`), uso el repo activo como **evidencia real de uso de Git**. Esto cubre todos los puntos de la consigna con mayor autenticidad, y el mini-demo del punto 5 (más abajo) muestra explícitamente la transición de estados.

## Marco teórico

### ¿Qué es Git?

**Git** es un *sistema de control de versiones distribuido*: permite registrar los cambios realizados en archivos a lo largo del tiempo y coordinar el trabajo entre varias personas. A diferencia de sistemas centralizados como SVN, cada desarrollador tiene una copia completa del historial del repositorio en su máquina, lo que permite trabajar sin conexión, experimentar con ramas locales y tener redundancia natural ante pérdidas de información.

> *"Git ayuda a los desarrolladores a mantener un historial claro y organizado de su trabajo, facilitando la colaboración y el manejo de proyectos complejos."* — Git Book

### Los tres estados de Git

Todo archivo dentro de un repositorio Git vive en uno de tres "estados". Entender esto es la clave para usar Git sin sorpresas:

| Estado | Qué es | Cómo se entra | Cómo se sale |
|--------|--------|---------------|--------------|
| **Working Tree** (directorio de trabajo) | Carpeta del proyecto donde editás los archivos a mano. Los cambios viven acá hasta que decidís incluirlos. | Editar/crear/borrar archivos en la carpeta. | `git add <archivo>` los mueve al staging area. |
| **Staging Area** (índice) | Zona intermedia donde se preparan los cambios que van a entrar en el próximo commit. Permite armar commits parciales y revisar antes de confirmar. | `git add <archivo>` | `git commit -m "..."` los pasa al repositorio. |
| **Repository** (historial) | Base de datos local con los commits confirmados. Es el "registro permanente" del proyecto. | `git commit -m "..."` | Los commits no salen del repositorio: son inmutables. Se les puede revertir con nuevos commits o resetear referencias. |

**¿Por qué tres estados y no dos?** El staging area da una zona de "ensayo" antes de commitear. Permite agregar solo los cambios de una funcionalidad y dejar otros archivos modificados para un commit siguiente. Sin esto, cada commit incluiría obligatoriamente todo lo modificado.

### Comandos básicos

Lista mínima de comandos cubiertos en esta unidad, agrupados por el estado sobre el que operan:

| Comando | Sintaxis | Sobre qué estado opera | Qué hace |
|---------|----------|------------------------|----------|
| `git config` | `git config --global user.name "Nombre"` | Configuración global del usuario | Define quién hace cada commit (queda registrado en el historial). |
| `git init` | `git init` | Crea el repositorio | Inicializa el directorio actual como un repositorio Git nuevo (vacío). |
| `git add` | `git add <archivo>` o `git add .` | Working Tree → Staging | Marca los archivos indicados como "listos para commitear". |
| `git commit` | `git commit -m "mensaje"` | Staging → Repository | Crea un commit con todos los cambios en staging. El mensaje describe qué cambió. |
| `git status` | `git status` | Consulta los tres estados | Muestra qué hay sin trackear, modificado, en staging o limpio. |
| `git log` | `git log` o `git log --oneline` | Consulta el repositorio | Lista los commits en orden cronológico inverso con autor, fecha y mensaje. |

### Configuración global: por qué importa

Antes del primer commit, hay que decirle a Git con qué identidad firmar los cambios:

```bash
git config --global user.name "Felipe Boivin"
git config --global user.email "felipe.epes@gmail.com"
```

El flag `--global` aplica esa configuración para todos los repositorios del usuario en la máquina. Sin esto, los commits salen con autor "unknown" o Git directamente rechaza el commit. Esta información viaja con cada commit y queda en el historial — por eso es importante usar la misma identidad que tu cuenta de GitHub si vas a colaborar.

## Evidencia de ejecución sobre `python_coder`

Esta sección demuestra los nueve puntos de la consigna usando el repositorio activo `python_coder` como evidencia real. Cada bloque corresponde a un screenshot ubicado en la carpeta `evidencia/`.

### 1. Git instalado (Paso 1 de la consigna)

```bash
git --version
```

Se espera ver una respuesta tipo `git version 2.x.x.windows.x`. Confirma que Git está instalado y disponible en el PATH.

**Screenshot:** `evidencia/01-git-version.png`

### 2. Configuración global de identidad (Paso 2)

```bash
git config --global user.name
git config --global user.email
```

Se esperan los valores `Felipe Boivin` y `felipe.epes@gmail.com`. Sin esto Git no podría firmar los commits.

**Screenshots:** `evidencia/02a-config-name.png` y `evidencia/02b-config-email.png`

### 3, 4 y 5. Carpeta del proyecto + `git init` + README (Pasos 3-5)

Estos pasos ya fueron ejecutados en su momento al crear el repositorio `python_coder` (commit `2a94df9`, *"Inicializar repo con TP Modulo 7b - Manejo de archivos"*). El repo vive en:

```
C:\Users\Felipe\OneDrive\Documentos\Coder_Curso_Python\Claude\python_coder\
```

Y contiene un `README.md` raíz con el índice del curso. Para verificarlo:

```bash
ls
```

Se esperan ver carpetas (`TP_Modulo_7b`, `TP_Modulo_7c`, ...) y el `README.md` del repo.

**Screenshot:** `evidencia/03-estructura-repo.png`

### 6, 7. Mini-demo de transición de estados (Pasos 6-7)

Para demostrar explícitamente cómo un archivo transita por los tres estados (Working Tree → Staging → Repository), ejecuto la siguiente secuencia. **Importante:** este demo crea un commit local que se revierte al final con `git reset --hard HEAD~1`, así que **no se pushea** y no contamina el historial remoto.

```bash
# 6.1 Crear archivo nuevo en Working Tree
echo "Archivo de prueba para demo de estados" > prueba.txt

# 6.2 Verificar estado: untracked
git status
# Se espera ver "prueba.txt" listado bajo "Untracked files"

# 6.3 git add: mueve a Staging Area
git add prueba.txt

# 6.4 Verificar estado: staged
git status
# Se espera ver "prueba.txt" listado bajo "Changes to be committed"

# 6.5 Commit: mueve a Repository
git commit -m "Demo: agregar prueba.txt para mostrar transicion de estados"

# 6.6 Verificar estado: limpio
git status
# Se espera "nothing to commit, working tree clean"

# 6.7 Cleanup: revertir el commit local y borrar el archivo
git reset --hard HEAD~1
```

**Screenshots:** `evidencia/06a-status-untracked.png`, `evidencia/06b-status-staged.png`, `evidencia/06c-status-clean.png`

### 8. `git status` en condiciones normales (Paso 8)

```bash
git status
```

Se espera ver el estado actual del repo: rama actual, si está al día con `origin/main`, y qué archivos hay modificados/staged/untracked en este momento.

**Screenshot:** `evidencia/08-git-status.png`

### 9. `git log` con historial real (Paso 9)

```bash
git log --oneline -10
```

Se esperan ver los últimos 10 commits del repositorio — los commits de los TPs 7a/7b/7c/7-Final, las correcciones aplicadas y las actualizaciones de notas. Esto demuestra **uso continuo y real de Git**, no un demo de un solo commit.

**Screenshot:** `evidencia/09-git-log.png`

## Preguntas de autoevaluación

### ¿Cómo cambia el estado de un archivo al hacer `git add`?

`git add` mueve el archivo del **Working Tree** al **Staging Area**. Si el archivo era nuevo (untracked), pasa a estar "staged como nuevo". Si era un archivo previamente trackeado y modificado, pasa de "modified" a "staged for commit". El archivo en sí no se mueve físicamente — Git registra en su índice que esa versión es la que debe entrar en el próximo commit. Mientras tanto, el archivo en el Working Tree puede seguir modificándose, y esas modificaciones nuevas quedarían "unstaged" hasta el próximo `git add`.

### ¿Qué diferencia hay entre `git status` y `git log`?

- **`git status`** mira el **presente**: qué archivos están sin trackear, modificados, staged o limpios *en este momento*. Es la herramienta para responder "¿qué cambios tengo pendientes?".
- **`git log`** mira el **pasado**: lista los commits ya confirmados en orden cronológico inverso, con autor, fecha y mensaje. Es la herramienta para responder "¿qué se hizo y cuándo?".

Ambos consultan el repositorio pero apuntan a momentos distintos del flujo de trabajo.

### ¿Por qué Git se considera "distribuido"?

Porque cada copia local de un repositorio Git contiene **el historial completo del proyecto**, no solo la versión actual. Esto significa que:

1. Podés trabajar offline (hacer commits, ver el historial, crear ramas) sin conexión al servidor remoto.
2. No hay un punto único de falla: si el servidor remoto se cae o se pierde, cualquier copia local sirve para reconstruir el repo.
3. La colaboración funciona "punto a punto": cada desarrollador sincroniza con otros (típicamente vía un remoto compartido como GitHub) cuando lo decide, no en tiempo real.

En sistemas centralizados (SVN, CVS), el historial vive solo en el servidor y los clientes tienen únicamente la versión actual. Git invierte ese modelo.

### ¿Qué pasa si hago `commit` sin pasar por staging?

`git commit` sin argumentos solo commitea **lo que esté en staging**. Si no hay nada staged, Git responde con `nothing to commit, working tree clean` (o con un mensaje sobre cambios sin staged) y no crea el commit.

Existe el atajo `git commit -a` que stagea automáticamente todos los archivos *previamente trackeados* que estén modificados, y luego commitea. Pero los archivos nuevos (untracked) siguen siendo invisibles para `git commit -a` y necesitan un `git add` explícito.

Conclusión: en Git **no se puede saltar el staging area**, pero sí existen atajos para combinar `add + commit` cuando los cambios son sobre archivos ya conocidos.

## Reflexión: uso real de Git en este curso

Este TP es la primera unidad teórica sobre Git, pero el repositorio `python_coder` viene siendo usado desde el Módulo 7 como **respaldo, evidencia y portfolio de cada TP entregado**. A la fecha de esta entrega el repo contiene:

- **4 carpetas de TPs** ya entregados (Módulo 7b, 7c, 7 Final, y este 8a).
- **Una decena de commits** organizados por tipo de cambio:
  - Inicialización del repo.
  - Agregado de cada TP.
  - Registro de correcciones y notas recibidas.
- **`.gitignore`** configurado para excluir artefactos generados (`__pycache__/`, archivos de salida de los scripts, screenshots de evidencia).
- **README de índice** que mantiene la tabla actualizada con los TPs y sus notas.

Los conceptos teóricos de esta unidad (estados, comandos básicos, configuración) no son nuevos para este contexto — son las herramientas que ya vengo usando. Lo nuevo es ponerles nombre formal y entender *por qué* funciona como funciona.

## Cumplimiento de la consigna

| # | Punto de la consigna | Dónde se demuestra |
|---|----------------------|--------------------|
| 1 | Git instalado | Sección "Evidencia 1" — `git --version` |
| 2 | Configuración de `user.name` y `user.email` | Sección "Evidencia 2" — `git config --global` |
| 3 | Carpeta nueva creada | Sección "Evidencia 3-5" — repo `python_coder` |
| 4 | `git init` ejecutado | Sección "Evidencia 3-5" — repo ya inicializado en commit `2a94df9` |
| 5 | README.md con contenido | Sección "Evidencia 3-5" — README raíz del repo + este mismo README |
| 6 | `git add` ejecutado | Sección "Evidencia 6-7" — mini-demo de transición de estados |
| 7 | `git commit` con mensaje | Sección "Evidencia 6-7" + historial completo de commits |
| 8 | `git status` ejecutado | Sección "Evidencia 8" + secciones 6.2, 6.4, 6.6 del mini-demo |
| 9 | `git log` ejecutado | Sección "Evidencia 9" — historial real con 10+ commits |

## Estructura del TP

```
TP_Modulo_8a/
├── README.md                       ← Este archivo (entregable)
├── comandos_para_capturar.md       ← Guía paso a paso para sacar los screenshots
└── evidencia/                      ← Screenshots (no se commitean a Git, solo se usan para el Google Doc)
    └── .gitkeep
```

## Entrega

- **Google Doc:** _pendiente de agregar el link cuando se publique la entrega_
- **Nota recibida:** _pendiente_

> Para la entrega: copiar el contenido de este README en un Google Doc, embeber los screenshots de `evidencia/` en las secciones correspondientes (cada sección "Evidencia X" indica qué imagen va), y compartir el doc con acceso público.
