# Pipeline de Limpeza de Dados v3


Executando o Pipeline
Arquivo de entrada: O pipeline aceita arquivos nos formatos .csv ou .json. O caminho do arquivo de entrada e o nome da coluna que contém o texto a ser processado devem ser fornecidos.

Processamento: O pipeline pode ser executado por meio da função pipeline. Ela carrega o arquivo, aplica o pré-processamento e exporta o resultado.

OBS: Todas as etapas de pré-processamento são opcionais e podem ser ativadas ou desativadas conforme necessário ao chamar a função pipeline. Cada etapa é controlada por um parâmetro booleano (True para ativar e False para desativar).

Exemplo de Uso
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

2. tokenizar_e_limpar_texto(text) (Nova Função)
Remove as stopwords presentes no texto e filtra tokens não-alfabéticos, utilizando a biblioteca NLTK.

Parâmetros: text (str): O texto no qual as stopwords serão removidas.

Retorno: list: Uma lista de tokens (palavras) filtrados.

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

4. pipeline_export(df, coluna, formato='json', **kwargs)
Aplica o pré-processamento em uma coluna de um DataFrame e exporta os dados processados.

Parâmetros:

df (pd.DataFrame): DataFrame original contendo os textos.

coluna (str): Nome da coluna que será processada.

formato (str): Formato de exportação (json ou csv).

**kwargs: Parâmetros opcionais para as etapas de pré-processamento.

Retorno:

DataFrame original com uma nova coluna texto_preprocessado.

5. pipeline(caminho_arquivo, coluna, formato='csv', **kwargs)
Função principal que aplica o pipeline ao arquivo fornecido e exporta o resultado.

Parâmetros:

caminho_arquivo (str): Caminho do arquivo a ser processado (.csv ou .json).

coluna (str): Nome da coluna a ser processada.

formato (str): Formato de exportação (csv ou json).

**kwargs: Parâmetros opcionais para as etapas de pré-processamento.

Retorno:

Exibe o DataFrame modificado após o processamento e exportação.

Estrutura de Saída
O pipeline cria uma nova coluna chamada texto_preprocessado no DataFrame original e exporta o resultado em um dos seguintes formatos:

JSON

CSV

Para escolher o formato de saída, utilize o parâmetro formato ao chamar a função pipeline ou pipeline_export. Defina formato='json' para exportar como JSON ou formato='csv' para CSV.

Detalhes do Pré-processamento de Texto
(Ordem atualizada para v3, seguindo o código)

1. Remoção de Usuários
O código realiza a remoção de menções a usuários no formato @usuário.

2. Remoção de URLs
Qualquer URL presente no texto é removida usando uma expressão regular que identifica padrões de URLs, começando com "http".

3. Substituição de Vírgulas (Temporária)
Nesta etapa, todas as vírgulas no texto são temporariamente substituídas por "chavevirg". Isso é feito para contornar a ferramenta Enelvo, que separa números com vírgula durante a normalização.

4. Normalização Enelvo
O próximo passo é a utilização da biblioteca Enelvo, que envolve a normalização de erros ortográficos, gírias da internet, siglas, nomes próprios e outros.

Exemplo:
Entrada: ['testeee', 'ururguau', 'disculpa qq coisa!', "Vc eh muitooooo legal", "Oii, To trabahlando hj"]

Saídas: ['teste', 'uruguai', 'desculpa qualquer coisa', 'você é muito legal', 'oii to trabalhando hoje']

5. Substituição de Emojis
Neste passo, o código realiza a substituição de emojis por rótulos específicos (incluindo o novo 'XD'). Também utilizamos a biblioteca demoji para substituir emojis Unicode por suas descrições.

Exemplo:
Entrada: ['😀', '😋', ':)', ':(', 'XD', '🤢', "😺", "🎂"]

Saídas: ['grinningface', 'facesavoringfood', 'emojipositivo', 'emojinegativo', 'emojipositivo', 'nauseatedface', 'grinningcat', 'birthdaycake']

6. Reversão da Substituição de Vírgulas
Após a normalização, o código reverterá a substituição anterior de vírgulas por 'chavevirg', restaurando-as ao seu estado original.

7. Conversão para ASCII
Converte caracteres especiais para ASCII.

8. Remoção de Pontuações e Caracteres Especiais
Este passo envolve a remoção de pontuações e caracteres especiais do texto, exceto quando esses caracteres são parte de hashtags, datas ou números com vírgulas.

9. Tokenização e Remoção de Stopwords (Novo)
Se tokenizar_texto=True (padrão), o texto passa pela função tokenizar_e_limpar_texto. Isso envolve:

Converter o texto para minúsculas.

Tokenizar (dividir) o texto em palavras individuais.

Remover tokens que não são puramente alfabéticos.

Remover stopwords em português (ex: 'de', 'a', 'o', 'que', 'e').

O resultado final na coluna texto_preprocessado será uma lista de tokens (palavras), e não mais uma string contínua.

Exemplo:
Entrada (após etapas anteriores): 'ola tudo bem com voce eu estou otimo'

Saída (como lista): ['ola', 'tudo', 'bem', 'voce', 'estou', 'otimo'] (Assumindo que 'com' e 'eu' estão nas stopwords).

Testes
