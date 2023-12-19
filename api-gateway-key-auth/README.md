# API Gateway com Key AUTH

O objetivo é apresentar um cenario de uso com autenticação simples, com chaves estaticas e rotacionaveis através da troca de arquivos de config.

Pontos fortes:
- Implementa autenticação via API-Key sem implementação (exceto logs) na aplicação atendida.
- Permite uso de mais de uma credencial, dando tempo para que as aplicações tenham o Token atualizado.

Pontos fracos:
- A rotação de chaves requer reenvio de toda a configuração, gerando oscilação de disponibilidade.

## Executando o lab

docker compose -f kong-dbless.yaml up -d

Serão executados:

- kong API Gateway
  modo configuração hard-coded

- pod view para debug de headers
  O objetivo é simplesmente apresentar o header recebido


## Validando o lab

Importe no Postman o arquivo kong db-less.postman_collection.

Execute as requisições numeradas:
1. loadConfig restart

  Instala config basica, util para zerar setup em novos testes.


2. Consulta - sem rotas

  Vai retornar erro, pois não existem rotas configuradas neste momento


3. loadConfig Basic no Service

  Instala config com serviço basico, sem autenticacao

4. Consulta - headers sem autenticacao

  É dada notificação de ausencia dos headers, devido ao estágio de configuração.


5. reloadConfig Require auth

  Instala config completa, com dois tokens para um dos accounts.

6. Consulta - Sem token - negado acesso

  Primeiro acesso sem token valido, acesso negado.


7. Consulta - Sucesso Token1

  Autenticação com Token1, ativo


8. Consulta - Sucesso Token2

  Autenticação com Token2, ativo


9. reloadConfig Revoke Token1

  Sobe nova configuração, revogando o Token1

10. Consulta - Falha de acesso Token1 revogado

  Acesso negado, pois o Token1 foi desativado


## Conclusão

Nesta abordagem, incremental foi demonstrada uma hipotese para a coexistencia de 2 tokens para uma credencial, e a revogação.

O proposito é manter o mesmo identificador, e dar tempo para a rotação do segredo na aplicação.


```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```