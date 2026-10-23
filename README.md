# 🌳 Explorador Dinámico de Estructuras de Datos con IA (Ollama + Streamlit)

Aplicación interactiva desarrollada en Python para la materia **Estructuras de Datos No Lineales** (Colegio Mayor del Cauca). Permite navegar jerárquicamente por un árbol de conceptos paso a paso y, al alcanzar el último nivel (hoja), consulta a un modelo de lenguaje local (**Ollama**) para generar una explicación clara y pedagógica en tiempo real.

---

## 🚀 Puesta en Marcha Rápida

### 1. Requisitos Previos
* **Python 3.10+** (el proyecto ya incluye su entorno virtual en `.venv-1`).
* **Ollama**: Descargado e instalado desde [ollama.com](https://ollama.com/).
* Modelo local de Ollama descargado (por defecto: `llama3.2:1b`):
  ```bash
  ollama run llama3.2:1b
  ```

---

### 2. Ejecutar la Aplicación

Abre una terminal (PowerShell o CMD) en la carpeta del proyecto y ejecuta:

```powershell
.\.venv-1\Scripts\streamlit.exe run app.py
```

> **Nota:** Si tienes el entorno virtual activado, también puedes ejecutar simplemente:
> ```bash
> streamlit run app.py
> ```

---

### 3. Acceder al Entorno Gráfico

Una vez ejecutado el comando anterior, la consola mostrará la URL local. Abre tu navegador web favorito (Chrome, Edge, Firefox, etc.) e ingresa a:

👉 **[http://localhost:8501/](http://localhost:8501/)**

---

## 🧠 ¿Cómo Funciona la Aplicación?

1. **Navegación Paso a Paso**:
   * No satura la pantalla con todo el diagrama. En su lugar, muestra **una pregunta por pantalla** correspondiente al nivel actual.
   * Cada opción muestra un icono de carpeta (`📁`) si tiene más subcategorías o de documento (`📄`) si es un concepto final.

2. **Ruta Actual (Miga de pan / Breadcrumb)**:
   * En la parte superior siempre visualizas el camino recorrido (ejemplo: `Estructuras de Datos No Lineales ➔ Arboles ➔ Recorridos ➔ InOrden`).

3. **Explicación con IA en el Último Nivel**:
   * Al seleccionar un nodo hoja (sin más hijos), la app genera automáticamente un prompt contextual y consulta a Ollama con efecto de escritura en vivo (*streaming*).

4. **Controles de Navegación**:
   * **`⬅️ Paso anterior`**: Retrocede un nivel en la jerarquía.
   * **`🔄 Desde el inicio`**: Regresa a la raíz del árbol.
   * **`🔄 Regenerar respuesta`**: Solicita una nueva explicación a la IA.

---

## ⚡ Modificar el Árbol Dinámicamente (`EstructurasDeDatos.json`)

El programa **no tiene rutas fijas en el código Python**; lee y construye las preguntas directamente del archivo `EstructurasDeDatos.json`.

### Estructura de un Nodo:
```json
{
  "valor": "Nombre de la categoría o concepto",
  "pregunta": "¿Pregunta personalizada opcional?",
  "hijos": [
    {
      "valor": "Subtema 1"
    },
    {
      "valor": "Subtema 2",
      "hijos": [ ... ]
    }
  ]
}
```

### ¿Cómo agregar nuevas ramas?
1. Abre `EstructurasDeDatos.json` y agrega o modifica cualquier categoría (por ejemplo, añadir *Árboles AVL*, *Árboles B*, *Colas de Prioridad*, etc.).
2. Guarda el archivo `.json`.
3. En la barra lateral de la aplicación web, haz clic en **`🔄 Recargar JSON`**.
4. ¡Listo! La nueva opción y sus preguntas aparecerán de inmediato en el menú sin reiniciar el servidor.

---

## ⚠️ Consideraciones Importantes

* **Servicio de Ollama Activo**: Para que la IA responda, el servicio de Ollama debe estar en ejecución en tu equipo. Si la aplicación muestra un error de conexión:
  1. Abre una terminal y ejecuta `ollama serve` (o asegúrate de que la app de Ollama esté abierta en la barra de tareas de Windows).
  2. Haz clic en el botón **`🔄 Reintentar conexión con Ollama`** en la página web.
* **Modo Demostrativo Offline**: Si vas a exponer el proyecto en un equipo donde no esté instalado Ollama o no haya recursos suficientes, la aplicación incluye un botón:  
  **`💡 Ver explicación de prueba (Modo Offline)`**, el cual genera una respuesta didáctica simulada para que la presentación nunca falle.
* **Cambio de Modelo**: En la barra lateral puedes cambiar el modelo de Ollama en cualquier momento (ej: `llama3`, `mistral`, `gemma:2b`, etc.) y regular la creatividad con el deslizador de *Temperatura*.

---

## 📁 Estructura de Archivos del Proyecto

| Archivo | Descripción |
| :--- | :--- |
| **`app.py`** | Interfaz gráfica interactiva y dinámica desarrollada en Streamlit. |
| **`EstructurasDeDatos.json`** | Estructura jerárquica en árbol que alimenta las preguntas y opciones. |
| **`ApiLocal.py`** | Versión de consola original para recorrer el árbol. |
| **`ApiLLM.py`** | Script base de prueba para la librería de Ollama. |
| **`.venv-1/`** | Entorno virtual de Python con todas las dependencias instaladas. |
| **`README.md`** | Guía de uso, consideraciones y documentación técnica del proyecto. |
