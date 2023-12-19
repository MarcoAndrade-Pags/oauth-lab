
Esta abordagem é bastante complexa e exige multiplos fluxos de autenticação e concessão de acesso.


@startuml "Authorization-code"
actor "Resource Owner"
participant "User Agent" as UA
participant "Authorization Server" as AS
participant "Client Application" as CA
participant "Resource Server" as RS

"Resource Owner" -> UA: Acessa a aplicação client
UA -> CA: Redirect url authorizacao do AS
CA -> AS: Requisita uma auth de acesso ao RS
AS -> "Resource Owner": Exibe tela de login
"Resource Owner" -> AS: Fornece as credenciais de authenticacao
AS -> "Resource Owner": Exibe a tela de consentimento de acesso ao RS
"Resource Owner" -> AS: Concede o consentimento
AS -> CA: Retorna um código de autorização
CA -> AS: Requisita um token de acesso, fornecendo o codigo de autorização
AS -> CA: Retorna um token de acesso
CA -> RS: Requisita um recurso protegido, fornecendo o token de acesso
RS -> CA: Retorna o recurso protegido
@enduml

