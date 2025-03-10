
def translate_large_text(text, source_lang='nl', target_lang='en', chunk_size=4999):
    """
    Translates large text by breaking it into chunks and translating each chunk.
    Falls back to alternative translators if one fails.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code
        target_lang (str): Target language code
        chunk_size (int): Maximum size of each chunk (default 4999 for Google)
        
    Returns:
        str: Full translated text
    """
    # Break text into chunks of chunk_size
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    
    # List of translator options with their respective implementations
    translators = [
        ('Google', lambda chunk: GoogleTranslator(source=source_lang, target=target_lang).translate(text=chunk)),
        ('Microsoft', lambda chunk: MicrosoftTranslator(source=source_lang, target=target_lang).translate(text=chunk)),
        ('MyMemory', lambda chunk: MyMemoryTranslator(source=source_lang, target=target_lang).translate(text=chunk)),
        ('DeepL', lambda chunk: DeeplTranslator(source=source_lang, target=target_lang).translate(text=chunk)),
        ('Papago', lambda chunk: PapagoTranslator(source=source_lang, target=target_lang).translate(text=chunk)),
        ('ChatGPT', lambda chunk: ChatGptTranslator(source=source_lang, target=target_lang).translate(text=chunk))
    ]
    
    translated_chunks = []
    
    for i, chunk in enumerate(chunks):
        success = False
        
        # Try each translator until one succeeds
        for name, translator_func in translators:
            try:
                translated_chunk = translator_func(chunk)
                translated_chunks.append(translated_chunk)
                print(f"Chunk {i+1}/{len(chunks)} translated using {name}")
                success = True
                
                # Add a small delay to avoid rate limiting
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"{name} translation failed: {str(e)}")
                continue
        
        if not success:
            print(f"Warning: Failed to translate chunk {i+1}")
            # Append original text if all translators fail
            translated_chunks.append(chunk)
    
    # Join all translated chunks
    return ''.join(translated_chunks)
