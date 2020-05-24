# FDTD-tline

Repositório do 1º projeto da disciplina SEL0612 - Ondas Eletromagnéticas, cujo objetivo é estudar o método de análise de dados FDTD (finite-difference time-domain), e observar o comportamento das propriedades físicas de uma linha de transmissão, e como as propriedades intrínsecas de uma linha (Resistência, Condutância, Indutância e Capacitância) afetam a forma da onda de transmissão de corrente e tensão, através do comprimento da linha, do gerador à carga, e também em sentido oposto. 

## Descrição do Repositório
- ```FDTD.py```: arquivo contendo o código proposto para simulação.
- ```Videos```: contêm videos de simulações.
- ```Images```: contêm imagens de simulações.
- ```Project1.pdf```: descrição do projeto proposto.
- ```Trabalho_1_Ondas___SEL0612.pdf```: relatório do projeto.
- ```requirements.txt```: arquivo contendo as bibliotecas de python exigidas para a execução

## Requerimentos
- Interpretador de Python 3
- Instalar as libs descritas em: ```requirements.txt``` (arquivo gerado utilizando a ferramenta pipreqs)

## Funcionamento
- Executrar o código no terminal:
```
python FDTD.py
```
- Listar os argumentos através do ```-help```:
```
python FDTD.py -h
```
- Lista de argumentos:

```"-s" ou "--source"```: Escolhe qual a fonte da simulação, sendo 0 a fonte 2*u(t) e 1 p/ a outra fonte. Default = 0;

```"-c" ou "--charge"```: Escolhe o valor da impedância da carga, em Ohms. Para simular um *circuito aberto*, utilizar um valor negativo para esse parâmetro. Default = 100;

```"-k" ou "--K"```: Escolhe o número de divisões no comprimento. Default = 500;

```"-r" ou "--reflections"```: Escolhe o número de reflexões da onda, determinando o tempo total da simulação. Default = 10;
