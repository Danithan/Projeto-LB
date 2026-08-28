import json
import re
import os

MD_FILE = 'AlgoritmosExercicios.md'
OUTPUT_FILE = 'catalogo_gerado.json'

def parse_markdown_to_json(md_path, json_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    exercicios = []
    
    current_faixa = ""
    current_fase = ""
    current_categoria = ""
    current_engine = ""
    
    # Regex patterns
    faixa_pattern = re.compile(r'^#\s*BLOCO\s*\d+:\s*(.*?)\s*\((.*?)\)')
    categoria_pattern = re.compile(r'^###\s*\d+\.\d+\s*Categoria:\s*(.*?)\s*\(')
    engine_pattern = re.compile(r'\*Engine:\s*`?([A-Z_]+)`?')

    in_table = False
    
    for line in lines:
        line = line.strip()
        
        m_faixa = faixa_pattern.match(line)
        if m_faixa:
            raw_faixa = m_faixa.group(1).strip()
            if "3 A 5 ANOS" in raw_faixa.upper():
                current_faixa = "3 a 5 anos"
            elif "6 A 10 ANOS" in raw_faixa.upper():
                current_faixa = "6 a 10 anos"
            elif "11+ ANOS" in raw_faixa.upper() or "11" in raw_faixa:
                current_faixa = "11+ anos"
            else:
                current_faixa = raw_faixa
                
            current_fase = m_faixa.group(2).strip()
            continue
            
        m_cat = categoria_pattern.match(line)
        if m_cat:
            current_categoria = m_cat.group(1).strip()
            continue
            
        m_engine = engine_pattern.search(line)
        if m_engine:
            current_engine = m_engine.group(1).strip()
            continue
            
        # Detect table
        if line.startswith('|') and '|' in line[1:]:
            # If it's header or separator
            if 'ID | Prompt |' in line or '|---|' in line or '---|---' in line:
                in_table = True
                continue
                
            if in_table:
                # Parse row
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 7: # ['', '1', 'Prompt', 'Opcoes', 'Resp', 'Gabarito', 'Comp', '']
                    try:
                        ex_id_str = re.sub(r'\D', '', parts[1])
                        if not ex_id_str: continue # possibly empty row
                        ex_id = int(ex_id_str)
                        prompt = parts[2]
                        
                        opcoes_raw = parts[3]
                        if opcoes_raw.startswith('`') and opcoes_raw.endswith('`'):
                            opcoes_raw = opcoes_raw[1:-1]

                        if opcoes_raw.startswith('[') and opcoes_raw.endswith(']'):
                            opcoes_raw = opcoes_raw.replace("'", '"')
                            try:
                                opcoes = json.loads(opcoes_raw)
                            except:
                                opcoes = [o.strip(' "`') for o in opcoes_raw.strip('[]').split(',')]
                        elif opcoes_raw == "-":
                            opcoes = []
                        else:
                            opcoes = [opcoes_raw] if opcoes_raw else []

                        gabarito_raw = parts[5]
                        if gabarito_raw.startswith('`') and gabarito_raw.endswith('`'):
                            gabarito_raw = gabarito_raw[1:-1]
                        
                        if gabarito_raw.startswith('[') and gabarito_raw.endswith(']'):
                            gabarito_raw = gabarito_raw.replace("'", '"')
                            try:
                                respostas = json.loads(gabarito_raw)
                            except:
                                respostas = [r.strip(' "`') for r in gabarito_raw.strip('[]').split(',')]
                        else:
                            respostas = [parts[4]]

                        competencia = parts[6]

                        ex_data = {
                            "id": ex_id,
                            "faixaEtaria": current_faixa,
                            "faseDesenvolvimento": current_fase,
                            "categoriaLogica": current_categoria,
                            "engineType": current_engine,
                            "prompt": prompt,
                            "opcoes": opcoes,
                            "respostasValidas": respostas,
                            "competenciaAlvo": competencia,
                            "metadata": {
                                "caseSensitive": False,
                                "ignoreAccents": True,
                                "trimWhitespace": True,
                                "allowAlternativeAnswers": True
                            }
                        }
                        exercicios.append(ex_data)
                    except Exception as e:
                        print(f"Error parsing line: {line} - {e}")
        else:
            in_table = False

    with open(json_path, 'w', encoding='utf-8') as out:
        json.dump(exercicios, out, ensure_ascii=False, indent=2)
        
    print(f"Successfully parsed {len(exercicios)} exercises into {json_path}")

if __name__ == "__main__":
    parse_markdown_to_json(MD_FILE, OUTPUT_FILE)
