#!/bin/sh

    LOGFILE=vault.log

    function log() {
        printf "%s %s\n" "$(date)" "$*"
    }


    LOG "Setup:"

    log "- VAULT_ADDR $VAULT_ADDR"
    log "- VAULT_TOKEN $VAULT_TOKEN"

    log "- Ativando PagVault / TokenAdmin KV-v2"
    vault secrets enable -path=pagvault -version=2 kv
    vault secrets enable -path=tokenAdmin -version=2 kv

    log "- Ativando approle:"
    vault auth enable approle

    log "- Criando Roles:"

    log "  - API-Server (api_server)"
    echo '
    # Backend Provider BackSample
    path "tokenAdmin/BackSample" {
        capabilities = [ "create", "read", "list", "update", "patch", "delete" ]
    }
    ' | vault policy write tokenAdmin/p-backSample -

    vault write auth/approle/role/backSample \
            token_policies="p-rol_unknown,tokenAdmin/p-backSample" \
            token_ttl=30d token_max_ttl=30d \
            token_type=batch


    for consumer in Client1 Client2 Client3; do
        # Gera token aleatorio
        Token="$(vault write -f sys/tools/random/76  | grep ^random | awk '{print $2}')"

        # Salva token para uso do provider
        vault kv put tokenAdmin/BackSample/provider/${consumer} token=$Token

        # Criar consumer
        pathPagVault=pagvault/data/topdomain/domain/default/${consumer}
        policyName="pol_rol_${consumer}"

        printf 'path "%s" { capabilities=["read"]}\n' $pathPagVault | 
            vault policy write ${policyName}

        vault write auth/approle/role/${consumer} \
                    bind_secret_id=false \
                    token_bound_cidrs=127.0.0.1/32 \
                    policies=${policyName}
        role_id=$(vault read auth/approle/role/${consumer}/role-id | grep ^role_id | awk '{print $2}')
        tokenConsumer=$(vault write auth/approle/login role_id=$role_id | grep ^token\  | awk '{print $2}')

        # Salva na area do Consumer
        vault kv put tokenAdmin/BackSample/provider/${consumer} token=$Token

    done




    #vault kv put -mount pagvault topdomain/domain/default/api_server/oauth client=api-server
    
