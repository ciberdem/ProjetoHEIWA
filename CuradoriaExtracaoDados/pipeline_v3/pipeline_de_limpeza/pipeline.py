import re
import demoji
import pandas as pd
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from enelvo import normaliser
from unidecode import unidecode

dicionario_girias_completo = {
    'cringe': 'vergonha alheia', 'tankar': 'aguentar', 'flopar': 'fracassar',
    'flopou': 'fracassou', 'hype': 'empolgação', 'hypar': 'empolgar',
    'hypado': 'empolgado', 'shippar': 'torcer por casal', 'biscoiteiro': 'chamar atenção',
    'biscoiteira': 'chamar atenção', 'fanficar': 'imaginar coisas', 'pov': 'ponto de vista',
    'bait': 'isca', 'baitar': 'provocar', 'random': 'aleatório', 'slay': 'arrasou',
    'delulu': 'delirante', 'red flag': 'sinal de alerta', 'f no chat': 'prestar respeito',
    'main character': 'personagem principal', 'mano': 'irmão', 'mana': 'irmã',
    'parça': 'parceiro', 'rolê': 'passeio', 'trampo': 'trabalho', 'trampar': 'trabalhar',
    'treta': 'briga', 'bagulho': 'coisa', 'daora': 'legal', 'dahora': 'legal',
    'busão': 'ônibus', 'perrengue': 'dificuldade', 'caô': 'mentira', 'mó': 'muito',
    'tá ligado': 'entende', 'ta ligado': 'entende', 'firmeza': 'combinado',
    'padoca': 'padaria', 'ranço': 'antipatia', 'sextou': 'comemorar sexta-feira',
    'tamo junto': 'conte comigo', 'tmj': 'conte comigo', 'deu ruim': 'deu errado',
    'deu bom': 'deu certo', 'nem a pau': 'de jeito nenhum', 'nem fudendo': 'de jeito nenhum',
    'pisar na bola': 'cometer um erro', 'chutar o balde': 'desistir de tudo',
    'viajar na maionese': 'falar algo sem sentido', 'segurar a onda': 'manter a calma',
    'mandar a real': 'falar a verdade', 'dar um perdido': 'sumir de propósito',
    'fazer uma vaquinha': 'juntar dinheiro em grupo', 'pagar de doido': 'se fazer de desentendido',
    'encher linguiça': 'falar coisas irrelevantes'
}

emoji_list = {
    ':))': 'emojipositivo',
    ':)': 'emojipositivo',
    ':d': 'emojipositivo',
    ':p': 'emojipositivo',
    'XD': 'emojipositivo',
    ':(': 'emojinegativo',
    ':((': 'emojinegativo',
    '8)': 'emojineutro'
}
normalizador = normaliser.Normaliser(tokenizer='readable')
stopwords_pt = set(stopwords.words('portuguese'))

def substituir_girias(texto, dicionario_de_girias):
    """
    Substitui gírias em um texto com base em um dicionário, garantindo a substituição
    apenas de palavras inteiras e ignorando maiúsculas/minúsculas.
    """
    sorted_girias = sorted(dicionario_de_girias.keys(), key=len, reverse=True)
    texto_processado = str(texto)
    for giria in sorted_girias:
        significado = dicionario_de_girias[giria]
        padrao = r'\b' + re.escape(giria) + r'\b'
        texto_processado = re.sub(padrao, significado, texto_processado, flags=re.IGNORECASE)
    return texto_processado

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

def tokenizar_e_limpar_texto(text):
    """
    Remove as stopwords presente no texto, através da biblioteca NLTK

    Parâmetros:
    text (str): O texto no qual as stopwords serão removidas.

    Retorna:
    str: O texto sem as stop words previamente removidas.
    """
    text = text.lower()
    tokens = word_tokenize(text, language='portuguese')
    tokens_filtrados = [
        palavra for palavra in tokens
        if palavra.isalpha() and palavra.lower() not in stopwords_pt
    ]
    return tokens_filtrados

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
    tokenizar_texto(bool): Tokeniza o texto e remove as stopwords. Padrão: True.

    Retorna:
    pd.Series: Uma série pandas com o texto pré-processado.
    """
    if substituir_users:
        texto = texto.str.replace(r'@\w+', '<user>', regex=True)

    if remover_urls:
        texto = texto.apply(lambda x: re.sub(r'http\S+', '<hyperlink>', x))

    texto = texto.apply(lambda x: substituir_girias(x, dicionario_girias_completo))

    if normalizar:
        texto = texto.apply(lambda x: normalizador.normalise(x))

    if substituir_emojis:
        texto = texto.apply(substitui_emoji)

    if converter_ascii:
        texto = texto.apply(lambda x: unidecode(x))

    if remover_pontuacao:
        texto = texto.apply(lambda x: re.sub(r'(?<!\d),(?=\D)|(?<=\D),(?!\d)|(?<!\d),(?=\d)|(?<!\d)\/|\/(?!\d)|_|[^\w#\/\s,\@]','', x))

    if tokenizar_texto:
        texto = texto.apply(tokenizar_e_limpar_texto)
        
    return texto

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
    if formato == 'json':
        df.to_json('saida_preprocessada.json', orient='records', lines=True, force_ascii=False)
    elif formato == 'csv':
        df.to_csv('saida_preprocessada.csv', index=False)
    else:
        print(f"Formato {formato} não é suportado.")
    return df

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
    if caminho_arquivo.endswith('.csv'):
        df = pd.read_csv(caminho_arquivo)
    elif caminho_arquivo.endswith('.json'):
        df = pd.read_json(caminho_arquivo, lines=True)
    else:
        raise ValueError("Formato de arquivo não suportado. Use um arquivo .csv ou .json")
    
    df_modificado = pipeline_export(df, coluna, formato, **kwargs)
    print(df_modificado)