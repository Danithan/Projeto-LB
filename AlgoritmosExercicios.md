# Especificação Técnica e Algoritmos dos Exercícios (270 Exercícios)
## Projeto LB — Plataforma de Sessões Terapêuticas Infantis

Documentação técnica, formal e **AI-Ready** contendo os algoritmos de validação, taxonomia, esquemas de dados e o catálogo completo dos 270 exercícios divididos por faixas etárias e competências cognitivas.

---

## 1. Arquitetura do Motor de Execução e Validação (Engine Specs)

Todos os exercícios operam sob uma interface unificada de avaliação algorítmica, permitindo integração direta com o front-end (Vanilla JS/Canvas/DOM) e back-end (Django Models & REST API).

### 1.1 JSON Schema Universal do Exercício (`ExercicioModelo.configuracao`)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ExercicioConfiguracao",
  "type": "object",
  "properties": {
    "id": { "type": "integer" },
    "faixaEtaria": { "type": "string", "enum": ["3 a 5 anos", "6 a 10 anos", "11+ anos"] },
    "faseDesenvolvimento": { "type": "string" },
    "categoriaLogica": { "type": "string" },
    "engineType": { 
      "type": "string", 
      "enum": [
        "SINGLE_CHOICE",
        "TRUE_FALSE",
        "ANAGRAM_ORDER",
        "SENTENCE_ORDER",
        "GAP_FILL",
        "SHADOW_PAIR",
        "INTRUDER_SELECTION",
        "NUMERIC_SEQUENCE"
      ] 
    },
    "prompt": { "type": "string" },
    "opcoes": { 
      "type": "array", 
      "items": { "type": "string" } 
    },
    "respostasValidas": { 
      "type": "array", 
      "items": { "type": "string" } 
    },
    "competenciaAlvo": { "type": "string" },
    "metadata": {
      "type": "object",
      "properties": {
        "caseSensitive": { "type": "boolean", "default": false },
        "ignoreAccents": { "type": "boolean", "default": true },
        "trimWhitespace": { "type": "boolean", "default": true },
        "allowAlternativeAnswers": { "type": "boolean", "default": true }
      }
    }
  },
  "required": ["id", "faixaEtaria", "categoriaLogica", "engineType", "prompt", "opcoes", "respostasValidas", "competenciaAlvo"]
}
```

### 1.2 Algoritmo Central de Normalização e Avaliação (Pseudo-código)

```typescript
interface ExerciseResult {
  isCorrect: boolean;
  score: number;             // 0 a 100
  feedback: string;
  attemptsCount: number;
  timeSpentSeconds: number;
}

function normalizeText(input: string, ignoreAccents: boolean = true): string {
  let normalized = input.trim().toUpperCase();
  if (ignoreAccents) {
    normalized = normalized.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
  }
  return normalized.replace(/\s+/g, " ");
}

function evaluateExercise(
  userInput: string | string[], 
  exercise: ExerciseConfig, 
  timeSpent: number, 
  attempts: number
): ExerciseResult {
  const meta = exercise.metadata || { ignoreAccents: true, caseSensitive: false, trimWhitespace: true };
  let isCorrect = false;

  switch (exercise.engineType) {
    case "ANAGRAM_ORDER":
    case "GAP_FILL":
    case "SINGLE_CHOICE":
    case "INTRUDER_SELECTION":
    case "TRUE_FALSE":
    case "NUMERIC_SEQUENCE":
      const formattedInput = normalizeText(String(userInput), meta.ignoreAccents);
      isCorrect = exercise.respostasValidas.some(ans => 
        normalizeText(ans, meta.ignoreAccents) === formattedInput ||
        normalizeText(ans.split(" ")[0], meta.ignoreAccents) === formattedInput // Trata casos como "2º (Segundo)"
      );
      break;

    case "SENTENCE_ORDER":
      const assembledSentence = Array.isArray(userInput) ? userInput.join(" ") : String(userInput);
      const normalizedSentence = normalizeText(assembledSentence, meta.ignoreAccents).replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"");
      isCorrect = exercise.respostasValidas.some(ans => 
        normalizeText(ans, meta.ignoreAccents).replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"") === normalizedSentence
      );
      break;

    case "SHADOW_PAIR":
      const selectedOption = normalizeText(String(userInput), meta.ignoreAccents);
      isCorrect = exercise.respostasValidas.some(ans => normalizeText(ans, meta.ignoreAccents) === selectedOption);
      break;
  }

  // Cálculo de Pontuação Ponderada
  const penalty = Math.max(0, (attempts - 1) * 15);
  const score = isCorrect ? Math.max(20, 100 - penalty) : 0;

  return {
    isCorrect,
    score,
    feedback: isCorrect ? "Excelente! Resposta correta." : "Tente novamente!",
    attemptsCount: attempts,
    timeSpentSeconds: timeSpent
  };
}
```

---

## 2. Catálogo Técnico Estruturado dos Exercícios

---

# BLOCO 1: 3 A 5 ANOS (Estimulação Sensório-Motora e Pré-Operatória)
*Total: 90 Exercícios (IDs 1 a 90)*

### 1.1 Categoria: Sombras e Pares (IDs 1 a 15)
*Engine: `SHADOW_PAIR` | Foco: Discriminação Visual, Atenção Sustentada e Emparelhamento Espacial.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **1** | Ligar a imagem da Maçã à sua sombra. | `["Sombra redonda com caule", "Sombra quadrada"]` | Sombra redonda com caule | `["Sombra redonda com caule"]` | Discriminação Visual |
| **2** | Ligar a Borboleta de asas abertas à sombra. | `["Sombra de asas abertas", "Sombra de asas fechadas"]` | Sombra de asas abertas | `["Sombra de asas abertas"]` | Emparelhamento Espacial |
| **3** | Ligar o Gato sentado à sua sombra. | `["Sombra de cão a correr", "Sombra de gato sentado"]` | Sombra de gato sentado | `["Sombra de gato sentado"]` | Atenção Sustentada |
| **4** | Ligar o Carro à sua sombra. | `["Sombra de bicicleta", "Sombra de veículo de 4 rodas"]` | Sombra de veículo de 4 rodas | `["Sombra de veículo de 4 rodas"]` | Identificação de Contornos |
| **5** | Ligar a Árvore à sua sombra. | `["Sombra de flor", "Sombra de tronco com copa"]` | Sombra de tronco com copa | `["Sombra de tronco com copa"]` | Raciocínio Espacial |
| **6** | Ligar o Sol à sua sombra. | `["Sombra circular com raios", "Sombra de nuvem"]` | Sombra circular com raios | `["Sombra circular com raios"]` | Discriminação Visual |
| **7** | Ligar a Estrela do mar à sombra. | `["Sombra de peixe", "Sombra com cinco pontas"]` | Sombra com cinco pontas | `["Sombra com cinco pontas"]` | Correspondência Geométrica |
| **8** | Ligar o Peixe à sua sombra. | `["Sombra oval com nadadeira", "Sombra redonda"]` | Sombra oval com nadadeira | `["Sombra oval com nadadeira"]` | Atenção ao Detalhe |
| **9** | Ligar a Casa à sua sombra. | `["Sombra retangular com teto", "Sombra de prédio"]` | Sombra retangular com teto | `["Sombra retangular com teto"]` | Emparelhamento Espacial |
| **10** | Ligar o Pato à sua sombra. | `["Sombra de ave com bico chato", "Sombra de águia"]` | Sombra de ave com bico chato | `["Sombra de ave com bico chato"]` | Reconhecimento de Forma |
| **11** | Ligar o Urso à sua sombra. | `["Sombra felpuda e redonda", "Sombra de cobra"]` | Sombra felpuda e redonda | `["Sombra felpuda e redonda"]` | Discriminação Visual |
| **12** | Ligar a Flor à sua sombra. | `["Sombra com caule e pétalas", "Sombra de folha"]` | Sombra com caule e pétalas | `["Sombra com caule e pétalas"]` | Correspondência Geométrica |
| **13** | Ligar a Nuvem à sua sombra. | `["Sombra irregular arredondada", "Sombra de lua"]` | Sombra irregular arredondada | `["Sombra irregular arredondada"]` | Percepção de Limites |
| **14** | Ligar o Lápis à sua sombra. | `["Sombra longa com ponta", "Sombra de livro"]` | Sombra longa com ponta | `["Sombra longa com ponta"]` | Atenção Sustentada |
| **15** | Ligar a Bola à sua sombra. | `["Sombra perfeitamente circular", "Sombra quadrada"]` | Sombra circular | `["Sombra perfeitamente circular", "Sombra circular"]` | Emparelhamento Espacial |

---

### 1.2 Categoria: O Que Não Pertence? (IDs 16 a 30)
*Engine: `INTRUDER_SELECTION` | Foco: Exclusão Categorial, Esquema Corporal e Classificação Semântica.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **16** | Qual não faz parte do grupo? Cachorro, Gato, Vaca, Sapato | `["Cachorro", "Gato", "Vaca", "Sapato"]` | Sapato (não é animal) | `["Sapato", "Sapato (não é animal)"]` | Exclusão por Categoria |
| **17** | Qual não faz parte do grupo? Maçã, Banana, Uva, Cadeira | `["Maçã", "Banana", "Uva", "Cadeira"]` | Cadeira (não é alimento) | `["Cadeira", "Cadeira (não é alimento)"]` | Raciocínio Dedutivo |
| **18** | Qual não faz parte do grupo? Carro, Ônibus, Bicicleta, Árvore | `["Carro", "Ônibus", "Bicicleta", "Árvore"]` | Árvore (não é veículo) | `["Árvore", "Árvore (não é veículo)"]` | Classificação Semântica |
| **19** | Qual não faz parte do grupo? Camisa, Calça, Meia, Caderno | `["Camisa", "Calça", "Meia", "Caderno"]` | Caderno (não é roupa) | `["Caderno", "Caderno (não é roupa)"]` | Exclusão Lógica |
| **20** | Qual não faz parte do grupo? Lápis, Borracha, Caderno, Garfo | `["Lápis", "Borracha", "Caderno", "Garfo"]` | Garfo (não é material escolar) | `["Garfo", "Garfo (não é material escolar)"]` | Organização Conceptual |
| **21** | Qual não faz parte do grupo? Cama, Sofá, Mesa, Sol | `["Cama", "Sofá", "Mesa", "Sol"]` | Sol (não é móvel de casa) | `["Sol", "Sol (não é móvel de casa)"]` | Categorização Ambiental |
| **22** | Qual não faz parte do grupo? Azul, Vermelho, Amarelo, Cachorro | `["Azul", "Vermelho", "Amarelo", "Cachorro"]` | Cachorro (não é cor) | `["Cachorro", "Cachorro (não é cor)"]` | Exclusão por Atributo |
| **23** | Qual não faz parte do grupo? Olho, Nariz, Boca, Bola | `["Olho", "Nariz", "Boca", "Bola"]` | Bola (não é parte do corpo) | `["Bola", "Bola (não é parte do corpo)"]` | Esquema Corporal |
| **24** | Qual não faz parte do grupo? Sol, Nuvem, Estrela, Cama | `["Sol", "Nuvem", "Estrela", "Cama"]` | Cama (não fica no céu) | `["Cama", "Cama (não fica no céu)"]` | Raciocínio Dedutivo |
| **25** | Qual não faz parte do grupo? Copo, Prato, Colher, Gato | `["Copo", "Prato", "Colher", "Gato"]` | Gato (não é utensílio) | `["Gato", "Gato (não é utensílio)"]` | Classificação Semântica |
| **26** | Qual não faz parte do grupo? Formiga, Abelha, Borboleta, Elefante | `["Formiga", "Abelha", "Borboleta", "Elefante"]` | Elefante (não é inseto) | `["Elefante", "Elefante (não é inseto)"]` | Comparação de Tamanhos |
| **27** | Qual não faz parte do grupo? Água, Suco, Leite, Pão | `["Água", "Suco", "Leite", "Pão"]` | Pão (não é líquido) | `["Pão", "Pão (não é líquido)"]` | Diferenciação de Estado |
| **28** | Qual não faz parte do grupo? Mão, Pé, Braço, Chapéu | `["Mão", "Pé", "Braço", "Chapéu"]` | Chapéu (não é do corpo) | `["Chapéu", "Chapéu (não é do corpo)"]` | Esquema Corporal |
| **29** | Qual não faz parte do grupo? Violão, Tambor, Flauta, Maçã | `["Violão", "Tambor", "Flauta", "Maçã"]` | Maçã (não faz música) | `["Maçã", "Maçã (não faz música)"]` | Exclusão Lógica |
| **30** | Qual não faz parte do grupo? Escova, Sabonete, Shampoo, Bicicleta | `["Escova", "Sabonete", "Shampoo", "Bicicleta"]` | Bicicleta (não é higiene) | `["Bicicleta", "Bicicleta (não é higiene)"]` | Organização Conceptual |

---

### 1.3 Categoria: Categorização Simples (IDs 31 a 45)
*Engine: `SINGLE_CHOICE` | Foco: Funções dos Objetos, Habitats, Sensações e Conhecimento Geral.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **31** | Qual destes animais vive na água? | `["Gato", "Peixe", "Pássaro"]` | Peixe | `["Peixe"]` | Associação de Habitat |
| **32** | Qual objeto usamos para dormir? | `["Cadeira", "Cama", "Mesa"]` | Cama | `["Cama"]` | Função de Objetos |
| **33** | Qual destes alimentos é uma fruta? | `["Cenoura", "Maçã", "Alface"]` | Maçã | `["Maçã"]` | Reconhecimento Alimentar |
| **34** | Qual destes animais sabe voar? | `["Pássaro", "Cachorro", "Tartaruga"]` | Pássaro | `["Pássaro"]` | Associação de Movimento |
| **35** | O que vestimos nos nossos pés? | `["Luva", "Chapéu", "Sapato"]` | Sapato | `["Sapato"]` | Esquema Corporal |
| **36** | O que ilumina e aquece o nosso dia? | `["Lua", "Sol", "Estrela"]` | Sol | `["Sol"]` | Conhecimento Geral |
| **37** | Qual destes animais é muito grande? | `["Formiga", "Elefante", "Joaninha"]` | Elefante | `["Elefante"]` | Noção de Grandeza |
| **38** | O que usamos quando está a chover? | `["Guarda-chuva", "Óculos de sol", "Chinelo"]` | Guarda-chuva | `["Guarda-chuva"]` | Relação Causa-Efeito |
| **39** | Que animal nos fornece o leite? | `["Vaca", "Galinha", "Sapo"]` | Vaca | `["Vaca"]` | Associação de Origem |
| **40** | Que objeto usamos para desenhar? | `["Borracha", "Lápis", "Régua"]` | Lápis | `["Lápis"]` | Função de Objetos |
| **41** | Qual destes animais anda muito devagar? | `["Cavalo", "Leopardo", "Tartaruga"]` | Tartaruga | `["Tartaruga"]` | Noção de Velocidade |
| **42** | O que usamos na nossa cabeça? | `["Chapéu", "Meia", "Cinto"]` | Chapéu | `["Chapéu"]` | Esquema Corporal |
| **43** | Qual destes alimentos tem um sabor doce? | `["Limão", "Bolo", "Sal"]` | Bolo | `["Bolo"]` | Discriminação Sensorial |
| **44** | Onde guardamos a nossa roupa? | `["Geladeira", "Guarda-roupa", "Fogão"]` | Guarda-roupa | `["Guarda-roupa"]` | Orientação Espacial/Função |
| **45** | Qual destes animais faz 'Miau'? | `["Cachorro", "Pato", "Gato"]` | Gato | `["Gato"]` | Associação Sonora |

---

### 1.4 Categoria: Sequências Visuais (IDs 46 a 60)
*Engine: `NUMERIC_SEQUENCE` / `SINGLE_CHOICE` | Foco: Padrões Algorítmicos, Memória de Trabalho e Alternância.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **46** | Complete: Círculo, Quadrado, Círculo, Quadrado... | `["Círculo", "Triângulo"]` | Círculo | `["Círculo"]` | Reconhecimento de Padrões |
| **47** | Complete: Sol, Lua, Sol, Lua... | `["Estrela", "Sol"]` | Sol | `["Sol"]` | Pensamento Algorítmico |
| **48** | Complete: Gato, Cão, Gato, Cão... | `["Gato", "Pato"]` | Gato | `["Gato"]` | Memória de Trabalho |
| **49** | Complete: Vermelho, Azul, Vermelho, Azul... | `["Amarelo", "Vermelho"]` | Vermelho | `["Vermelho"]` | Sequenciação Cromática |
| **50** | Complete: Grande, Pequeno, Grande, Pequeno... | `["Grande", "Médio"]` | Grande | `["Grande"]` | Relação de Proporção |
| **51** | Complete: Flor, Borboleta, Flor, Borboleta... | `["Flor", "Árvore"]` | Flor | `["Flor"]` | Reconhecimento de Padrões |
| **52** | Complete: Maçã, Banana, Maçã, Banana... | `["Laranja", "Maçã"]` | Maçã | `["Maçã"]` | Memória de Curto Prazo |
| **53** | Complete: Estrela, Círculo, Estrela, Círculo... | `["Estrela", "Quadrado"]` | Estrela | `["Estrela"]` | Pensamento Algorítmico |
| **54** | Complete: Sapo, Peixe, Sapo, Peixe... | `["Sapo", "Cobra"]` | Sapo | `["Sapo"]` | Sequenciação Lógica |
| **55** | Complete: Dia, Noite, Dia, Noite... | `["Dia", "Tarde"]` | Dia | `["Dia"]` | Ciclos Naturais |
| **56** | Complete: Triângulo, Quadrado, Triângulo... | `["Círculo", "Quadrado"]` | Quadrado | `["Quadrado"]` | Memória Visual |
| **57** | Complete: Pássaro, Ninho, Pássaro, Ninho... | `["Pássaro", "Ovo"]` | Pássaro | `["Pássaro"]` | Reconhecimento de Padrões |
| **58** | Complete: Lápis, Papel, Lápis, Papel... | `["Lápis", "Borracha"]` | Lápis | `["Lápis"]` | Pensamento Sequencial |
| **59** | Complete: Mão, Pé, Mão, Pé... | `["Braço", "Mão"]` | Mão | `["Mão"]` | Esquema Corporal em Série |
| **60** | Complete: Carro, Moto, Carro, Moto... | `["Carro", "Barco"]` | Carro | `["Carro"]` | Atenção Alternada |

---

### 1.5 Categoria: Quem Sou Eu? (IDs 61 a 75)
*Engine: `SINGLE_CHOICE` | Foco: Dedução Simples, Associação Sensorial e Memória Semântica.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **61** | Tenho uma tromba comprida e sou muito pesado. | `["Elefante", "Macaco"]` | Elefante | `["Elefante"]` | Dedução Simples |
| **62** | Sou amarelo, brilho no céu e aqueço o dia. | `["Lua", "Sol"]` | Sol | `["Sol"]` | Conhecimento do Mundo |
| **63** | Tenho quatro patas e adoro ladrar. | `["Gato", "Cão"]` | Cão | `["Cão"]` | Associação Auditivo-Visual |
| **64** | Sou vermelha e doce. A Branca de Neve comeu-me. | `["Laranja", "Maçã"]` | Maçã | `["Maçã"]` | Memória Semântica |
| **65** | Tenho quatro rodas e levo-te a passear. | `["Avião", "Carro"]` | Carro | `["Carro"]` | Associação Funcional |
| **66** | Vivo na água e nado com nadadeiras. | `["Pato", "Peixe"]` | Peixe | `["Peixe"]` | Conhecimento Ambiental |
| **67** | Sou macio e apoias a cabeça em mim para dormir. | `["Livro", "Travesseiro"]` | Travesseiro | `["Travesseiro"]` | Utilidade Diária |
| **68** | Voo pelas flores e antes era uma lagarta. | `["Abelha", "Borboleta"]` | Borboleta | `["Borboleta"]` | Dedução Simples |
| **69** | Caio das nuvens e molho a rua toda. | `["Neve", "Chuva"]` | Chuva | `["Chuva"]` | Conhecimento Natural |
| **70** | Sou verde por fora, vermelha por dentro. | `["Maçã", "Melancia"]` | Melancia | `["Melancia"]` | Discriminação de Cor/Fruta |
| **71** | Dou leite, como erva e faço "Muuu". | `["Ovelha", "Vaca"]` | Vaca | `["Vaca"]` | Dedução Sensorial |
| **72** | Tenho dentes mas não mordo. Arrumo o teu cabelo. | `["Escova de dentes", "Pente"]` | Pente | `["Pente"]` | Pensamento Metafórico Simples |
| **73** | Sou muito comprida e rastejo pelo chão. | `["Minhoca", "Cobra"]` | Cobra | `["Cobra"]` | Associação de Movimento |
| **74** | Tenho duas rodas e precisas de te equilibrar em mim. | `["Carro", "Bicicleta"]` | Bicicleta | `["Bicicleta"]` | Utilidade de Transporte |
| **75** | Sou gelado e derreto se não me comeres rápido. | `["Bolo", "Gelado"]` | Gelado | `["Gelado"]` | Relação Térmica |

---

### 1.6 Categoria: Associação Utilidade (IDs 76 a 90)
*Engine: `SINGLE_CHOICE` | Foco: Causa-Efeito, Cuidados Pessoais, Rotinas e Instrumentalidade.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **76** | Com que objeto a Chave faz par? | `["Cadeado", "Livro", "Garfo"]` | Cadeado | `["Cadeado"]` | Causa e Efeito |
| **77** | O que a Escova de dentes limpa? | `["Cabelo", "Dente", "Sapato"]` | Dente | `["Dente"]` | Higiene Pessoal |
| **78** | O que comemos com a Colher? | `["Sopa", "Pão", "Maçã"]` | Sopa | `["Sopa"]` | Funcionalidade |
| **79** | O que o Regador molha? | `["Computador", "Planta", "Cama"]` | Planta | `["Planta"]` | Ação e Objeto Alvo |
| **80** | O que usamos juntamente com o Pincel? | `["Tinta", "Sabão", "Terra"]` | Tinta | `["Tinta"]` | Emparelhamento de Materiais |
| **81** | O que colocamos no Prato? | `["Comida", "Roupa", "Brinquedo"]` | Comida | `["Comida"]` | Rotinas Diárias |
| **82** | O que a Tesoura corta? | `["Papel", "Água", "Pedra"]` | Papel | `["Papel"]` | Ferramenta e Material |
| **83** | O que usamos para varrer o Chão? | `["Pente", "Vassoura", "Garfo"]` | Vassoura | `["Vassoura"]` | Limpeza |
| **84** | Onde batemos com o Martelo? | `["Prego", "Vidro", "Almofada"]` | Prego | `["Prego"]` | Causa e Efeito |
| **85** | O que bebemos na Chávena? | `["Leite/Café", "Areia", "Tinta"]` | Leite/Café | `["Leite/Café", "Leite", "Café"]` | Recipientes e Conteúdos |
| **86** | O que limpamos com o Sabonete? | `["Corpo", "Carro", "Parede"]` | Corpo | `["Corpo"]` | Cuidados Pessoais |
| **87** | Onde escrevemos com o Lápis? | `["Papel", "Espelho", "Casca"]` | Papel | `["Papel"]` | Associação de Utilidade |
| **88** | Onde penduramos o Cabide? | `["Guarda-roupa", "Frigorífico"]` | Guarda-roupa | `["Guarda-roupa"]` | Organização Espacial |
| **89** | O que usamos para proteger os Olhos do sol? | `["Chapéu", "Óculos de Sol"]` | Óculos de Sol | `["Óculos de Sol", "Óculos de sol"]` | Proteção e Função |
| **90** | O que guardamos dentro da Mochila? | `["Livros e Cadernos", "Água"]` | Livros e Cadernos | `["Livros e Cadernos"]` | Relação Continente/Conteúdo |

---

# BLOCO 2: 6 A 10 ANOS (Segunda Infância - Alfabetização e Lógica Concreta)
*Total: 90 Exercícios (IDs 91 a 180)*

### 2.1 Categoria: Palavras Embaralhadas (IDs 91 a 105)
*Engine: `ANAGRAM_ORDER` | Foco: Consciência Fonológica, Manipulação Silábica e Flexibilidade Lexical.*

| ID | Prompt | Letras Fornecidas | Resposta Esperada | Gabarito Técnico (Múltiplas Soluções) | Competência Alvo |
|---|---|---|---|---|---|
| **91** | Desembaralhe as letras para formar a palavra: O B L O | `["O", "B", "L", "O"]` | BOLO (ou LOBO) | `["BOLO", "LOBO"]` | Planeamento Lexical |
| **92** | Desembaralhe as letras: A S C A | `["A", "S", "C", "A"]` | CASA (ou SACA) | `["CASA", "SACA"]` | Flexibilidade Ortográfica |
| **93** | Desembaralhe as letras: M O A R | `["M", "O", "A", "R"]` | AMOR | `["AMOR", "ROMA", "RAMO", "MORA"]` | Atenção e Reorganização |
| **94** | Desembaralhe as letras: T G A O | `["T", "G", "A", "O"]` | GATO | `["GATO", "TOGA"]` | Acesso Lexical |
| **95** | Desembaralhe as letras: D V I A | `["D", "V", "I", "A"]` | VIDA | `["VIDA", "DIVA"]` | Descodificação Visual |
| **96** | Desembaralhe as letras: Z A U L | `["Z", "A", "U", "L"]` | AZUL | `["AZUL"]` | Ortografia Básica |
| **97** | Desembaralhe as letras: V ÃO O A | `["V", "ÃO", "O", "A"]` | AVIÃO | `["AVIÃO"]` | Consciência Fonológica |
| **98** | Desembaralhe as letras: R O R R Á V E | `["R", "O", "R", "R", "Á", "V", "E"]` | ÁRVORE | `["ÁRVORE"]` | Manipulação Silábica |
| **99** | Desembaralhe as letras: L ÃO O I V | `["L", "ÃO", "O", "I", "V"]` | VIOLÃO | `["VIOLÃO"]` | Planeamento Lexical |
| **100** | Desembaralhe as letras: F G O O | `["F", "G", "O", "O"]` | FOGO | `["FOGO"]` | Atenção Visual |
| **101** | Desembaralhe as letras: R A T O | `["R", "A", "T", "O"]` | RATO (ou TORA) | `["RATO", "TORA", "ROTA"]` | Descodificação Flexível |
| **102** | Desembaralhe as letras: G A O L | `["G", "A", "O", "L"]` | LAGO (ou GOLA) | `["LAGO", "GOLA", "GALO"]` | Combinação Lexical |
| **103** | Desembaralhe as letras: B ÃO S A | `["B", "ÃO", "S", "A"]` | SABÃO | `["SABÃO"]` | Construção Ortográfica |
| **104** | Desembaralhe as letras: C M A A | `["C", "M", "A", "A"]` | CAMA (ou MACA) | `["CAMA", "MACA"]` | Organização Cognitiva |
| **105** | Desembaralhe as letras: I O R | `["I", "O", "R"]` | RIO | `["RIO"]` | Raciocínio Espacial |

---

### 2.2 Categoria: Qual Letra Falta? (IDs 106 a 120)
*Engine: `GAP_FILL` | Foco: Dígrafos, Ditongos, Encontros Consonânticos e Memória Ortográfica.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **106** | C A C H O _ R O | `["R", "M", "P"]` | R | `["R"]` | Ortografia de Dígrafos |
| **107** | P A S S A _ I N H O | `["R", "S", "T"]` | R | `["R"]` | Discriminação Fonológica |
| **108** | E S T _ E L A | `["P", "R", "M"]` | R | `["R"]` | Estruturas Consonânticas |
| **109** | B I _ I C L E T A | `["S", "C", "Z"]` | C | `["C"]` | Regras Ortográficas (C/S) |
| **110** | C _ V A L O | `["O", "A", "E"]` | A | `["A"]` | Identificação Vocálica |
| **111** | M O _ I L A | `["X", "CH", "G"]` | CH | `["CH"]` | Ortografia Complexa (X/CH) |
| **112** | T A _ T A R U G A | `["R", "L", "S"]` | R | `["R"]` | Final de Sílaba |
| **113** | G I R _ F A | `["E", "A", "O"]` | A | `["A"]` | Reconhecimento Lexical |
| **114** | F E _ J ÃO | `["I", "E", "U"]` | I | `["I"]` | Ditongos |
| **115** | E S C _ L A | `["O", "A", "U"]` | O | `["O"]` | Memória Ortográfica |
| **116** | B O _ E C A | `["M", "N", "P"]` | N | `["N"]` | Consciência Fonológica |
| **117** | M A _ A C O | `["C", "S", "Z"]` | C | `["C"]` | Discriminação Visual |
| **118** | T E L E _ I S ÃO | `["F", "V", "M"]` | V | `["V"]` | Associação Som/Letra |
| **119** | L _ R A N J A | `["O", "A", "E"]` | A | `["A"]` | Reconhecimento Lexical |
| **120** | S A P A _ O | `["P", "T", "C"]` | T | `["T"]` | Fecho Ortográfico |

---

### 2.3 Categoria: Verdadeiro ou Falso (IDs 121 a 135)
*Engine: `TRUE_FALSE` | Foco: Conhecimento Científico, Geometria, Proporções e Geografia.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **121** | As vacas fornecem-nos o leite. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Conhecimento Geral |
| **122** | O sol brilha intensamente durante a noite. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Lógica e Ciclos |
| **123** | Os peixes conseguem respirar fora de água. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Ciências da Natureza |
| **124** | O gelo é feito de água que congelou. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Estados da Matéria |
| **125** | Um triângulo possui quatro lados. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Geometria Básica |
| **126** | As formigas são animais maiores que os elefantes. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Noção de Proporção |
| **127** | O número 5 representa uma quantidade maior que o 2. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Valor Numérico |
| **128** | Os pássaros constroem ninhos para os seus ovos. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Conhecimento Ambiental |
| **129** | O mês de dezembro é o último mês do ano. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Orientação Temporal |
| **130** | A maçã é uma fruta que tem a cor azul. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Memória Semântica |
| **131** | Um dia completo tem 24 horas. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Noção de Tempo |
| **132** | Lisboa é a capital de Espanha. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Geografia Básica |
| **133** | O inverno é a estação mais quente de todo o ano. | `["Verdadeiro", "Falso"]` | Falso | `["Falso", "F", "False"]` | Ciclos Climáticos |
| **134** | A cor do céu num dia limpo e ensolarado é azul. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Percepção Ambiental |
| **135** | A lagarta transforma-se numa borboleta. | `["Verdadeiro", "Falso"]` | Verdadeiro | `["Verdadeiro", "V", "True"]` | Biologia Simples |

---

### 2.4 Categoria: Problemas Lógicos (IDs 136 a 150)
*Engine: `SINGLE_CHOICE` | Foco: Operações Aritméticas Concretas, Frações, Moeda e Tempo.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **136** | O João tinha 3 maçãs. Ganhou mais 2. Quantas tem? | `["4", "5", "6"]` | 5 | `["5"]` | Adição Simples |
| **137** | A Maria tinha 5 euros, gastou 2 euros. Quanto sobrou? | `["3", "4", "7"]` | 3 | `["3"]` | Subtração Simples |
| **138** | Numa caixa cabem 6 lápis. Estão lá 4. Faltam quantos? | `["1", "2", "3"]` | 2 | `["2"]` | Complemento Numérico |
| **139** | Um cão tem 4 patas. Dois cães juntos têm quantas? | `["6", "8", "10"]` | 8 | `["8"]` | Multiplicação Básica |
| **140** | Se hoje é terça-feira, que dia será amanhã? | `["Segunda", "Quarta"]` | Quarta | `["Quarta"]` | Orientação Temporal |
| **141** | Tenho 10 cromos. Dei 5 ao amigo. Com quantos fiquei? | `["4", "5", "15"]` | 5 | `["5"]` | Subtração Simples |
| **142** | Uma bicicleta tem 2 rodas. E 3 bicicletas? | `["5", "6", "8"]` | 6 | `["6"]` | Multiplicação Básica |
| **143** | O Pedro tem 7 anos. A irmã tem 9. Quem é mais velho? | `["Pedro", "Irmã"]` | Irmã | `["Irmã"]` | Comparação Numérica |
| **144** | Num aquário havia 8 peixes. 3 fugiram. Quantos ficaram? | `["5", "11", "4"]` | 5 | `["5"]` | Lógica de Subtração |
| **145** | Uma piza foi cortada em 4 fatias. Comi 1. Sobraram? | `["2", "3", "4"]` | 3 | `["3"]` | Fração/Subtração |
| **146** | Tenho duas notas de 5 euros. Quantos euros tenho? | `["5", "10", "20"]` | 10 | `["10"]` | Valor do Dinheiro |
| **147** | Um inseto tem 6 pernas. Perdeu 1. Com quantas ficou? | `["5", "7", "4"]` | 5 | `["5"]` | Subtração Concreta |
| **148** | Uma mão tem 5 dedos. Duas mãos têm quantos? | `["5", "10", "15"]` | 10 | `["10"]` | Dobro Matemático |
| **149** | O Lucas dormiu às 20h e dormiu 10 horas. Acordou às? | `["5h", "6h", "7h"]` | 6h | `["6h", "6"]` | Cálculo de Tempo |
| **150** | Havia 7 pássaros na árvore. Chegaram mais 4. Total? | `["10", "11", "12"]` | 11 | `["11"]` | Adição Simples |

---

### 2.5 Categoria: Intruso Complexo (IDs 151 a 165)
*Engine: `INTRUDER_SELECTION` | Foco: Abstração Categorial, Propriedades Físicas e Hierarquia Semântica.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **151** | Martelo, Serrote, Alicate, Maçã | `["Martelo", "Serrote", "Alicate", "Maçã"]` | Maçã (não é ferramenta) | `["Maçã", "Maçã (não é ferramenta)"]` | Exclusão Abstrata |
| **152** | Carro, Mota, Comboio, Avião | `["Carro", "Mota", "Comboio", "Avião"]` | Avião (não anda no solo) | `["Avião", "Avião (não anda no solo)"]` | Categorização de Transporte |
| **153** | Natação, Futebol, Basquete, Voleibol | `["Natação", "Futebol", "Basquete", "Voleibol"]` | Natação (sem bola) | `["Natação", "Natação (sem bola)"]` | Classificação Desportiva |
| **154** | Violão, Violino, Bateria, Guitarra | `["Violão", "Violino", "Bateria", "Guitarra"]` | Bateria (sem cordas) | `["Bateria", "Bateria (sem cordas)"]` | Propriedades Físicas |
| **155** | Médico, Professor, Mesa, Bombeiro | `["Médico", "Professor", "Mesa", "Bombeiro"]` | Mesa (não é profissão) | `["Mesa", "Mesa (não é profissão)"]` | Organização Semântica |
| **156** | Tubarão, Baleia, Golfinho, Águia | `["Tubarão", "Baleia", "Golfinho", "Águia"]` | Águia (não é marinho) | `["Águia", "Águia (não é marinho)"]` | Classificação Habitacional |
| **157** | Portugal, Espanha, Europa, França | `["Portugal", "Espanha", "Europa", "França"]` | Europa (continente) | `["Europa", "Europa (continente)"]` | Geografia Complexa |
| **158** | Camisa, Casaco, Meia, Guarda-chuva | `["Camisa", "Casaco", "Meia", "Guarda-chuva"]` | Guarda-chuva (não vestuário) | `["Guarda-chuva", "Guarda-chuva (não vestuário)"]` | Funcionalidade |
| **159** | Tristeza, Raiva, Mesa, Alegria | `["Tristeza", "Raiva", "Mesa", "Alegria"]` | Mesa (não é emoção) | `["Mesa", "Mesa (não é emoção)"]` | Abstração Emocional |
| **160** | Olhos, Nariz, Boca, Joelho | `["Olhos", "Nariz", "Boca", "Joelho"]` | Joelho (não no rosto) | `["Joelho", "Joelho (não no rosto)"]` | Anatomia e Agrupamento |
| **161** | Primavera, Verão, Chuva, Outono | `["Primavera", "Verão", "Chuva", "Outono"]` | Chuva (não é estação) | `["Chuva", "Chuva (não é estação)"]` | Fenómenos Climáticos |
| **162** | Janeiro, Terça-feira, Março, Abril | `["Janeiro", "Terça-feira", "Março", "Abril"]` | Terça-feira (dia) | `["Terça-feira", "Terça-feira (dia)"]` | Calendário e Estrutura |
| **163** | Ouro, Prata, Ferro, Algodão | `["Ouro", "Prata", "Ferro", "Algodão"]` | Algodão (não é metal) | `["Algodão", "Algodão (não é metal)"]` | Propriedades da Matéria |
| **164** | Pato, Galinha, Peru, Leão | `["Pato", "Galinha", "Peru", "Leão"]` | Leão (não é ave/bota ovo) | `["Leão", "Leão (não é ave/bota ovo)"]` | Categorização Animal |
| **165** | Português, Matemática, Ciências, Recreio | `["Português", "Matemática", "Ciências", "Recreio"]` | Recreio (não é disciplina) | `["Recreio", "Recreio (não é disciplina)"]` | Conceitos Escolares |

---

### 2.6 Categoria: Mania de Letra (IDs 166 a 180)
*Engine: `SINGLE_CHOICE` | Foco: Evocação Condicionada (Letra Inicial + Restrição Semântica).*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **166** | Letra A + Animal | `["Abelha", "Bolo", "Árvore"]` | Abelha | `["Abelha"]` | Memória de Evocação |
| **167** | Letra B + Cor | `["Banana", "Branco", "Brinco"]` | Branco | `["Branco"]` | Associação Condicionada |
| **168** | Letra C + Móvel de Casa | `["Cama", "Cão", "Cebola"]` | Cama | `["Cama"]` | Filtragem Cognitiva |
| **169** | Letra M + Fruta | `["Mesa", "Macaco", "Maçã"]` | Maçã | `["Maçã"]` | Flexibilidade Lexical |
| **170** | Letra P + País | `["Porta", "Portugal", "Parede"]` | Portugal | `["Portugal"]` | Geografia e Letra Inicial |
| **171** | Letra V + Cor | `["Vidro", "Vermelho", "Vaca"]` | Vermelho | `["Vermelho"]` | Evocação por Categoria |
| **172** | Letra G + Animal | `["Gato", "Gota", "Gelo"]` | Gato | `["Gato"]` | Organização Semântica |
| **173** | Letra E + Animal muito grande | `["Elefante", "Escova", "Estrela"]` | Elefante | `["Elefante"]` | Associação Múltipla |
| **174** | Letra J + Animal selvagem | `["Janela", "Jacaré", "Jogo"]` | Jacaré | `["Jacaré"]` | Filtragem Lexical |
| **175** | Letra T + Fruta/Legume vermelho | `["Tatu", "Tomate", "Telhado"]` | Tomate | `["Tomate"]` | Associação de Propriedades |
| **176** | Letra S + Calçado | `["Sol", "Sapato", "Sabão"]` | Sapato | `["Sapato"]` | Acesso ao Vocabulário |
| **177** | Letra L + Fruta ácida/azeda | `["Lápis", "Limão", "Lata"]` | Limão | `["Limão"]` | Evocação Sensorial |
| **178** | Letra U + Fruta de cacho | `["Urso", "Uva", "Unha"]` | Uva | `["Uva"]` | Categoria Específica |
| **179** | Letra O + Parte do rosto | `["Olho", "Ovo", "Onda"]` | Olho | `["Olho"]` | Vocabulário Anatómico |
| **180** | Letra D + Número | `["Dado", "Dez", "Dedo"]` | Dez | `["Dez"]` | Raciocínio Matemático |

---

# BLOCO 3: 11+ ANOS (Operações Formais e Abstratas)
*Total: 90 Exercícios (IDs 181 a 270)*

### 3.1 Categoria: Pensamento Lateral (IDs 181 a 195)
*Engine: `SINGLE_CHOICE` | Foco: Raciocínio Analógico, Paradoxo, Metalinguagem e Metáforas.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **181** | Tem dentes, não morde e ajuda no teu dia a dia. | `["Pente", "Tubarão", "Serra"]` | Pente | `["Pente"]` | Raciocínio Analógico |
| **182** | Quanto mais tiras de mim, maior eu fico. O que sou? | `["Dinheiro", "Buraco", "Pão"]` | Buraco | `["Buraco"]` | Flexibilidade Cognitiva |
| **183** | O que anda sem pés e voa sem asas? | `["Pássaro", "Tempo/Nuvem"]` | Tempo / Nuvem | `["Tempo/Nuvem", "Tempo", "Nuvem"]` | Pensamento Metafórico |
| **184** | Cheio de furos, mas consegue reter muita água. | `["Rede", "Esponja", "Peneira"]` | Esponja | `["Esponja"]` | Contradição Lógica |
| **185** | Tem cidades sem casas, rios sem água e florestas sem árvores. | `["Mapa", "Globo", "Planeta"]` | Mapa | `["Mapa"]` | Abstração Espacial |
| **186** | Podes quebrar-me apenas falando o meu nome. | `["Vidro", "Silêncio", "Segredo"]` | Silêncio | `["Silêncio"]` | Metacognição |
| **187** | Sou de todos, ninguém me prende. Formo a praia. | `["Água", "Vento", "Areia"]` | Areia | `["Areia"]` | Associação Conceptual |
| **188** | Tenho pescoço, não tenho cabeça. Tenho corpo, não tenho braços. | `["Garrafa", "Camisa", "Árvore"]` | Garrafa | `["Garrafa"]` | Antropomorfismo Físico |
| **189** | O que sempre cai, mas nunca se aleija? | `["Pedra", "Chuva/Noite"]` | Chuva | `["Chuva", "Chuva/Noite", "Noite"]` | Desconstrução de Verbos |
| **190** | Nasço grande e morro pequeno. O que sou? | `["Humano", "Lápis/Vela"]` | Lápis / Vela | `["Lápis/Vela", "Lápis", "Vela"]` | Raciocínio Inverso |
| **191** | Quem faz não quer; quem compra não usa; quem usa não vê. | `["Cama", "Roupa", "Caixão"]` | Caixão | `["Caixão"]` | Dedução Social Paradoxal |
| **192** | O que entra na água e não se molha? | `["Barco", "Sombra", "Peixe"]` | Sombra | `["Sombra"]` | Fenómenos Óticos/Físicos |
| **193** | Palavra sempre escrita incorretamente no dicionário. | `["Incorretamente", "Errado"]` | Incorretamente | `["Incorretamente"]` | Metalinguagem |
| **194** | Pertence-te, mas as outras pessoas usam mais do que tu. | `["Telefone", "O teu nome"]` | O teu nome | `["O teu nome", "Nome"]` | Convenções Sociais |
| **195** | Quanto mais seca com ela, mais molhada ela fica. | `["Água", "Toalha", "Areia"]` | Toalha | `["Toalha"]` | Dedução Funcional |

---

### 3.2 Categoria: Polissemia (IDs 196 a 210)
*Engine: `SINGLE_CHOICE` | Foco: Ambiguidade Lexical, Sentido Figurado vs Literal e Contexto.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **196** | 1. Fruta. / 2. A camisa tem uma ___ curta. | `["Manga", "Gola"]` | Manga | `["Manga"]` | Sentido Figurado e Literal |
| **197** | 1. Sentar na praça. / 2. Depositar dinheiro. | `["Cadeira", "Banco"]` | Banco | `["Banco"]` | Ambiguidade Lexical |
| **198** | 1. O relógio parou sem ___. / 2. Instrumento musical. | `["Bateria", "Corda"]` | Bateria | `["Bateria"]` | Flexibilidade Semântica |
| **199** | 1. ___ de raciocínio. / 2. Costurar com agulha e ___. | `["Fio", "Linha"]` | Linha | `["Linha"]` | Reconhecimento Lexical |
| **200** | 1. Parar de autocarro. / 2. ___ final no texto. | `["Estação", "Ponto"]` | Ponto | `["Ponto"]` | Adaptação de Contexto |
| **201** | 1. Um ___ de alho. / 2. Fica dentro da boca. | `["Pedaço", "Dente"]` | Dente | `["Dente"]` | Generalização de Conceitos |
| **202** | 1. A aranha teceu-a. / 2. ___ Mundial de Computadores. | `["Rede/Teia", "Fio"]` | Rede | `["Rede", "Rede/Teia"]` | Polissemia Moderna |
| **203** | 1. Caiu da árvore. / 2. Escrever na ___ do caderno. | `["Folha", "Letra"]` | Folha | `["Folha"]` | Múltiplos Significados |
| **204** | 1. Trancar a porta. / 2. A ___ da charada ou enigma. | `["Fechadura", "Chave"]` | Chave | `["Chave"]` | Abstração Metáforica |
| **205** | 1. A água a ferver está ___. / 2. A notícia do dia. | `["Quente", "Fria"]` | Quente | `["Quente"]` | Contexto Informal |
| **206** | 1. A tartaruga escondeu-se. / 2. O ___ do navio. | `["Casco", "Escudo"]` | Casco | `["Casco"]` | Vocabulário Complexo |
| **207** | 1. O rei e a rainha governam a ___. / 2. Ferida, rasgão. | `["Corte", "País"]` | Corte | `["Corte"]` | Polissemia Histórica |
| **208** | 1. O pássaro tem-nas. / 2. Ter ___ de alguém a chorar. | `["Pena", "Asas"]` | Pena | `["Pena"]` | Emoção vs Objeto Físico |
| **209** | 1. Pular a ___ do vizinho. / 2. Usar nas janelas contra insetos. | `["Rede", "Muro"]` | Rede | `["Rede"]` | Discriminação Funcional |
| **210** | 1. Da camisa. / 2. Rosa abriu em ___. | `["Botão", "Fio"]` | Botão | `["Botão"]` | Analogia Botânica/Física |

---

### 3.3 Categoria: Dedução Lógica (IDs 211 a 225)
*Engine: `SINGLE_CHOICE` | Foco: Silogismos, Ordenação Transitiva, Paradoxo e Eliminação.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **211** | Ana > Bia. Bia > Carla. Quem é a mais baixa? | `["Ana", "Bia", "Carla"]` | Carla | `["Carla"]` | Ordenação Transitiva |
| **212** | M=Verde. J detesta vermelho. Qual é a de Pedro (V/A/Az)? | `["Vermelho", "Azul", "Verde"]` | Vermelho | `["Vermelho"]` | Eliminação Pura |
| **213** | Se todo o gato mia, e Rex não mia, Rex é gato? | `["Sim", "Não"]` | Não | `["Não"]` | Silogismo Básico |
| **214** | Todos os alunos gostam de ler. Tiago é aluno. Gosta de ler? | `["Sim", "Não"]` | Sim | `["Sim"]` | Lógica Dedutiva Afirmativa |
| **215** | Carro C > Carro A > Carro B (Velocidade). Qual o mais lento? | `["Carro A", "Carro B", "C"]` | Carro B | `["Carro B"]` | Comparação Sucessiva |
| **216** | Gaveta 1 = Facas. Gaveta 2 = Vazia. Gaveta 3 = Colheres. Corta? | `["1", "2", "3"]` | 1 (Superior) | `["1", "1 (Superior)"]` | Raciocínio de Associação |
| **217** | Lucas mora à Esq. de Felipe e Dir. de Bruno. Ordem? | `["B-F-L", "B-L-F", "L-B-F"]` | Bruno-Lucas-Felipe | `["B-L-F", "Bruno-Lucas-Felipe"]` | Posicionamento Espacial |
| **218** | Ultrapassaste o 2º lugar. Ficas em qual posição? | `["1º", "2º", "3º"]` | 2º (Segundo) | `["2º", "2º (Segundo)", "2"]` | Inibição Impulsiva |
| **219** | Quando chove, a rua fica molhada. Hoje choveu. Seca? | `["Sim", "Não"]` | Não | `["Não"]` | Causa e Efeito Necessário |
| **220** | Luiza só estuda de noite. É de manhã. Luíza estuda? | `["Sim", "Não"]` | Não | `["Não"]` | Exclusão de Premissas |
| **221** | Cão Tiago > Cão Paula > Cão Rita. Qual o maior? | `["Paula", "Rita", "Tiago"]` | Tiago | `["Tiago"]` | Ordenação Lógica |
| **222** | Algumas frutas são cítricas (ex: limão). Todas são? | `["Sim", "Não"]` | Não | `["Não"]` | Quantificadores Lógicos |
| **223** | Rel. A atrasa. B adianta. C pontual (12h). Qual marca 11:50? | `["A", "B", "C"]` | Relógio A | `["A", "Relógio A"]` | Inferência de Estados |
| **224** | Mário nunca mente à 2ªF. Hoje diz: "Hoje é 3ª". Hoje é 2ª? | `["Sim", "Não"]` | Não | `["Não"]` | Paradoxo Simples |
| **225** | Fila de 5. Leo = 5º. Caio = 1º. Bia atrás Caio. Duda = 4º. Rui? | `["2º", "3º", "4º"]` | 3º Lugar | `["3º", "3º Lugar", "3"]` | Localização Matricial |

---

### 3.4 Categoria: Frase Desordenada (IDs 226 a 240)
*Engine: `SENTENCE_ORDER` | Foco: Sintaxe, Reconstrução de Axiomas e Memória de Trabalho.*

| ID | Prompt | Tokens/Palavras | Resposta Esperada | Gabarito Técnico Normalizado | Competência Alvo |
|---|---|---|---|---|---|
| **226** | Ordene a frase lógica: tarde / do que / antes / nunca / Mais. | `["tarde", "do que", "antes", "nunca", "Mais"]` | Mais vale tarde do que nunca | `["Mais vale tarde do que nunca", "Mais antes tarde do que nunca"]` | Sintaxe e Cultura |
| **227** | Ordene a frase lógica: cão / morde / que / não / ladra. | `["cão", "morde", "que", "não", "ladra"]` | Cão que ladra não morde | `["Cão que ladra não morde"]` | Organização Frásica |
| **228** | Ordene a frase lógica: saudável / corpo / A / são / um / mente / habita. | `["saudável", "corpo", "A", "são", "um", "mente", "habita"]` | A mente sã habita um corpo saudável | `["A mente sã habita um corpo saudável", "A mente são habita um corpo saudável"]` | Coesão Lexical |
| **229** | Ordene a frase lógica: livro / capa / não / o / pela / Julgues. | `["livro", "capa", "não", "o", "pela", "Julgues"]` | Não julgues o livro pela capa | `["Não julgues o livro pela capa"]` | Flexibilidade Mental |
| **230** | Ordene a frase lógica: de / devagar / longe / vai / Quem / vai. | `["de", "devagar", "longe", "vai", "Quem", "vai"]` | Quem vai devagar vai longe | `["Quem vai devagar vai longe"]` | Ordenação Sintática |
| **231** | Ordene a frase lógica: sol / brilhando / O / hoje / forte / está. | `["sol", "brilhando", "O", "hoje", "forte", "está"]` | O sol está brilhando forte hoje | `["O sol está brilhando forte hoje", "Hoje o sol está brilhando forte"]` | Estruturação de Frase |
| **232** | Ordene a frase lógica: do / amanhã / o / trabalho / Não / para / deixes / hoje. | `["do", "amanhã", "o", "trabalho", "Não", "para", "deixes", "hoje"]` | Não deixes para amanhã o trabalho de hoje | `["Não deixes para amanhã o trabalho de hoje"]` | Memória de Trabalho Larga |
| **233** | Ordene a frase lógica: voa / Quando / nos / tempo / divertimos / o. | `["voa", "Quando", "nos", "tempo", "divertimos", "o"]` | O tempo voa quando nos divertimos | `["O tempo voa quando nos divertimos", "Quando nos divertimos o tempo voa"]` | Causa e Consequência |
| **234** | Ordene a frase lógica: sabedoria / livros / Os / fonte / de / são. | `["sabedoria", "livros", "Os", "fonte", "de", "são"]` | Os livros são fonte de sabedoria | `["Os livros são fonte de sabedoria"]` | Sentido Frásico Completo |
| **235** | Ordene a frase lógica: paciência / é / A / virtude / uma. | `["paciência", "é", "A", "virtude", "uma"]` | A paciência é uma virtude | `["A paciência é uma virtude"]` | Identificação de Sujeito/Verbo |
| **236** | Ordene a frase lógica: ouro / que / reluz / tudo / Nem / é. | `["ouro", "que", "reluz", "tudo", "Nem", "é"]` | Nem tudo que reluz é ouro | `["Nem tudo que reluz é ouro"]` | Compreensão Filosófica |
| **237** | Ordene a frase lógica: perfeição / faz / A / prática / a. | `["perfeição", "faz", "A", "prática", "a"]` | A prática faz a perfeição | `["A prática faz a perfeição"]` | Previsão Linguística |
| **238** | Ordene a frase lógica: mais / silêncio / palavras / que / O / fala / muitas. | `["mais", "silêncio", "palavras", "que", "O", "fala", "muitas"]` | O silêncio fala mais que muitas palavras | `["O silêncio fala mais que muitas palavras"]` | Paradoxos Organizacionais |
| **239** | Ordene a frase lógica: juntos / sempre / Somos / fortes / mais. | `["juntos", "sempre", "Somos", "fortes", "mais"]` | Somos sempre mais fortes juntos | `["Somos sempre mais fortes juntos", "Juntos somos sempre mais fortes"]` | Construção Lógica Coesa |
| **240** | Ordene a frase lógica: e / água / mole / dura / fura / pedra / bate / até / que. | `["e", "água", "mole", "dura", "fura", "pedra", "bate", "até", "que"]` | Água mole em pedra dura, bate até que fura | `["Água mole em pedra dura bate até que fura", "Água mole e pedra dura bate até que fura"]` | Organização Sequencial Complexa |

---

### 3.5 Categoria: Expressões Idiomáticas (IDs 241 a 255)
*Engine: `SINGLE_CHOICE` | Foco: Metáforas Comportamentais, Simbolismo e Contexto Sociocultural.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **241** | Qual o significado de "Bater as botas"? | `["Comprar sapatos", "Morrer"]` | Morrer | `["Morrer"]` | Literacia Sociocultural |
| **242** | Qual o significado de "Cabeça dura"? | `["Teimoso", "Usar capacete"]` | Teimoso | `["Teimoso"]` | Transição Abstrata |
| **243** | Significado de "Chorar sobre o leite derramado"? | `["Lamentar o passado", "Limpar"]` | Lamentar o que passou | `["Lamentar o passado", "Lamentar o que passou"]` | Processamento Emocional Simbólico |
| **244** | Significado de "Andar a pisar ovos"? | `["Fazer um bolo", "Ter extremo cuidado"]` | Ter extremo cuidado | `["Ter extremo cuidado"]` | Metáforas Comportamentais |
| **245** | Significado de "Lavar as mãos" num conflito? | `["Não assumir responsabilidade", "Ficar limpo"]` | Não assumir responsabilidade | `["Não assumir responsabilidade"]` | Ética e Expressão Figurada |
| **246** | Significado de "Pôr as mãos no fogo" por alguém? | `["Queimar-se", "Confiar plenamente"]` | Confiar plenamente | `["Confiar plenamente"]` | Avaliação de Confiança |
| **247** | Significado de ter "Pé frio"? | `["Precisar de meias", "Ter azar"]` | Ter azar | `["Ter azar"]` | Associação Metonímica |
| **248** | Significado de "Pagar o pato"? | `["Comprar jantar", "Sofrer consequências alheias"]` | Sofrer as consequências | `["Sofrer consequências alheias", "Sofrer as consequências"]` | Interpretação Complexa |
| **249** | Significado de "Encher chouriços"? | `["Cozinhar", "Falar sem dizer nada importante"]` | Falar muito sem dizer nada | `["Falar sem dizer nada importante", "Falar muito sem dizer nada"]` | Filtragem Analítica |
| **250** | Significado de "Dar com os burros na água"? | `["Fracassar", "Dar banho aos animais"]` | Fracassar num plano | `["Fracassar", "Fracassar num plano"]` | Interpretação Narrativa |
| **251** | Significado de "Acordar com os pés de fora"? | `["Ter cama pequena", "Acordar de mau humor"]` | Acordar de mau humor | `["Acordar de mau humor"]` | Avaliação Emocional |
| **252** | Significado de "Ficar a segurar a vela"? | `["Faltar a luz", "Ser o terceiro intruso num casal"]` | Estar a sobrar (intruso) | `["Ser o terceiro intruso num casal", "Estar a sobrar (intruso)"]` | Contexto Social Abstrato |
| **253** | Significado de "Estar com a faca e o queijo na mão"? | `["Comer", "Ter o controlo absoluto"]` | Ter controlo da situação | `["Ter o controlo absoluto", "Ter controlo da situação"]` | Raciocínio Analógico |
| **254** | Significado de "Tirar o cavalinho da chuva"? | `["Ajudar um animal", "Desistir da ideia"]` | Desistir de uma expetativa | `["Desistir da ideia", "Desistir de uma expetativa"]` | Desconstrução de Expetativas |
| **255** | Significado de "Ter o coração na boca"? | `["Estar doente", "Estar muito assustado/ansioso"]` | Estar ansioso/assustado | `["Estar muito assustado/ansioso", "Estar ansioso/assustado"]` | Consciência Interoceptiva e Figurada |

---

### 3.6 Categoria: Raciocínio Numérico (IDs 256 a 270)
*Engine: `NUMERIC_SEQUENCE` / `SINGLE_CHOICE` | Foco: Álgebra, Progressões, Quadrados Perfeitos e Undo/Inversão.*

| ID | Prompt | Opções | Resposta Esperada | Gabarito Técnico | Competência Alvo |
|---|---|---|---|---|---|
| **256** | Padrão Matemático: 2, 4, 6, 8, [?] | `["9", "10", "12"]` | 10 | `["10"]` | Progressão Aritmética |
| **257** | Padrão Matemático: 1, 3, 5, 7, [?] | `["8", "9", "11"]` | 9 | `["9"]` | Lógica Numérica Ímpar |
| **258** | Padrão Matemático: 10, 20, 30, [?], 50 | `["35", "40", "45"]` | 40 | `["40"]` | Contagem em Dezenas |
| **259** | A + A = 10. B + B = 6. Quanto é A + B? | `["8", "16", "12"]` | 8 | `["8"]` | Resolução de Equações Básicas |
| **260** | Padrão Numérico: 1, 2, 4, 8, [?] | `["10", "12", "16"]` | 16 | `["16"]` | Progressão Geométrica |
| **261** | Sequência Decrescente: 100, 90, 80, 70, [?] | `["60", "50", "65"]` | 60 | `["60"]` | Subtração Sistemática |
| **262** | 1 triângulo=3. 1 quadrado=4. 2 triângulos + 1 quadrado = ? | `["7", "10", "11"]` | 10 | `["10"]` | Representação Simbólica |
| **263** | Qual é a metade do dobro de 12? | `["6", "12", "24"]` | 12 | `["12"]` | Inferência Linguístico-Matemática |
| **264** | Padrão Numérico: 3, 6, 9, 12, [?] | `["13", "14", "15"]` | 15 | `["15"]` | Multiplicação por 3 |
| **265** | Se X + 5 = 12. Qual é o valor de X? | `["6", "7", "8"]` | 7 | `["7"]` | Álgebra Introdutória |
| **266** | Sequência Decrescente: 25, 20, 15, 10, [?] | `["5", "0", "-5"]` | 5 | `["5"]` | Cálculo Regressivo |
| **267** | O tijolo pesa 1kg mais meio tijolo. Quanto pesa o tijolo? | `["1.5kg", "2kg", "1kg"]` | 2kg (1kg = a outra metade) | `["2kg", "2", "2kg (1kg = a outra metade)"]` | Resolução de Paradoxo Matemático |
| **268** | Tenho 3 dúzias de ovos. Uso 10. Fico com quantos? | `["20", "26", "30"]` | 26 | `["26"]` | Operações Compostas |
| **269** | Sequência: 1, 4, 9, 16, [?] (Quadrados Perfeitos) | `["20", "25", "24"]` | 25 | `["25"]` | Maturação Lógico-Dedutiva |
| **270** | Pensei num número. Dobrei-o. Juntei 4, deu 14. Qual era o número? | `["6", "5", "4"]` | 5 | `["5"]` | Raciocínio em Inverso (Undo) |

---

## 3. Matriz de Distribuição das Sessões (10 Sessões x 9 Exercícios)

A distribuição recomendada para compor as 10 sessões no banco de dados, equilibrando dificuldade e áreas cognitivas:

| Sessão | Perfil / Faixa Etária | Exercícios (IDs) | Foco Pedagógico |
|---|---|---|---|
| **Sessão 01** | 3 a 5 anos | 1 a 9 | Sombras, Formas e Contornos |
| **Sessão 02** | 3 a 5 anos | 10 a 18 | Sombras + Exclusão de Intruso |
| **Sessão 03** | 3 a 5 anos | 19 a 27 | Intruso + Categorias de Alimentos/Objetos |
| **Sessão 04** | 3 a 5 anos | 28 a 36 | Esquema Corporal e Sequências Simples |
| **Sessão 05** | 3 a 5 anos | 37 a 45 | Velocidade, Tamanhos e Adivinhas Básicas |
| **Sessão 06** | 6 a 10 anos | 91 a 99 | Anagramas, Alfabetização e Reorganização Lexical |
| **Sessão 07** | 6 a 10 anos | 106 a 114 | Qual Letra Falta (Ortografia e Dígrafos) |
| **Sessão 08** | 6 a 10 anos | 121 a 129 | Verdadeiro ou Falso (Ciências e Mundo Físico) |
| **Sessão 09** | 6 a 10 anos | 136 a 144 | Problemas Lógicos e Operações Concretas |
| **Sessão 10** | 11+ anos | 181 a 189 | Pensamento Lateral e Metáforas Abstratas |
| **Sessão 11+ (Expansão)**| 11+ anos | 196 a 270 | Polissemia, Dedução Lógica, Frases e Álgebra |
