import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")


def generar_plan_alimentario(paciente, clasificacion, alimentos):
    nombres_alimentos = ", ".join([a.nombre for a in alimentos]) if alimentos else "alimentos básicos del PAE"

    prompt = f"""
    Eres un asistente nutricional especializado en nutrición infantil en zonas vulnerables de Colombia.
    
    Genera un plan alimentario personalizado y detallado para el siguiente paciente:
    
    - Nombre: {paciente.nombre_completo}
    - Edad: {paciente.edad} años
    - IMC: {paciente.imc}
    - Estado nutricional: {clasificacion}
    - Nivel socioeconómico: {paciente.get_nivel_socioeconomico_display()}
    - Nivel de actividad física: {paciente.get_nivel_actividad_display()}
    - Alergias: {", ".join([a.descripcion for a in paciente.alergias.all()]) or "ninguna"}
    - Alimentos PAE disponibles: {nombres_alimentos}
    
    El plan debe:
    1. Ser práctico y usar solo los alimentos PAE disponibles
    2. Incluir recomendaciones para desayuno, almuerzo y cena
    3. Considerar las alergias del paciente
    4. Ser comprensible para los padres o cuidadores
    5. Incluir una meta nutricional para el próximo mes
    
    Responde en español, de forma clara y empática. Máximo 300 palabras.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"No se pudo generar el plan con IA: {str(e)}"