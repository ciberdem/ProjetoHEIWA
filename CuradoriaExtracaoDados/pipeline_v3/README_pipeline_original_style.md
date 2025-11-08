# 🧠 Pipeline de Pré-processamento de Texto

O **Pipeline de Pré-processamento de Texto** tem como objetivo padronizar e preparar dados textuais para aplicações em **Processamento de Linguagem Natural (PLN)**, aplicando uma sequência de transformações que facilitam o uso de modelos de aprendizado de máquina.

---

## 🧩 Etapas do Pipeline

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

---

## ⚙️ Executando o Pipeline

### 1. Instale as dependências

```bash
pip install pandas nltk unidecode
```

### 2. Baixe os recursos necessários do NLTK (apenas na primeira execução)

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt')
```

### 3. Execute o pipeline

```python
from pipeline import preprocess_texts

texts = ["Esse filme é mt bom!", "vc viu o q aconteceu ontem?"]
processed = preprocess_texts(texts)
print(processed)
```

---

## 🧪 Exemplo de Uso

**Entrada:**
```python
["Vc viu o q rolou hj?", "Esse filme é mt bom!!"]
```

**Saída esperada:**
```python
["você ver o que acontecer hoje", "esse filme muito bom"]
```

---

## 📊 Estrutura do Projeto

```
📦 projeto_pipeline
 ┣ 📜 pipeline.py
 ┣ 📜 README.md
 ┗ 📂 assets
    ┗ diagrama.png
```

---

## 📘 Diagrama do Processo

![Diagrama do Pipeline](assets/diagrama.png)

---

## 🧠 Observações

- Pode ser adaptado para outros idiomas ajustando as stopwords e o mapeamento de gírias.  
- Ideal para **análises de sentimento**, **classificação de textos** e **limpeza de bases linguísticas**.

---

## ✨ Autor

Desenvolvido por **João Pedro**  
Com foco em **clareza, modularidade e reutilização de código**.
