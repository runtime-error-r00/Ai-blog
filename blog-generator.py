"""
GENERATORE DI BLOG CON OPENAI GPT-3
====================================

Questo programma crea automaticamente articoli per blog utilizzando l'API di OpenAI.
Basta inserire un argomento e l'AI genererà paragrafi di testo su quel tema.

PREREQUISITI:
1. Python 3.10 o superiore
2. Account OpenAI (https://platform.openai.com/)
3. API Key di OpenAI

INSTALLAZIONE PACCHETTI:
pip install openai python-dotenv

CONFIGURAZIONE:
1. Crea un file .env nella stessa cartella
2. Aggiungi la tua API key: OPENAI_API_KEY=sk-tuachiave...
"""

import os
from dotenv import load_dotenv
import openai

# Carica le variabili d'ambiente dal file .env
# Questo serve per mantenere la API key sicura e non esporla nel codice
load_dotenv()

# Imposta la API key di OpenAI
# La chiave viene letta dal file .env per motivi di sicurezza
openai.api_key = os.getenv("OPENAI_API_KEY")

def genera_paragrafo(argomento):
    """
    Genera un singolo paragrafo su un argomento specifico usando GPT-3
    
    Args:
        argomento (str): Il tema su cui scrivere
        
    Returns:
        str: Un paragrafo generato dall'AI
    """
    # Chiamata all'API di OpenAI per generare testo
    response = openai.Completion.create(
        engine="text-davinci-003",  # Modello GPT-3 da utilizzare
        prompt=f"Scrivi un paragrafo informativo su: {argomento}",
        max_tokens=200,  # Lunghezza massima della risposta
        temperature=0.7,  # Creatività (0-1, più alto = più creativo)
        top_p=1.0,  # Diversità del vocabolario
        frequency_penalty=0.0,  # Penalità per ripetizioni
        presence_penalty=0.0  # Penalità per introdurre nuovi argomenti
    )
    
    # Estrae il testo generato dalla risposta
    return response.choices[0].text.strip()


def genera_blog(argomento, num_paragrafi=3):
    """
    Genera un articolo completo con più paragrafi
    
    Args:
        argomento (str): Il tema dell'articolo
        num_paragrafi (int): Numero di paragrafi da generare
        
    Returns:
        str: L'articolo completo
    """
    print(f"\n{'='*60}")
    print(f"GENERAZIONE ARTICOLO SU: {argomento.upper()}")
    print(f"{'='*60}\n")
    
    articolo = f"# {argomento.title()}\n\n"
    
    # Loop per generare più paragrafi
    for i in range(num_paragrafi):
        print(f"Generazione paragrafo {i+1}/{num_paragrafi}...")
        
        # Genera un paragrafo
        paragrafo = genera_paragrafo(argomento)
        
        # Aggiunge il paragrafo all'articolo
        articolo += f"{paragrafo}\n\n"
    
    print("\n✅ Articolo completato!")
    return articolo


def salva_articolo(articolo, nome_file="articolo_generato.md"):
    """
    Salva l'articolo in un file Markdown
    
    Args:
        articolo (str): Il testo dell'articolo
        nome_file (str): Nome del file dove salvare
    """
    with open(nome_file, "w", encoding="utf-8") as file:
        file.write(articolo)
    print(f"📄 Articolo salvato in: {nome_file}")


# ============================================
# PROGRAMMA PRINCIPALE
# ============================================

if __name__ == "__main__":
    print("\n🤖 GENERATORE DI BLOG CON AI 🤖")
    print("=" * 60)
    
    # Verifica che la API key sia configurata
    if not openai.api_key:
        print("\n⚠️  ERRORE: API key non trovata!")
        print("Crea un file .env e aggiungi: OPENAI_API_KEY=tua-chiave")
        exit()
    
    # Input dall'utente
    argomento = input("\n📝 Su quale argomento vuoi scrivere? ")
    
    try:
        num_paragrafi = int(input("📊 Quanti paragrafi vuoi generare? (consigliato: 3-5) "))
    except ValueError:
        print("⚠️  Numero non valido, uso default di 3 paragrafi")
        num_paragrafi = 3
    
    # Genera l'articolo
    try:
        articolo = genera_blog(argomento, num_paragrafi)
        
        # Mostra l'articolo
        print("\n" + "="*60)
        print("ARTICOLO GENERATO:")
        print("="*60)
        print(articolo)
        
        # Chiedi se salvare
        salva = input("\n💾 Vuoi salvare l'articolo? (s/n) ").lower()
        if salva == 's':
            nome_file = input("Nome file (default: articolo_generato.md): ").strip()
            if not nome_file:
                nome_file = "articolo_generato.md"
            if not nome_file.endswith('.md'):
                nome_file += '.md'
            
            salva_articolo(articolo, nome_file)
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        print("Verifica la tua API key e la connessione internet")

"""
COME FUNZIONA:
==============

1. CARICAMENTO CONFIGURAZIONE
   - Il programma legge la API key dal file .env
   - Questo protegge la chiave da essere esposta nel codice

2. GENERAZIONE PARAGRAFI
   - Per ogni paragrafo richiesto, viene fatta una chiamata all'API OpenAI
   - GPT-3 genera testo basandosi sull'argomento fornito
   - I paragrafi vengono concatenati per formare l'articolo

3. SALVATAGGIO
   - L'articolo può essere salvato in formato Markdown
   - Markdown è perfetto per blog e pubblicazioni web

PARAMETRI CHIAVE:
=================

- engine: Il modello AI da usare (text-davinci-003 è molto potente)
- max_tokens: Lunghezza massima (1 token ≈ 4 caratteri)
- temperature: Creatività (0=conservativo, 1=molto creativo)
- prompt: Le istruzioni che dai all'AI

COSTI:
======
L'API di OpenAI è a pagamento. Controlla i prezzi su:
https://openai.com/pricing

ALTERNATIVE MODERNE:
===================
Questo tutorial usa GPT-3, ma oggi puoi usare:
- GPT-4 (più potente)
- gpt-3.5-turbo (più economico)
- Chat completions API (più moderno)

Esempio con API moderna:
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": f"Scrivi su: {argomento}"}
    ]
)
"""