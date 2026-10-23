import json
import ollama

def explorar():
    try:
        # 1. Cambiamos el archivo al nuevo JSON de triaje
        with open("TriageMascotas.json", encoding="utf-8") as f:
            nodo = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'TriageMascotas.json'")
        return

    camino = []
    
    while True:
        camino.append(nodo["valor"])
        hijos = nodo.get("hijos", [])
        
        print(f"\n" + "="*50)
        print(f" HISTORIAL DE SÍNTOMAS:\n > {' | '.join(camino)}")
        print("="*50)
        
        if not hijos:
            prompt = (
                f"El dueño de la mascota reportó estos síntomas: {' -> '.join(camino[:-1])}. "
                f"El sistema arrojó la siguiente conclusión: {nodo['valor']}. "
                "Con base en esta conclusión, redacta una respuesta empática, clara y directa para el dueño. "
                "Explícale la gravedad de la situación y dale las instrucciones de primeros auxilios paso a paso. "
                "Recuérdale al final que esto es una guía de emergencia y debe consultar a su veterinario."
            )
            
            print(f"\n[Ollama] Analizando síntomas y generando recomendaciones de primeros auxilios...")
            # --- PEGA ESTO EN SU LUGAR ---
            try:
                response = ollama.chat(
                    model='triaje-veterinario', 
                    messages=[
                        {
                            "role": "user", 
                            "content": prompt + "\n\nRECUERDA: Al final de tu respuesta, debes pegar exactamente la lista de clínicas de Popayán recomendadas."
                        }
                    ],
                    options={
                        "temperature": 0.1, 
                        "top_p": 0.85        
                    }
                )
            # -----------------------------
                print("\n" + "*"*50)
                print("RECOMENDACIÓN VETERINARIA:")
                print("*"*50)
                print(response['message']['content'])
            except Exception as e:
                print(f"\nError al conectar con Ollama: {e}")
            
            break

        print(f"\nSeleccione la opción que mejor describa la situación:")
        for i, h in enumerate(hijos, 1):
            print(f"{i}. {h['valor']}")

        while True:
            idx = input("\nNúmero > ")
            if idx.isdigit() and 1 <= int(idx) <= len(hijos):
                nodo = hijos[int(idx) - 1]
                break
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    explorar()