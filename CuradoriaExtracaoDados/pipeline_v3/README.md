# Pipeline de Pré-processamento de Texto

O **Pipeline de Pré-processamento de Texto** tem como objetivo padronizar e preparar dados textuais para aplicações em **Processamento de Linguagem Natural (PLN)**, aplicando uma sequência de transformações que facilitam o uso de modelos de aprendizado de máquina.

---
# Conteúdo

- [Como Utilizar](#como-utilizar)
  - [Dependências](dependencias)
    - [Instalação das Dependências](instalação-de-dependências)
  - [Executando o Pipeline](executando-o-pipeline)
    - [Exemplo de Uso](exemplo-de-uso)
- [Funcionalidades](#funcionalidades)
  - [Parâmetros para Ativar/Desativar Etapas](parâmetros-para-ativar/desativar-etapas)
- [Funções do Pipeline](funções-do-peipeline)
- [Estrutura de Saída](estrutura-de-saída)
- [Detalhes do Pré-processamento de Texto](#detalhes-do-pré-processamento-de-texto)

---

# Como Utilizar

## Dependências
Antes de executar o pipeline, certifique-se de ter as seguintes bibliotecas instaladas:

- demoji: https://pypi.org/project/demoji/
- pandas: https://pypi.org/project/pandas/
- nltk: https://pypi.org/project/nltk/
- enelvo: https://pypi.org/project/enelvo/
- unidecode: https://pypi.org/project/Unidecode/

### Instalação das Dependências

Para instalar todas as dependências, utilize o arquivo requirements.txt. Com o arquivo pronto, basta executar o comando:

```python
pip install -r /path/to/requirements.txt
```

Após a instalação das bibliotecas, é necessário baixar alguns conteúdos adicionais para do NLTK para que o pipelone funcione corretamente. 

```python
import nltk

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
```

## Executando o Pipeline

- **Arquivo de entrada**: O pipeline aceita arquivos nos formatos `.csv` ou `.json`. O caminho do arquivo de entrada e o nome da coluna que contém o texto a ser processado devem ser fornecidos.
- **Processamento**: O pipeline pode ser executado por meio da função pipeline. Ela carrega o arquivo, aplica o pré-processamento e exporta o resultado.

- **OBS**: Todas as etapas de pré-processamento são **opcionais** e podem ser ativadas ou desativadas conforme necessário ao chamar a função `pipeline`. Cada etapa é controlada por um parâmetro booleano (`True` para ativar e `False` para desativar).


### Exemplo de Uso

```python
from pipeline_de_limpeza import pipeline

caminho_arquivo = 'dados.csv'  # ou 'dados.json'
coluna = 'texto'
formato = 'json'

# Executando o pipeline
pipeline(caminho_arquivo, coluna, formato)
```

# Funcionalidades

O pipeline realiza as seguintes etapas principais:

1. **Normalização de Texto**  
   Conversão para letras minúsculas, remoção de acentuação, pontuação e espaços extras.

2. **Substituição de Gírias e Abreviações**  
   Converte termos informais para suas formas padrão, garantindo maior consistência semântica.

3. **Tokenização**  
   Separa o texto em palavras (tokens), facilitando o tratamento e análise.

4. **Remoção de Stopwords**  
   Elimina palavras sem relevância semântica, como artigos e preposições.

5. **Reconstrução do Texto**  
   Retorna o texto processado de forma limpa e padronizada.

Para desativar etapas específicas, basta definir o parâmetro desejado como `False` ao chamar a função `pipeline`. Por exemplo, para desativar a normalização e a remoção de URLs:

```python
from pipeline import pipeline

# Executa o pipeline sem normalizar o texto e sem remover URLs
pipeline('dados.csv', 'texto', formato='json', normalizar=False, remover_urls=False)
```


### Parâmetros para Ativar/Desativar Etapas

- `substituir_emojis` (padrão: `True`): Substitui emojis por rótulos sentimentais.
- `substituir_users` (padrão: `True`): Remove menções a usuários (exemplo: @usuario).
- `normalizar` (padrão: `True`): Aplica a normalização ao texto para padronizar variações informais utilizando ferramenta enelvo.
- `remover_urls` (padrão: `True`): Remove URLs do texto.
- `converter_ascii` (padrão: `True`): Converte caracteres especiais para ASCII.
- `remover_pontuacao` (padrão: `True`): Remove pontuações não associadas a números.


# Funções do Pipeline
## 1.substituir_girias(texto, dicionario_de_girias)
Substitui gírias em um texto com base em um dicionário, garantindo a substituição apenas de palavras inteiras e ignorando maiúsculas/minúsculas

**Parâmetros**:
`texto (str)`: Texto no qual os emojis serão substituídos.
`dicionario_de_girias (dict)`: Dicionário Python onde cada chave é uma gíria e cada valor é o significado “normalizado” dela.

**Retorno**:
Texto com as gírias substituidas por seu significado normaliizado. 

```python
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
```



## 2. `substitui_emoji(text)`
Substitui os emojis por rótulos sentimentais (emojipositivo, emojinegativo, emojineutro) ou descrições Unicode.

**Parâmetros**:
`text (str)`: Texto no qual os emojis serão substituídos.

**Retorno**:
Texto com emojis substituídos.

```python
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
```



## 3. `preprocess(texto, substituir_users=True, remover_urls=True, ...)`
Aplica o pipeline de pré-processamento ao texto com diversas etapas opcionais, como normalização, remoção de URLs e emojis.

**Parâmetros**:

-`texto (pd.Series)`: Série Pandas contendo os textos a serem processados.
-`substituir_users (bool)`: Substitui menções a usuários no formato @usuario por <user>, evitando que o Enelvo modifique esses elementos.
-`remover_urls (bool)`: Substitui links e URLs por <hyperlink> antes da normalização, garantindo consistência. (Padrão: True)
-`normalizar (bool)`: Aplica a normalização ao texto utilizando o Enelvo, que corrige gírias, abreviações e erros ortográficos, mantendo os placeholders <user> e <hyperlink>.
-`substituir_emojis (bool)`: Substitui emojis por rótulos sentimentais ou descrições textuais.
-`converter_ascii (bool)`: Converte caracteres especiais (acentos, cedilhas, etc.) para caracteres ASCII simples.
-`remover_pontuacao (bool)`: Remove pontuações e símbolos não associados a números, hashtags ou menções.
-`tokenizar_texto (bool)`: Tokeniza o texto em palavras, remove stopwords e retorna o texto limpo.

**Retorno**:
Série Pandas com o texto pré-processado.

```python
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
```



## 4. `pipeline_export(df, coluna, formato='json', **kwargs)`
Aplica o pré-processamento em uma coluna de um DataFrame e exporta os dados processados.

**Parâmetros**:

- `df (pd.DataFrame)`: DataFrame original contendo os textos.
- `coluna (str)`: Nome da coluna que será processada.
- `formato (str)`: Formato de exportação (json ou csv).
- `**kwargs`: Parâmetros opcionais para as etapas de pré-processamento.

**Retorno**:

DataFrame original com uma nova coluna `texto_preprocessado`.


```python
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
```



## 5. `pipeline(caminho_arquivo, coluna, formato='csv', **kwargs)` 
Função principal que aplica o pipeline ao arquivo fornecido e exporta o resultado.

**Parâmetros**:

- `caminho_arquivo (str)`: Caminho do arquivo a ser processado (.csv ou .json).
- `coluna (str)`: Nome da coluna a ser processada.
- `formato (str)`: Formato de exportação (csv ou json).
- `**kwargs`: Parâmetros opcionais para as etapas de pré-processamento.

**Retorno**:

Exibe o DataFrame modificado após o processamento e exportação.

```python
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
```

# Estrutura de Saída
O pipeline cria uma nova coluna chamada texto_preprocessado no DataFrame original e exporta o resultado em um dos seguintes formatos:

- `JSON`
- `CSV`

Para escolher o formato de saída, utilize o parâmetro `formato` ao chamar a função `pipeline` ou `pipeline_export`. Defina `formato='json'` para exportar como JSON ou `formato='csv'` para CSV.

```python
from pipeline import pipeline

# Executa o pipeline e exporta o resultado em formato CSV
pipeline('dados.csv', 'texto', formato='csv')
```


# Detalhes do Pré-processamento de Texto
## 1. Substituição de usuários (substituir_users)

Substitui menções a usuários no formato @usuario por um placeholder <user>. Fazer isso antes de normalizar evita que o normalizador altere os padrões @ e quebras na regex.

```python
if substituir_users:
    texto = texto.str.replace(r'@\w+', '<user>', regex=True)
```

Exemplo
Entrada: ["@joao gostei", "obrigado @maria!"]
Saída: ["<user> gostei", "obrigado <user>!"]

## 2. Substituição de URLs (remover_urls)

Substitui URLs por um placeholder <hyperlink> — feito cedo para evitar que normalizadores ou substituições subsequentes quebrem os links.

```python
if remover_urls:
    texto = texto.apply(lambda x: re.sub(r'http\S+', '<hyperlink>', x))
```

Exemplo
Entrada: ["veja http://ex.com", "link: https://site.com/test"]
Saída: ["veja <hyperlink>", "link: <hyperlink>"]

## 3. Substituição de gírias (substituir_girias)

Aplica o dicionário de gírias, substituindo apenas palavras inteiras (uso de \b), e usa ordenação por tamanho para evitar colisões (ex.: pq vs p).

```python
texto = texto.apply(lambda x: substituir_girias(x, dicionario_girias_completo))
```

Exemplo
Entrada: "vc ta mt loko hj"
Saída: "você ta muito louco hoje"

## 4. Normalização Enelvo (normalizar)

Aplica o normalizador.normalise(x) da biblioteca Enelvo para corrigir grafias, abreviações e variações coloquiais. Normalização vem após users/URLs/gírias para não atrapalhar placeholders.

```python
if normalizar:
    texto = texto.apply(lambda x: normalizador.normalise(x))
```

Exemplo
Entrada: "testeee q q rolou"
Saída: "teste que que rolou" (exemplo ilustrativo)

## 5. Substituição de emojis (substituir_emojis)

Substitui emojis por rótulos/descritivos (usa emoji_list + demoji), transformando símbolos em tokens textuais significativos.

```python
if substituir_emojis:
    texto = texto.apply(substitui_emoji)
```

Exemplo
Entrada: ["😀 que delicia", "tô triste 😢"]
Saída: ["emoji_feliz que delicia", "tô triste emoji_triste"]

## 6. Conversão para ASCII (converter_ascii)

Converte caracteres acentuados e especiais para representações ASCII com unidecode, evitando inconsistências entre acentuados e não acentuados.

```python
if converter_ascii:
    texto = texto.apply(lambda x: unidecode(x))
```

Exemplo
Entrada: "você está ótimo"
Saída: "voce esta otimo"

## 7. Remoção de pontuação e caracteres indesejados (remover_pontuacao)

Aplica expressão regular que remove pontuações e símbolos indesejados, mas tenta preservar hashtags, números relevantes e outros padrões esperados pelo seu pipeline (conforme a regex utilizada no código).

```python
if remover_pontuacao:
    texto = texto.apply(lambda x: re.sub(r'(?<!\d),(?=\D)|(?<=\D),(?!\d)|(?<!\d),(?=\d)|(?<!\d)\/|\/(?!\d)|_|[^\w#\/\s,\@]','', x))
```

Exemplo
Entrada: "Olá!!! Tá, 100% (teste) ~"
Saída: "Olá Tá 100 teste "

## 8. Tokenização e limpeza final (tokenizar_texto)

Se ativada, a função tokenizar_e_limpar_texto é aplicada — geralmente faz tokenização (por NLTK ou split), remoção de stopwords, limpeza de tokens vazios e possivelmente lematização/stem (depende da implementação interna dessa função).

```python
if tokenizar_texto:
    texto = texto.apply(tokenizar_e_limpar_texto)
```

Exemplo
Entrada (após limpezas): "este é um texto de teste"
Saída: ["texto", "teste"] (exemplo ilustrativo — formato pode ser lista de tokens ou string, dependendo da função)

---

## Diagrama do Processo

![Diagrama do Pipeline](assets/diagrama.png)

---

## Observações

- Pode ser adaptado para outros idiomas ajustando as stopwords e o mapeamento de gírias.  
- Ideal para **análises de sentimento**, **classificação de textos** e **limpeza de bases linguísticas**.

---

## Teste


---

## Autor

Desenvolvido por **João Pedro Honorato**  
