# Malicious-DNS-Detection
<h5><p align="left"><br>
 <a href="#projeto">1. PROJETO</a><br>
 <a href="#tecnologias">2. TECNOLOGIAS</a><br>
 <a href="#autores">3. AUTORES</a><br>
 <a href="#autor">4. NÃO SEI</a><br>
</p></h5>

<h4><a name="projeto">1. PROJETO</a></h4>
Este projeto foi desenvolvido para fins avaliativas da disciplina de Ciência de Dados para Segurança, lecionada pelo professor doutor André Ricardo Grégio, do Curso de Mestrado em Informática da UFPR, no período de novembro de dezembro de 2021. O objetivo do projeto foi classificar nomes de domínios em benignos ou malignos utilizando algoritmos de aprendizado de máquina. O código-fonte fez parte do aprendizado dos autores e pode ser customizado, com os devidos ajustes, para outros usos.

O dataset coletado que embasou este trabalho está disponível em: https://www.unb.ca/cic/datasets/dns-2021.html

O trabalho seguiu os seguintes passos e etapas:


<blockquote>
ETAPA 1 : TRATAMENTO DOS DADOS
<ul>
<li>PASSO 1: [01] [01] Data Cleaning.ipynb. Limpeza dos dados, junção dos datasets limpos, redução da quantidade de classes de benignos.</li>
<li>PASSO 2: [01] [02] Gerador de Atributos.ipynb. Geração de atributos TLD, SLD, SSD, SUB. Definição das classes Benign = 0 e Malware = 1</li>
<li>PASSO 3: [01] [03] Obtendo Características de Terceiros.ipynb. Utilizando IP, whois, IPWhois.</li>
<li>PASSO 4: [01] [04] Balanceando os dados para 50 - 50.ipynb </li>
<li>Passo 5: [01] [05] Train Test Split.ipynb</li>
</ul>
</blockquote>

<blockquote>
ETAPA 2 : GERAÇÃO DE CARACTERÍSTICAS
<ul>
<li>PASSO 6: [02] [01] Gerador de Características de Terceiros.ipynb. Definindo Domínios famosos a partir do ranking Alexa. SLD, connection, SLDs in SUB, age, creation, org, registrant, registrar, servers, email, country, state, address, name, privacy, SLD Distance. </li>
<li>PASSO 7: [02] [02] Gerador de Características Lexicográficas.ipynb. Geração das características  SSD_len, SUB_len,SLD_len, SSD_pct, SUB_pct, SLD_pct, SSD_nan, SUB_nan, SLD_nan, SSD_etp, SUB_etp, SLD_etp, SUB_num.</li>
<li>PASSO 8: [02] [03] Gerador de Características Lexicográficas Part 2.ipynb. Dígitos sequenciais, caracteres sequenciais em SSD, SUB, SLD.</li>
<li>PASSO 9: [02] [04] Gerador de Características Lexicográficas Part 3.ipynb. Palavras comuns e famosas de sites famosos (words_reliable, words_catchy, words_countries, words_bad).</li>
<li>PASSO 10: [02] [05] Gerador de Características.ipynb. Características para pré-treino e pré-teste.</li>
</ul>
</blockquote>



<h4><h4><a name="tecnologias">2. TECNOLOGIAS</a></h4>
As tecnologias usadas no desenvolvimento foram:
<ul><li>Jupiter Notebook</li><li>Linguagem Python</li></ul>

<h4><a name="autores">3. AUTORES</a></h4>
Abner Fontebom Bissolli Costa (afbcosta@inf.ufpr.br) e Michele Venturin (mventurin@inf.ufpr.br)

