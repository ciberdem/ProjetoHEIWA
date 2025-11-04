#Pipeline de Limpeza de Dados v3#
Este repositório contém um pipeline de limpeza de dados v3 em Python, desenvolvido para pré-processar conjuntos de dados textuais. O pipeline foi desenvolvido para limpeza de dados advindos de redes sociais. Entretanto, ele pode ser utilizado para várias bases de dados textuais. O pipeline utiliza diversas bibliotecas, ferramentas e técnicas para garantir a qualidade e a consistência dos dados, incluindo agora tokenização e remoção de stopwords com NLTK.

<img src="https://github.com/ciberdem/ProjetoHEIWA-FAPESP/blob/main/CuradoriaExtracaoDados/pipeline_v2/assets/Pipeline_diagrama.png" alt="Diagrama do pipeline de limpeza">

Conteúdo
Como Utilizar

Dependências

Instalação das Dependências

Executando o Pipeline

Exemplo de Uso

Funcionalidades

Parâmetros para Ativar/Desativar Etapas

Funções do Pipeline

Estrutura de Saída

Detalhes do Pré-processamento de Texto

Como Utilizar
Dependências
Antes de executar o pipeline, certifique-se de ter as seguintes bibliotecas instaladas:

pandas : https://pandas.pydata.org/

demoji : https://pypi.org/project/demoji/

enelvo : https://github.com/thalesbertaglia/enelvo

unidecode : https://pypi.org/project/Unidecode/

nltk : https://www.nltk.org/

Instalação das Dependências
Para instalar todas as dependências, utilize o arquivo requirements.txt. Com o arquivo pronto, basta executar o comando:

Bash

pip install -r /path/to/requirements.txt
Você também precisará baixar os recursos necessários do NLTK (stopwords e tokenizador):

Python

import nltk
nltk.download('stopwords')
nltk.download('punkt')
Executando o Pipeline
Arquivo de entrada: O pipeline aceita arquivos nos formatos .csv ou .json. O caminho do arquivo de entrada e o nome da coluna que contém o texto a ser processado devem ser fornecidos.

Processamento: O pipeline pode ser executado por meio da função pipeline. Ela carrega o arquivo, aplica o pré-processamento e exporta o resultado.

OBS: Todas as etapas de pré-processamento são opcionais e podem ser ativadas ou desativadas conforme necessário ao chamar a função pipeline. Cada etapa é controlada por um parâmetro booleano (True para ativar e False para desativar).

Exemplo de Uso
Python

from pipeline import pipeline

caminho_arquivo = 'dados.csv'  # ou 'dados.json'
coluna = 'texto'
formato = 'json'

# Executando o pipeline com todas as etapas padrão (incluindo tokenização)
pipeline(caminho_arquivo, coluna, formato)
Funcionalidades
O pré-processamento de texto desempenha um papel crucial na qualidade e na consistência dos dados. No pipeline v3, várias etapas são realizadas para garantir que o texto de entrada seja limpo e adequado para análises subsequentes, como:

Remoção de menções a usuários (@usuario).

Remoção de URLs.

Normalização Enelvo (e tratamento de vírgulas).

Substituição de emojis por rótulos sentimentais.

Conversão de caracteres especiais para ASCII.

Remoção de pontuações e caracteres especiais.

(Novo) Tokenização do texto e remoção de stopwords.

Para desativar etapas específicas, basta definir o parâmetro desejado como False ao chamar a função pipeline. Por exemplo, para desativar a normalização e a nova etapa de tokenização:

Python

from pipeline import pipeline

# Executa o pipeline sem normalizar e sem tokenizar
pipeline('dados.csv', 'texto', formato='json', normalizar=False, tokenizar_texto=False)
Parâmetros para Ativar/Desativar Etapas
normalizar (padrão: True): Aplica a normalização ao texto para padronizar variações informais utilizando ferramenta enelvo.

substituir_emojis (padrão: True): Substitui emojis por rótulos sentimentais.

substituir_users (padrão: True): Remove menções a usuários (exemplo: @usuario).

remover_urls (padrão: True): Remove URLs do texto.

converter_ascii (padrão: True): Converte caracteres especiais para ASCII.

remover_pontuacao (padrão: True): Remove pontuações não associadas a números.

tokenizar_texto (padrão: True): (Novo) Tokeniza o texto, remove stopwords e tokens não-alfabéticos.

Funções do Pipeline
1. substitui_emoji(text)
Substitui os emojis por rótulos sentimentais (emojipositivo, emojinegativo, emojineutro) ou descrições Unicode.

Parâmetros: text (str): Texto no qual os emojis serão substituídos.

Retorno: Texto com emojis substituídos.

Python

def substitui_emoji(text):
    """
    Substitui emojis em um texto por rótulos de sentimento ou descrições de emojis.

    Parâmetros:
    text (str): O texto no qual os emojis serão substituídos.

    Retorna:
    str: O texto com os emojis substituídos por rótulos de sentimentos ou descrições Unicode.
    """
     
    for emoji, label in emoji_list.items():
        text = text.replace(emoji, label)
    dem = demoji.findall(text)
    for item, value in dem.items():
        text = text.replace(item, f" {value.replace(' ', '')}")
    return text
2. tokenizar_e_limpar_texto(text) (Nova Função)
Remove as stopwords presentes no texto e filtra tokens não-alfabéticos, utilizando a biblioteca NLTK.

Parâmetros: text (str): O texto no qual as stopwords serão removidas.

Retorno: list: Uma lista de tokens (palavras) filtrados.

Python

def tokenizar_e_limpar_texto(text):
  """
  Remove as stopwords presente no texto, através da biblioteca NLTK

  Parâmetros:
  text (str): O texto no qual as stopwords serão removidas.

  Retorna:
  str: O texto sem as stop words previamente removidas.
  """
  text = text.lower()
  tokens = word_tokenize(text, langauge='portuguese') # Nota: 'langauge' é um typo no código original
  tokens_filtrados = [
    palavra for palavra in tokens
    if palavra.isalpha() and palavra.lower() not in stopwords_pt
  ]

  return tokens_filtrados
3. preprocess(texto, normalizar=True, substituir_emojis=True, ...)
Aplica o pipeline de pré-processamento ao texto com diversas etapas opcionais, agora incluindo tokenizar_texto.

Parâmetros:

texto (pd.Series): Série Pandas contendo os textos a serem processados.

normalizar (bool): Substitui vírgulas temporariamente e normaliza o texto com a ferramenta enelvo.

substituir_emojis (bool): Substitui emojis por rótulos sentimentais.

substituir_users (bool): Remove menções a usuários.

remover_urls (bool): Remove URLs do texto.

converter_ascii (bool): Converte caracteres especiais para ASCII.

remover_pontuacao (bool): Remove pontuações não associadas a números.

tokenizar_texto (bool): (Novo) Tokeniza o texto e remove stopwords.

Retorno: Série Pandas com o texto pré-processado.

Python

def preprocess(texto, normalizar=True, substituir_emojis=True, substituir_users=True, remover_urls=True, converter_ascii=True, remover_pontuacao=True, tokenizar_texto=True):
    """
    Aplica o pipeline de pré-processamento ao texto fornecido.

    Parâmetros:
    texto (pd.Series): Uma série pandas contendo os textos a serem processados.
    normalizar (bool): Normaliza o texto usando o enelvo. Padrão: True.
    substituir_emojis (bool): Substitui emojis por rótulos de sentimentos. Padrão: True.
    substituir_users (bool): Remove menções a usuários no formato @usuario. Padrão: True.
    remover_urls (bool): Remove URLs do texto. Padrão: True.
    converter_ascii (bool): Converte caracteres especiais para ASCII. Padrão: True.
    remover_pontuacao (bool): Remove pontuações desnecessárias. Padrão: True.
    tokenizar_texto (bool): Tokeniza e remove stopwords. Padrão: True.

    Retorna:
    pd.Series: Uma série pandas com o texto pré-processado.
    """

    # Substituindo users
    if substituir_users:
        texto = texto.str.replace(r'@\w+', '')

    # Removendo URLs
    if remover_urls:
        texto = texto.apply(lambda x: re.sub(r'http\S+', '', x))

    # Substituindo vírgulas por "chavevirg"
    if normalizar:
        texto = texto.str.replace(r',', 'chavevirg')

    # Normalizando texto (enelvo)
    if normalizar:
        texto = texto.apply(lambda x: normalizador.normalise(x))

    # Substituindo emojis
    if substituir_emojis:
        texto = texto.apply(substitui_emoji)

    # Revertendo substituição de vírgulas
    if normalizar:
        texto = texto.str.replace(r'chavevirg', ',')

    # Convertendo para ASCII
    if converter_ascii:
        texto = texto.apply(lambda x: unidecode(x))

    # Removendo vírgulas não associadas a números e outras pontuações
    if remover_pontuacao:
        texto = texto.apply(lambda x: re.sub(r'(?<!\d),(?=\D)|(?<=\D),(?!\d)|(?<!\d),(?=\d)|(?<!\d)\/|\/(?!\d)|_|[^\w#\/\s,\@]','', x))

    if tokenizar_texto:
        texto = texto.apply(tokenizar_e_limpar_texto)

    return texto
4. pipeline_export(df, coluna, formato='json', **kwargs)
Aplica o pré-processamento em uma coluna de um DataFrame e exporta os dados processados.

Parâmetros:

df (pd.DataFrame): DataFrame original contendo os textos.

coluna (str): Nome da coluna que será processada.

formato (str): Formato de exportação (json ou csv).

**kwargs: Parâmetros opcionais para as etapas de pré-processamento.

Retorno:

DataFrame original com uma nova coluna texto_preprocessado.

Python

def pipeline_export(df, coluna, formato='json', **kwargs):
    """
    Aplica o pré-processamento em uma coluna do DataFrame e exporta o DataFrame modificado.

    Parâmetros:
    df (pd.DataFrame): O DataFrame original contendo os dados.
    coluna (str): Nome da coluna que será processada.
    formato (str): Formato de exportação dos dados ('json' ou 'csv'). Padrão: 'json'.
    **kwargs: Parâmetros opcionais para as etapas do pré-processamento.

    Retorna:
    pd.DataFrame: O DataFrame original com uma nova coluna chamada 'texto_preprocessado'.
    """

    df['texto_preprocessado'] = preprocess(df[coluna], **kwargs)

    # Exportar para o formato escolhido
    if formato == 'json':
        df.to_json('saida_preprocessada.json', orient='records', lines=True, force_ascii=False)
    elif formato == 'csv':
        df.to_csv('saida_preprocessada.csv', index=False)
    else:
        print(f"Formato {formato} não é suportado.")
    
    return df  # Retorna o DataFrame original com a nova coluna
5. pipeline(caminho_arquivo, coluna, formato='csv', **kwargs)
Função principal que aplica o pipeline ao arquivo fornecido e exporta o resultado.

Parâmetros:

caminho_arquivo (str): Caminho do arquivo a ser processado (.csv ou .json).

coluna (str): Nome da coluna a ser processada.

formato (str): Formato de exportação (csv ou json).

**kwargs: Parâmetros opcionais para as etapas de pré-processamento.

Retorno:

Exibe o DataFrame modificado após o processamento e exportação.

Python

def pipeline(caminho_arquivo, coluna, formato='csv', **kwargs):
    """
    Função principal que aplica o pipeline de pré-processamento ao arquivo fornecido.

    Parâmetros:
    caminho_arquivo (str): Caminho para o arquivo a ser processado (.csv ou .json).
    coluna (str): Nome da coluna que será processada no DataFrame.
    formato (str): Formato de exportação dos dados ('json' ou 'csv'). Padrão: 'csv'.
    **kwargs: Parâmetros opcionais para as etapas do pré-processamento.

    Retorna:
    None: Exibe o DataFrame modificado após o processamento e exportação.
    """

    # Verificar a extensão do arquivo para carregar o DataFrame corretamente
    if caminho_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho_arquivo)
    elif caminho_arquivo.endswith('.json'):
        df = pd.read_json(caminho_arquivo, lines=True)
    else:
        raise ValueError("Formato de arquivo não suportado. Use um arquivo .csv ou .json")
    
    # Aplicar o pipeline e exportar
    df_modificado = pipeline_export(df, coluna, formato, **kwargs)
    
    # Exibir o DataFrame modificado
    print(df_modificado)
Estrutura de Saída
O pipeline cria uma nova coluna chamada texto_preprocessado no DataFrame original e exporta o resultado em um dos seguintes formatos:

JSON

CSV

Para escolher o formato de saída, utilize o parâmetro formato ao chamar a função pipeline ou pipeline_export. Defina formato='json' para exportar como JSON ou formato='csv' para CSV.

Python

from pipeline import pipeline

# Executa o pipeline e exporta o resultado em formato CSV
pipeline('dados.csv', 'texto', formato='csv')
Detalhes do Pré-processamento de Texto
(Ordem atualizada para v3)

1. Remoção de Usuários
O código realiza a remoção de menções a usuários no formato @usuário.

Python

texto = texto.str.replace(r'@\w+', '')
2. Remoção de URLs
Qualquer URL presente no texto é removida usando uma expressão regular que identifica padrões de URLs, começando com "http".

Python

texto = texto.apply(lambda x: re.sub(r'http\S+', '', x))
3. Substituição de Vírgulas
Nesta etapa, todas as vírgulas no texto são temporariamente substituídas por "chavevirg". Isso é feito para contornar a ferramenta Enelvo, que separa números com vírgula durante a normalização. A substituição temporária facilita a manutenção da integridade dos dados numéricos e é revertida posteriormente.

Python

texto = texto.str.replace(r',', 'chavevirg')
4. Normalização Enelvo
O próximo passo é a utilização da biblioteca Enelvo, que envolve a normalização de erros ortográficos, gírias da internet, siglas, nomes próprios e outros.

Python

texto = texto.apply(lambda x: normalizador.normalise(x))
Exemplo:
Entrada: ['testeee', 'ururguau', 'disculpa qq coisa!', "Vc eh muitooooo legal", "Oii, To trabahlando hj"]

Saídas: ['teste', 'uruguai', 'desculpa qualquer coisa', 'você é muito legal', 'oii to trabalhando hoje']

5. Substituição de Emojis
Neste passo, o código realiza a substituição de emojis por rótulos específicos (incluindo o novo 'XD'). Também utilizamos a biblioteca demoji para substituir emojis Unicode por suas descrições.

Python

texto = texto.apply(substitui_emoji)
Exemplo:
Entrada: ['😀', '😋', ':)', ':(', 'XD', '🤢', "😺", "🎂"]

Saídas: ['grinningface', 'facesavoringfood', 'emojipositivo', 'emojinegativo', 'emojipositivo', 'nauseatedface', 'grinningcat', 'birthdaycake']

6. Reversão da Substituição de Vírgulas
Após a normalização, o código reverterá a substituição anterior de vírgulas por 'chavevirg', restaurando-as ao seu estado original.

Python

texto = texto.str.replace(r'chavevirg', ',')
7. Conversão para ASCII
Converte caracteres especiais para ASCII.

Python

texto = texto.apply(lambda x: unidecode(x))
8. Remoção de Pontuações e Caracteres Especiais
Este passo envolve a remoção de pontuações e caracteres especiais do texto, exceto quando esses caracteres são parte de hashtags, datas ou números com vírgulas.

Python

texto = texto.apply(lambda x: re.sub(r'(?<!\d),(?=\D)|(?<=\D),(?!\d)|(?<!\d),(?=\d)|(?<!\d)\/|\/(?!\d)|_|[^\w#\/\s,\@]','', x))
9. Tokenização e Remoção de Stopwords (Novo)
Se tokenizar_texto=True, o texto passa pela função tokenizar_e_limpar_texto. Isso envolve:

Converter o texto para minúsculas.

Tokenizar (dividir) o texto em palavras individuais.

Remover tokens que não são puramente alfabéticos.

Remover stopwords em português (ex: 'de', 'a', 'o', 'que', 'e').

O resultado final na coluna texto_preprocessado será uma lista de tokens (palavras), e não mais uma string contínua.

Python

if tokenizar_texto:
    texto = texto.apply(tokenizar_e_limpar_texto)
Exemplo:
Entrada (após etapas anteriores): 'ola tudo bem com voce eu estou otimo'

Saída: ['ola', 'tudo', 'bem', 'voce', 'eu', 'estou', 'otimo'] (Nota: 'com' seria removido se estivesse na lista de stopwords do NLTK).

Testes
<img src="https://github.com/ciberdem/ProjetoHEIWA-FAPESP/blob/main/CuradoriaExtracaoDados/pipeline_v2/assets/ex_teste_plv2.png" alt="Exemplo de saída de execução do código">
