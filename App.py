import tkinter as tk
from tkinter import filedialog
from transformers import LlamaForCausalLM, LlamaTokenizer
import PyPDF2

# Cargar modelo Llama
def load_llama_model():
    tokenizer = LlamaTokenizer.from_pretrained('Llama3.1-model')
    model = LlamaForCausalLM.from_pretrained('Llama3.1-model')
    return tokenizer, model

tokenizer, model = load_llama_model()

# Función para extraer texto de un PDF
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
    return text

# Función para procesar el currículum y generar uno nuevo
def generate_new_resume(text, job_title):
    input_text = f"Currículum: {text}\nPuesto deseado: {job_title}\nGenera un nuevo currículum con palabras clave relevantes."
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = model.generate(inputs['input_ids'], max_length=500)
    new_resume = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return new_resume

# Función para cargar el currículum
def load_resume():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    resume_text = extract_text_from_pdf(file_path)
    job_title = job_title_entry.get()
    generated_resume = generate_new_resume(resume_text, job_title)
    output_textbox.insert(tk.END, generated_resume)

# Interfaz gráfica con tkinter
app = tk.Tk()
app.title("Generador de Currículum con Llama 3.1")

# Entrada para el título del puesto
tk.Label(app, text="Puesto deseado:").pack()
job_title_entry = tk.Entry(app, width=50)
job_title_entry.pack()

# Botón para cargar el currículum
upload_button = tk.Button(app, text="Cargar Currículum (PDF)", command=load_resume)
upload_button.pack()

# Texto generado
output_textbox = tk.Text(app, height=20, width=80)
output_textbox.pack()

# Ejecutar la aplicación
app.mainloop()
