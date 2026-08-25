# Catálogo real de sessões e exercícios (issue #19).
# Preenchido incrementalmente a partir do material de referência da terapeuta.
#
# Cada item de SESSOES:
#   {
#       "numero": int,
#       "titulo": str,
#       "descricao": str,           # opcional
#       "exercicios": [
#           {
#               "numero": int,       # único dentro da sessão
#               "tipo": str,         # uma das TIPO_CHOICES de ExercicioModelo
#               "enunciado": str,
#               "configuracao": dict,
#           },
#           ...
#       ],
#   }


def _mania_de(letra):
    return {
        "itens": [
            {"texto": f"1. O nome de um país começando com {letra}:"},
            {"texto": f"2. Os nomes de duas flores começando com {letra}:"},
            {"texto": f"3. Os nomes de três cores começando com {letra}:"},
            {"texto": f"4. Os nomes de quatro animais começando com {letra}:"},
            {"texto": f"5. Os nomes de cinco alimentos começando com {letra}:"},
            {"texto": f"6. Os nomes de seis profissões começando com {letra}:"},
            {"texto": f"7. Os nomes de sete cidades brasileiras começando com {letra}:"},
            {"texto": f"8. Os nomes de oito objetos começando com {letra}:"},
            {"texto": f"9. Os nomes de nove pessoas começando com {letra}:"},
            {"texto": f"10. Dez verbos começando com {letra}:"},
        ]
    }


# Exercícios piloto (issue #19): 83 exercícios de conteúdo INVENTADO (não é o
# material real da terapeuta), no formato/mecânica do manual de referência, para
# ela avaliar antes de entrarmos com o conteúdo definitivo das 10 sessões reais.
# Os outros 11 itens do piloto (mecânicas ainda não suportadas: grade de caminho,
# grade numérica, grade de dedução, memória) ficaram de fora — dependem de novos
# tipos de exercício.
#
# Divididos em várias SessaoModelo (91-99) — numeração que não colide com as
# sessões reais 1-10 — só pra testar o fluxo de escolha de sessão com mais de
# uma opção. O "numero" de cada exercício abaixo é o número original do item no
# PDF piloto (mantido pra referência cruzada), não precisa ser sequencial dentro
# da sessão dividida.
_PILOTO_EXERCICIOS = [
    {
                "numero": 1,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 palavras foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "ELATFEEN", "resposta": "ELEFANTE", "sombreadas": []},
                        {"embaralhada": "IGRFAA", "resposta": "GIRAFA", "sombreadas": []},
                        {"embaralhada": "RARGTATUA", "resposta": "TARTARUGA", "sombreadas": []},
                        {"embaralhada": "HOCORRAC", "resposta": "CACHORRO", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 2,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra C:",
                "configuracao": _mania_de("C"),
            },
            {
                "numero": 3,
                "tipo": "pergunta_aberta",
                "enunciado": "Charada da estrada",
                "configuracao": {
                    "itens": [
                        {
                            "texto": (
                                "Você chega numa bifurcação. Um caminho leva à cidade, o "
                                "outro não. Um morador sempre fala a verdade; outro sempre "
                                "mente — mas você não sabe qual é qual, e só pode fazer uma "
                                "pergunta a um deles. O que você pergunta pra descobrir o "
                                "caminho certo?"
                            ),
                            "resposta_esperada": (
                                'Ex.: "Se eu perguntasse ao outro qual caminho leva à '
                                'cidade, o que ele diria?" (e faz o oposto)'
                            ),
                        }
                    ]
                },
            },
            {
                "numero": 4,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Conjunto 1:\n• Coma uma ___ madura.\n• Arregace a ___ da camisa.",
                            "resposta_esperada": "MANGA",
                        },
                        {
                            "texto": "Conjunto 2:\n• A ___ do Mundo de futebol é a cada 4 anos.\n• Guarde os pratos na ___.",
                            "resposta_esperada": "COPA",
                        },
                    ]
                },
            },
            {
                "numero": 6,
                "tipo": "multipla_escolha",
                "enunciado": 'DEVERFOBIA é uma palavra inventada. Qual você acha que é o significado dela?',
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": "Qual é o significado de DEVERFOBIA?",
                            "opcoes": ["Medo de aranha", "Medo de fazer o dever de casa", "Medo do escuro", "Medo de água"],
                            "correta": 1,
                        }
                    ]
                },
            },
            {
                "numero": 7,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 5 objetos de escola escondidos no quadro abaixo. Eles podem estar na horizontal ou na vertical.",
                "configuracao": {
                    "grid": [
                        list("CADERNOKL"),
                        list("EMUBCRDLA"),
                        list("BORRACHAP"),
                        list("SBQGBCNNI"),
                        list("CHCREGUAS"),
                        list("RNBSDHUUS"),
                        list("BSSMBHBRE"),
                        list("JNERDSJRV"),
                        list("MOCHILAFD"),
                    ],
                    "palavras": ["LAPIS", "CADERNO", "BORRACHA", "REGUA", "MOCHILA"],
                },
            },
            {
                "numero": 9,
                "tipo": "ordena_letras",
                "enunciado": "Desembaralhe o nome de cada profissão a partir da dica:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "MCDIOE", "resposta": "MEDICO", "sombreadas": []},
                        {"embaralhada": "PODERIA", "resposta": "PADEIRO", "sombreadas": []},
                        {"embaralhada": "NPRIOT", "resposta": "PINTOR", "sombreadas": []},
                        {"embaralhada": "DAETNSTI", "resposta": "DENTISTA", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 10,
                "tipo": "pergunta_aberta",
                "enunciado": "Quantos anos tem?",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Ana tem o dobro da idade do seu irmão. Se o irmão tem 4 anos, quantos anos tem Ana?",
                            "resposta_esperada": "8 anos",
                        }
                    ]
                },
            },
            {
                "numero": 11,
                "tipo": "pergunta_aberta",
                "enunciado": "Quem sou eu?",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Tenho quatro patas, um rabo peludo, gosto de ossos e late. Quem sou eu?",
                            "resposta_esperada": "Cachorro",
                        }
                    ]
                },
            },
            {
                "numero": 13,
                "tipo": "pergunta_aberta",
                "enunciado": (
                    'Forme uma palavra que contenha as letras abaixo, nesta ordem, sem '
                    'nenhuma outra letra no meio delas. Por exemplo: dado "NT", PONTE é '
                    "uma resposta válida."
                ),
                "configuracao": {
                    "itens": [
                        {"texto": "1. ___ BR ___", "resposta_esperada": "ex.: LIBRA, SOMBRA"},
                        {"texto": "2. ___ OL ___", "resposta_esperada": "ex.: VIOLA, ESCOLA"},
                        {"texto": "3. ___ AN ___", "resposta_esperada": "ex.: PLANETA, BANANA"},
                        {"texto": "4. ___ CH ___", "resposta_esperada": "ex.: MOCHILA, FECHAR"},
                    ]
                },
            },
            {
                "numero": 14,
                "tipo": "pergunta_aberta",
                "enunciado": "Palíndromos",
                "configuracao": {
                    "itens": [
                        {
                            "texto": (
                                "Palíndromo é uma palavra que continua igual quando lida de "
                                "trás para frente. Por exemplo: ANA. Escreva 3 palíndromos "
                                "que você conhece:"
                            ),
                            "resposta_esperada": "ex.: OVO, ARARA, RADAR",
                        }
                    ]
                },
            },
            {
                "numero": 15,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "Numa turma de 13 alunos, com certeza pelo menos 2 fazem aniversário no mesmo mês.", "correta": True},
                        {"texto": "Numa turma de 5 alunos, com certeza pelo menos 2 fazem aniversário no mesmo mês.", "correta": False},
                        {"texto": "Numa turma de 13 alunos, é possível que nenhum aniversário caia no mesmo mês que outro.", "correta": False},
                    ]
                },
            },
            {
                "numero": 16,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 5 nomes de brinquedos escondidos no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("BONECAOP"),
                        list("ROOQSGFI"),
                        list("BOLAQPUA"),
                        list("TFDOJECO"),
                        list("RXPIPAIU"),
                        list("BTMOUZOT"),
                        list("UFTAQCIB"),
                        list("BGHTAOOK"),
                    ],
                    "palavras": ["BONECA", "BOLA", "PIAO", "PIPA", "IOIO"],
                },
            },
            {
                "numero": 17,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra P:",
                "configuracao": _mania_de("P"),
            },
            {
                "numero": 18,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Conjunto 1:\n• Machuquei a ___ da perna.\n• Bolo de ___ é gostoso.",
                            "resposta_esperada": "CANELA",
                        },
                        {
                            "texto": "Conjunto 2:\n• Sente no ___ do parque.\n• Guardei meu dinheiro no ___.",
                            "resposta_esperada": "BANCO",
                        },
                    ]
                },
            },
            {
                "numero": 19,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 nomes foram embaralhadas. Escreva o nome certo:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "LCASU", "resposta": "LUCAS", "sombreadas": []},
                        {"embaralhada": "AIARM", "resposta": "MARIA", "sombreadas": []},
                        {"embaralhada": "DERPO", "resposta": "PEDRO", "sombreadas": []},
                        {"embaralhada": "OSIAF", "resposta": "SOFIA", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 20,
                "tipo": "pergunta_aberta",
                "enunciado": "Falta uma letra em cada nome. Descubra qual é e escreva o nome completo:",
                "configuracao": {
                    "itens": [
                        {"texto": "1. P_DRO", "resposta_esperada": "PEDRO"},
                        {"texto": "2. J_LIA", "resposta_esperada": "JULIA"},
                        {"texto": "3. L_CAS", "resposta_esperada": "LUCAS"},
                        {"texto": "4. _NA", "resposta_esperada": "ANA"},
                    ]
                },
            },
            {
                "numero": 22,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "O sol é uma estrela.", "correta": True},
                        {"texto": "Os peixes respiram fora da água.", "correta": False},
                        {"texto": "Uma semana tem 7 dias.", "correta": True},
                        {"texto": "As borboletas nascem de lagartas.", "correta": True},
                        {"texto": "O gelo é mais quente que a água líquida.", "correta": False},
                    ]
                },
            },
            {
                "numero": 23,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensamento lateral",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Qual é a coisa que, quanto mais você tira dela, maior ela fica?",
                            "resposta_esperada": "Um buraco",
                        }
                    ]
                },
            },
            {
                "numero": 24,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 palavras foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "LNJEAA", "resposta": "JANELA", "sombreadas": []},
                        {"embaralhada": "RDCAEAI", "resposta": "CADEIRA", "sombreadas": []},
                        {"embaralhada": "OPTSAA", "resposta": "SAPATO", "sombreadas": []},
                        {"embaralhada": "GERLOIO", "resposta": "RELOGIO", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 25,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 6 nomes de cores escondidos no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("BRANCOKAE"),
                        list("MUBCRDLZS"),
                        list("VERDEBQUG"),
                        list("BCNNCHCLR"),
                        list("NBSDHUPUS"),
                        list("BSROXORSM"),
                        list("BHBREJENE"),
                        list("ROSARDTSJ"),
                        list("RVFDSSOUG"),
                    ],
                    "palavras": ["BRANCO", "VERDE", "AZUL", "ROXO", "ROSA", "PRETO"],
                },
            },
            {
                "numero": 26,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 palavras foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "RORZA", "resposta": "ARROZ", "sombreadas": []},
                        {"embaralhada": "IPCAPO", "resposta": "PIPOCA", "sombreadas": []},
                        {"embaralhada": "EROVSET", "resposta": "SORVETE", "sombreadas": []},
                        {"embaralhada": "ANNABA", "resposta": "BANANA", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 27,
                "tipo": "pergunta_aberta",
                "enunciado": "Muitas palavras...",
                "configuracao": {
                    "itens": [
                        {
                            "texto": (
                                "Forme o maior número possível de palavras usando as letras "
                                "abaixo (cada letra só pode ser usada uma vez na mesma "
                                "palavra): M A R O T I P S"
                            ),
                            "resposta_esperada": "Aberto — ex.: MAR, RATO, PATO, TIME, PRATO",
                        }
                    ]
                },
            },
            {
                "numero": 28,
                "tipo": "multipla_escolha",
                "enunciado": 'Organize as letras. Todas as palavras começam com a letra A. Depois, marque a categoria certa:',
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": "1. AUGAI — desembaralhe e marque a categoria certa:",
                            "opcoes": ["uma ave", "um animal aquático", "uma fruta", "uma cidade"],
                            "correta": 0,
                        },
                        {
                            "texto": "2. ACABIAX — desembaralhe e marque a categoria certa:",
                            "opcoes": ["uma fruta", "uma profissão", "um país", "uma cor"],
                            "correta": 0,
                        },
                        {
                            "texto": "3. RTAO — desembaralhe e marque a categoria certa:",
                            "opcoes": ["uma profissão", "um animal", "um alimento", "uma cidade"],
                            "correta": 1,
                        },
                        {
                            "texto": (
                                "4. AERLAOM — desembaralhe e marque a categoria certa "
                                "[CONFERIR: anagrama incerto na extração do PDF, ver "
                                "imagem original]"
                            ),
                            "opcoes": ["um animal", "uma cor", "um país", "um objeto"],
                            "correta": 3,
                        },
                    ]
                },
            },
            {
                "numero": 30,
                "tipo": "pergunta_aberta",
                "enunciado": "Esses provérbios perderam as vogais. Você consegue descobrir quais são?",
                "configuracao": {
                    "itens": [
                        {"texto": "1. DVGR S V LNG", "resposta_esperada": "DEVAGAR SE VAI LONGE"},
                        {"texto": "2. QM N RRSC N PTSC", "resposta_esperada": "QUEM NÃO ARRISCA NÃO PETISCA"},
                    ]
                },
            },
            {
                "numero": 31,
                "tipo": "pergunta_aberta",
                "enunciado": "Muitos pés",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Numa sala há alguns cachorros e algumas galinhas. Ao todo são 5 cabeças e 14 pés. Quantos cachorros e quantas galinhas há?",
                            "resposta_esperada": "2 cachorros e 3 galinhas (2×4 + 3×2 = 14 pés, 2+3 = 5 cabeças)",
                        }
                    ]
                },
            },
            {
                "numero": 32,
                "tipo": "pergunta_aberta",
                "enunciado": "Se você sabe, escreva a resposta. Se não sabe, é uma boa desculpa pra aprender algo novo!",
                "configuracao": {
                    "itens": [
                        {"texto": "1. Quantas patas tem uma aranha?", "resposta_esperada": "8"},
                        {"texto": "2. Qual é o maior animal do mundo?", "resposta_esperada": "Baleia-azul"},
                        {"texto": "3. Quantos dias tem uma semana?", "resposta_esperada": "7"},
                        {"texto": '4. Qual planeta é conhecido como o "planeta vermelho"?', "resposta_esperada": "Marte"},
                    ]
                },
            },
            {
                "numero": 34,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 6 nomes de animais escondidos no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("ELEFANTEKT"),
                        list("EMUBCRDLSI"),
                        list("GIRAFABQGG"),
                        list("BCNNCHCRLR"),
                        list("MACACONBEE"),
                        list("SDHUUSBSAS"),
                        list("MBZEBRAHOB"),
                        list("REJNERDSJR"),
                        list("VFDSSUGLDR"),
                        list("XCSBTGPVRN"),
                    ],
                    "palavras": ["ELEFANTE", "GIRAFA", "MACACO", "TIGRE", "ZEBRA", "LEAO"],
                },
            },
            {
                "numero": 35,
                "tipo": "multipla_escolha",
                "enunciado": "De qual história de fadas é essa fala? Marque a alternativa certa.",
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": '1. "Espelho, espelho meu, existe alguém mais bela do que eu?"',
                            "opcoes": ["Cinderela", "A madrasta má de Branca de Neve", "Rapunzel", "A Bela Adormecida"],
                            "correta": 1,
                        },
                        {
                            "texto": '2. "Eu vou soprar e vou arrebentar!"',
                            "opcoes": ["O Lobo Mau", "Os Três Porquinhos", "Chapeuzinho Vermelho", "O Gato de Botas"],
                            "correta": 0,
                        },
                        {
                            "texto": '3. "Que dentes grandes você tem!"',
                            "opcoes": ["O Lobo Mau", "Chapeuzinho Vermelho", "A Vovozinha", "O Caçador"],
                            "correta": 1,
                        },
                    ]
                },
            },
            {
                "numero": 37,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra F:",
                "configuracao": _mania_de("F"),
            },
            {
                "numero": 38,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra S:",
                "configuracao": _mania_de("S"),
            },
            {
                "numero": 39,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra M:",
                "configuracao": _mania_de("M"),
            },
            {
                "numero": 40,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra G:",
                "configuracao": _mania_de("G"),
            },
            {
                "numero": 41,
                "tipo": "pergunta_aberta",
                "enunciado": "Escreva palavras que começam com a letra V:",
                "configuracao": _mania_de("V"),
            },
            {
                "numero": 42,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {"texto": "Conjunto 1:\n• Cole o ___ na carta.\n• Ele tem um ___ de nascença.", "resposta_esperada": "SELO"},
                        {"texto": "Conjunto 2:\n• Corte a ___ pra fazer suco.\n• Use a ___ pra afiar a unha.", "resposta_esperada": "LIMA"},
                    ]
                },
            },
            {
                "numero": 43,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {"texto": "Conjunto 1:\n• Coloque um ___ de gelo no suco.\n• Essa caixa tem formato de ___.", "resposta_esperada": "CUBO"},
                        {"texto": "Conjunto 2:\n• Acenda a ___ do bolo.\n• O barco tem uma ___ grande.", "resposta_esperada": "VELA"},
                    ]
                },
            },
            {
                "numero": 44,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {"texto": "Conjunto 1:\n• Ela ganhou um ___ de noivado.\n• Adoro ___ de cebola frito.", "resposta_esperada": "ANEL"},
                        {"texto": "Conjunto 2:\n• Costure o ___ da camisa.\n• Aperte o ___ da campainha.", "resposta_esperada": "BOTAO"},
                    ]
                },
            },
            {
                "numero": 45,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {"texto": "Conjunto 1:\n• O ___ cantou de manhã.\n• Ele levou um ___ de tão bravo.", "resposta_esperada": "GALO"},
                        {"texto": "Conjunto 2:\n• O passarinho bateu a ___.\n• A xícara quebrou a ___.", "resposta_esperada": "ASA"},
                    ]
                },
            },
            {
                "numero": 46,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {"texto": "Conjunto 1:\n• A ___ da árvore caiu no chão.\n• Escreva numa ___ de papel.", "resposta_esperada": "FOLHA"},
                        {"texto": "Conjunto 2:\n• Ele fala outra ___ muito bem.\n• Mostre a ___ pro médico.", "resposta_esperada": "LINGUA"},
                    ]
                },
            },
            {
                "numero": 47,
                "tipo": "pergunta_aberta",
                "enunciado": "Uma mesma palavra encaixa em todas as frases do conjunto. Descubra qual é:",
                "configuracao": {
                    "itens": [
                        {"texto": "Conjunto 1:\n• A planta cresceu a ___ pro sol.\n• Calcule a ___ quadrada do número.", "resposta_esperada": "RAIZ"},
                        {"texto": "Conjunto 2:\n• Atravesse a ___ com cuidado.\n• Fiz uma ___ de amizade com ele.", "resposta_esperada": "PONTE"},
                    ]
                },
            },
            {
                "numero": 48,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 esportes foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "OELFTUB", "resposta": "FUTEBOL", "sombreadas": []},
                        {"embaralhada": "AOCNTAA", "resposta": "NATACAO", "sombreadas": []},
                        {"embaralhada": "IVOEL", "resposta": "VOLEI", "sombreadas": []},
                        {"embaralhada": "UODJ", "resposta": "JUDO", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 49,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 instrumentos musicais foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "RIUGRTAA", "resposta": "GUITARRA", "sombreadas": []},
                        {"embaralhada": "ABREATI", "resposta": "BATERIA", "sombreadas": []},
                        {"embaralhada": "ULATAF", "resposta": "FLAUTA", "sombreadas": []},
                        {"embaralhada": "IOOIVLN", "resposta": "VIOLINO", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 50,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 meios de transporte foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "LTICCAIEB", "resposta": "BICICLETA", "sombreadas": []},
                        {"embaralhada": "OCRRA", "resposta": "CARRO", "sombreadas": []},
                        {"embaralhada": "RTEM", "resposta": "TREM", "sombreadas": []},
                        {"embaralhada": "NAVOI", "resposta": "NAVIO", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 51,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 doces foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "CLOACTHOE", "resposta": "CHOCOLATE", "sombreadas": []},
                        {"embaralhada": "TIORLUPI", "resposta": "PIRULITO", "sombreadas": []},
                        {"embaralhada": "LAAB", "resposta": "BALA", "sombreadas": []},
                        {"embaralhada": "PIMDU", "resposta": "PUDIM", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 52,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 roupas foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "AAEMCSTI", "resposta": "CAMISETA", "sombreadas": []},
                        {"embaralhada": "HORSST", "resposta": "SHORTS", "sombreadas": []},
                        {"embaralhada": "NESTI", "resposta": "TENIS", "sombreadas": []},
                        {"embaralhada": "EBON", "resposta": "BONE", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 53,
                "tipo": "ordena_letras",
                "enunciado": "As letras de 4 móveis foram embaralhadas. Escreva a palavra certa:",
                "configuracao": {
                    "palavras": [
                        {"embaralhada": "RCAAEDI", "resposta": "CADEIRA", "sombreadas": []},
                        {"embaralhada": "MAES", "resposta": "MESA", "sombreadas": []},
                        {"embaralhada": "AOFS", "resposta": "SOFA", "sombreadas": []},
                        {"embaralhada": "RAIMRAO", "resposta": "ARMARIO", "sombreadas": []},
                    ]
                },
            },
            {
                "numero": 54,
                "tipo": "pergunta_aberta",
                "enunciado": "Falta uma letra em cada palavra. Complete:",
                "configuracao": {
                    "itens": [
                        {"texto": "1. P_TO", "resposta_esperada": "ex.: PATO"},
                        {"texto": "2. B_LA", "resposta_esperada": "ex.: BOLA"},
                        {"texto": "3. C_SA", "resposta_esperada": "CASA"},
                        {"texto": "4. F_CA", "resposta_esperada": "ex.: FACA"},
                        {"texto": "5. S_L", "resposta_esperada": "ex.: SOL"},
                        {"texto": "6. M_R", "resposta_esperada": "ex.: MAR"},
                    ]
                },
            },
            {
                "numero": 55,
                "tipo": "pergunta_aberta",
                "enunciado": "Falta uma letra em cada palavra. Complete:",
                "configuracao": {
                    "itens": [
                        {"texto": "1. R_TO", "resposta_esperada": "ex.: RATO"},
                        {"texto": "2. L_VA", "resposta_esperada": "LUVA"},
                        {"texto": "3. C_MA", "resposta_esperada": "CAMA"},
                        {"texto": "4. P_LO", "resposta_esperada": "ex.: PELO"},
                        {"texto": "5. S_PO", "resposta_esperada": "SAPO"},
                        {"texto": "6. N_VE", "resposta_esperada": "ex.: NEVE"},
                    ]
                },
            },
            {
                "numero": 56,
                "tipo": "pergunta_aberta",
                "enunciado": "Qual é a única letra que completa todas estas palavras?",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "1. _ATO\n2. _URO\n3. _ILA\n4. _OME\n5. _ESTA",
                            "resposta_esperada": "F (FATO, FURO, FILA, FOME, FESTA)",
                        }
                    ]
                },
            },
            {
                "numero": 57,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "O que anda o dia inteiro mas nunca sai do lugar?", "resposta_esperada": "O relógio"}]},
            },
            {
                "numero": 58,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "Quanto mais eu seco, mais molhado fico. O que sou?", "resposta_esperada": "A toalha"}]},
            },
            {
                "numero": 59,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Tenho cidades, mas não tenho casas. Tenho montanhas, mas não tenho árvores. Tenho água, mas não tenho peixes. O que sou?",
                            "resposta_esperada": "Um mapa",
                        }
                    ]
                },
            },
            {
                "numero": 60,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Se você me soltar, eu quebro. Mas se você nunca me tocar, eu também quebro. O que sou?",
                            "resposta_esperada": "Uma promessa",
                        }
                    ]
                },
            },
            {
                "numero": 61,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Numa corrida, você ultrapassa quem está em segundo lugar. Em que posição você fica?",
                            "resposta_esperada": "Segundo lugar",
                        }
                    ]
                },
            },
            {
                "numero": 62,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "Tenho dentes, mas não mordo. O que sou?", "resposta_esperada": "Um pente (ou garfo/serrote)"}]},
            },
            {
                "numero": 63,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Duas mães e duas filhas foram à feira e compraram 3 maçãs. Cada uma ganhou uma maçã inteira, e nenhuma sobrou nem faltou. Como isso é possível?",
                            "resposta_esperada": "São só 3 pessoas: avó, mãe e filha",
                        }
                    ]
                },
            },
            {
                "numero": 64,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "O que fica mais pesado quanto mais água você tira dele?", "resposta_esperada": "Uma esponja/toalha molhada"}]},
            },
            {
                "numero": 65,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "Um menino tinha 5 balas e comeu todas, menos 3. Quantas balas sobraram?", "resposta_esperada": "3"}]},
            },
            {
                "numero": 66,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "Tenho teclas, mas não abro nenhuma porta. O que sou?", "resposta_esperada": "Um piano (ou teclado)"}]},
            },
            {
                "numero": 67,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {"itens": [{"texto": "Quanto menor eu fico, mais claridade eu dou — até apagar de vez. O que sou?", "resposta_esperada": "Uma vela"}]},
            },
            {
                "numero": 68,
                "tipo": "pergunta_aberta",
                "enunciado": "Pensando um pouco...",
                "configuracao": {
                    "itens": [
                        {
                            "texto": "Eu te sigo o dia inteiro, mas nunca te alcanço, e desapareço quando escurece. O que sou?",
                            "resposta_esperada": "A sombra",
                        }
                    ]
                },
            },
            {
                "numero": 69,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "O morcego é uma ave.", "correta": False},
                        {"texto": "A baleia é um mamífero.", "correta": True},
                        {"texto": "A cobra tem pernas.", "correta": False},
                    ]
                },
            },
            {
                "numero": 70,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "O coração fica do lado esquerdo do peito.", "correta": True},
                        {"texto": "Nós temos 4 pulmões.", "correta": False},
                        {"texto": "Os dentes de leite caem e nascem outros no lugar.", "correta": True},
                    ]
                },
            },
            {
                "numero": 71,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "É possível escrever 100 como soma de 5 números ímpares.", "correta": False},
                    ]
                },
            },
            {
                "numero": 72,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "A Terra gira em torno do Sol.", "correta": True},
                        {"texto": "A Lua tem luz própria.", "correta": False},
                        {"texto": "Marte é conhecido como o planeta vermelho.", "correta": True},
                    ]
                },
            },
            {
                "numero": 73,
                "tipo": "verdadeiro_falso",
                "enunciado": "Essas frases são verdadeiras ou falsas?",
                "configuracao": {
                    "afirmacoes": [
                        {"texto": "O tomate é, na verdade, uma fruta.", "correta": True},
                        {"texto": "O chocolate vem do cacau.", "correta": True},
                        {"texto": "A batata cresce pendurada em árvores.", "correta": False},
                    ]
                },
            },
            {
                "numero": 74,
                "tipo": "multipla_escolha",
                "enunciado": 'Organize as letras. Todas as palavras começam com a letra S. Depois, marque a categoria certa:',
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": "1. SAOP — desembaralhe e marque a categoria certa:",
                            "opcoes": ["um animal", "uma fruta", "uma cidade", "um objeto"],
                            "correta": 0,
                        },
                        {
                            "texto": (
                                "2. CISEAU — desembaralhe e marque a categoria certa "
                                "[CONFERIR: anagrama incerto na extração do PDF]"
                            ),
                            "opcoes": ["uma profissão", "um país", "um alimento", "uma cor"],
                            "correta": 1,
                        },
                        {
                            "texto": (
                                "3. LNASAIDA — desembaralhe e marque a categoria certa "
                                "[CONFERIR: anagrama incerto na extração do PDF]"
                            ),
                            "opcoes": ["um animal", "um objeto", "uma cidade", "uma fruta"],
                            "correta": 2,
                        },
                        {
                            "texto": "4. SDADLOO — desembaralhe e marque a categoria certa:",
                            "opcoes": ["uma profissão", "um país", "um objeto", "uma cor"],
                            "correta": 0,
                        },
                    ]
                },
            },
            {
                "numero": 75,
                "tipo": "multipla_escolha",
                "enunciado": 'A expressão usa a palavra "cabeça". Marque o significado certo pra cada uma:',
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": '1. "Ele é muito cabeça-dura."',
                            "opcoes": ["Machucou a cabeça", "É muito teimoso", "É muito inteligente", "Tem dor de cabeça"],
                            "correta": 1,
                        },
                        {
                            "texto": '2. "O quarto dele está de cabeça pra baixo."',
                            "opcoes": ["Bagunçado", "Muito arrumado", "Pintado de azul", "Vazio"],
                            "correta": 0,
                        },
                        {
                            "texto": '3. "Ela manteve a cabeça fria."',
                            "opcoes": ["Estava com frio", "Ficou calma", "Ficou nervosa", "Foi tomar sorvete"],
                            "correta": 1,
                        },
                        {
                            "texto": '4. "Fiquei quebrando a cabeça com esse problema."',
                            "opcoes": ["Me machuquei", "Pensei bastante pra resolver", "Desisti logo", "Resolvi rápido, sem pensar"],
                            "correta": 1,
                        },
                    ]
                },
            },
            {
                "numero": 76,
                "tipo": "multipla_escolha",
                "enunciado": "É só pensar direito",
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": (
                                "Um vaso com um casal de coelhos dobra de quantidade a cada "
                                "mês. Em 6 meses, o vaso está cheio de coelhos. Em que mês o "
                                "vaso estava com metade da quantidade de coelhos?"
                            ),
                            "opcoes": ["No 3º mês", "No 4º mês", "No 5º mês", "No 6º mês, no fim do dia"],
                            "correta": 2,
                        }
                    ]
                },
            },
            {
                "numero": 77,
                "tipo": "multipla_escolha",
                "enunciado": 'Organize as letras. Todas as palavras começam com a letra M. Depois, marque a categoria certa:',
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": "1. CAMCOA — desembaralhe e marque a categoria certa:",
                            "opcoes": ["um animal", "um país", "uma cor", "um alimento"],
                            "correta": 0,
                        },
                        {
                            "texto": "2. MEXCIO — desembaralhe e marque a categoria certa:",
                            "opcoes": ["um animal", "um país", "uma profissão", "uma cidade"],
                            "correta": 1,
                        },
                        {
                            "texto": "3. OLMIAHC — desembaralhe e marque a categoria certa:",
                            "opcoes": ["um objeto", "um animal", "uma fruta", "uma cor"],
                            "correta": 0,
                        },
                        {
                            "texto": "4. ORITOTSAM — desembaralhe e marque a categoria certa:",
                            "opcoes": ["uma cidade", "uma profissão", "um objeto", "um país"],
                            "correta": 1,
                        },
                    ]
                },
            },
            {
                "numero": 78,
                "tipo": "multipla_escolha",
                "enunciado": "De qual história é essa fala? Marque a alternativa certa.",
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": '1. "Feijões, feijões mágicos!"',
                            "opcoes": ["João e o Pé de Feijão", "Cachinhos Dourados", "O Patinho Feio", "A Bela e a Fera"],
                            "correta": 0,
                        },
                        {
                            "texto": '2. "Alguém dormiu na minha cama, e ainda está aqui!"',
                            "opcoes": ["Os Três Porquinhos", "Cachinhos Dourados e os Três Ursos", "Branca de Neve", "Cinderela"],
                            "correta": 1,
                        },
                        {
                            "texto": '3. "Puxe a corda que a tranca vai subir."',
                            "opcoes": ["Chapeuzinho Vermelho", "Rapunzel", "João e Maria", "O Gato de Botas"],
                            "correta": 1,
                        },
                    ]
                },
            },
            {
                "numero": 79,
                "tipo": "multipla_escolha",
                "enunciado": "Marque a alternativa certa em cada pergunta:",
                "configuracao": {
                    "perguntas": [
                        {
                            "texto": "1. Qual desses é um réptil?",
                            "opcoes": ["Cachorro", "Jacaré", "Gato", "Passarinho"],
                            "correta": 1,
                        },
                        {
                            "texto": "2. Qual desses vive na água?",
                            "opcoes": ["Golfinho", "Coelho", "Galinha", "Cavalo"],
                            "correta": 0,
                        },
                        {
                            "texto": "3. Qual desses sabe voar?",
                            "opcoes": ["Pinguim", "Avestruz", "Coruja", "Cachorro"],
                            "correta": 2,
                        },
                    ]
                },
            },
            {
                "numero": 80,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 5 palavras escondidas no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("BONECAOP"),
                        list("ROOQSGFI"),
                        list("BOLAQPUA"),
                        list("TFDOJECO"),
                        list("RXPIPAIU"),
                        list("BTMOUZOT"),
                        list("UFTAQCIB"),
                        list("BGHTAOOK"),
                    ],
                    "palavras": ["BONECA", "BOLA", "PIAO", "PIPA", "IOIO"],
                },
            },
            {
                "numero": 81,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 5 palavras escondidas no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("CAMISAOS"),
                        list("ROOQSGFA"),
                        list("CALCAQPI"),
                        list("UTFDOJEA"),
                        list("CRXMEIAU"),
                        list("BTMOUZTU"),
                        list("BONEFTAQ"),
                        list("CBBGHTAO"),
                    ],
                    "palavras": ["CAMISA", "CALCA", "SAIA", "MEIA", "BONE"],
                },
            },
            {
                "numero": 82,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 5 palavras escondidas no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("CABECAOP"),
                        list("ROOQSGFE"),
                        list("BRACOQPR"),
                        list("UTFDOJEN"),
                        list("CRXMAOUA"),
                        list("BTMOUZTU"),
                        list("OLHOFTAQ"),
                        list("CBBGHTAO"),
                    ],
                    "palavras": ["CABECA", "BRACO", "PERNA", "MAO", "OLHO"],
                },
            },
            {
                "numero": 83,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 4 palavras escondidas no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("VIOLAOORT"),
                        list("OOQSGFQPA"),
                        list("FLAUTAUTM"),
                        list("FDOJECRXB"),
                        list("UBTMOUZTO"),
                        list("UFPIANOTR"),
                        list("AQCBBGHTA"),
                        list("OKOSGQHUJ"),
                        list("PAVCOUINR"),
                    ],
                    "palavras": ["VIOLAO", "FLAUTA", "TAMBOR", "PIANO"],
                },
            },
            {
                "numero": 84,
                "tipo": "caca_palavras",
                "enunciado": "Encontre 5 palavras escondidas no quadro abaixo (horizontal ou vertical).",
                "configuracao": {
                    "grid": [
                        list("ONIBUSORT"),
                        list("OOQSGFQPR"),
                        list("CARROUTFE"),
                        list("DOJECRXUM"),
                        list("BTMAVIAOO"),
                        list("UZTUFTAQC"),
                        list("BARCOBBGH"),
                        list("TAOKOSGQH"),
                        list("UJPAVCOUI"),
                    ],
                    "palavras": ["ONIBUS", "CARRO", "TREM", "AVIAO", "BARCO"],
                },
            },
            {
                "numero": 85,
                "tipo": "pergunta_aberta",
                "enunciado": (
                    "Acrescente uma palavra a cada grupo de 3 palavras, para formar novas "
                    'palavras compostas. Por exemplo: no grupo "chuva, sol, costas", a '
                    "palavra é guarda (guarda-chuva, guarda-sol, guarda-costas)."
                ),
                "configuracao": {
                    "itens": [
                        {"texto": "1. roupa, chuva, costas", "resposta_esperada": "GUARDA"},
                        {"texto": "2. retrato, voz, chaves", "resposta_esperada": "PORTA"},
                        {"texto": "3. vindo, estar, feito", "resposta_esperada": "BEM"},
                    ]
                },
            },
            {
                "numero": 86,
                "tipo": "pergunta_aberta",
                "enunciado": "Mais palavras 2",
                "configuracao": {
                    "itens": [
                        {
                            "texto": (
                                "Forme o maior número possível de palavras usando as letras "
                                "abaixo (cada letra só pode ser usada uma vez na mesma "
                                "palavra): T E C L A D O S"
                            ),
                            "resposta_esperada": "Aberto — ex.: TELA, LADO, DOSE, SECA, CASO",
                        }
                    ]
                },
            },
            {
                "numero": 87,
                "tipo": "pergunta_aberta",
                "enunciado": "Mais palavras 3",
                "configuracao": {
                    "itens": [
                        {
                            "texto": (
                                "Forme o maior número possível de palavras usando as letras "
                                "abaixo (cada letra só pode ser usada uma vez na mesma "
                                "palavra): B A R C O L I N"
                            ),
                            "resposta_esperada": "Aberto — ex.: BAR, COR, RIO, CARO, CABO, LINO",
                        }
                    ]
                },
            },
            {
                "numero": 88,
                "tipo": "pergunta_aberta",
                "enunciado": "As palavras desta frase estão fora de ordem. Escreva a frase correta:",
                "configuracao": {
                    "itens": [
                        {"texto": "gato o dorme sofá no", "resposta_esperada": "O gato dorme no sofá."}
                    ]
                },
            },
            {
                "numero": 89,
                "tipo": "pergunta_aberta",
                "enunciado": "As palavras desta frase estão fora de ordem. Escreva a frase correta:",
                "configuracao": {
                    "itens": [
                        {"texto": "amigos brincam os parque no", "resposta_esperada": "Os amigos brincam no parque."}
                    ]
                },
            },
            {
                "numero": 90,
                "tipo": "pergunta_aberta",
                "enunciado": "As palavras desta frase estão fora de ordem. Escreva a frase correta:",
                "configuracao": {
                    "itens": [
                        {"texto": "brilhando sol hoje está o", "resposta_esperada": "O sol está brilhando hoje."}
                    ]
                },
            },
        ]


def _chunk(lista, tamanho):
    for i in range(0, len(lista), tamanho):
        yield lista[i : i + tamanho]


SESSOES = [
    {
        "numero": 90 + indice,
        "titulo": f"[PILOTO] Sessão de teste {indice} — não usar em atendimento real",
        "descricao": (
            "Parte do piloto de 83 exercícios de conteúdo inventado (issue #19), "
            "dividido em sessões só para testar o fluxo de escolha de sessão. "
            "Não é o catálogo real."
        ),
        "exercicios": exercicios,
    }
    for indice, exercicios in enumerate(_chunk(_PILOTO_EXERCICIOS, 9), start=1)
]
