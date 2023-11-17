from flask import Flask, request
import requests, json, os

app = Flask(__name__)

kongAdmin = os.getenv('KONG_ADMIN', 'http://kong:8001')

@app.route("/")
def home_route():
    Result = [ "<table><tr><th>Key</th><th>Value</th></tr>" ]
    for key, value in request.headers.items():
        Result.append(f"<tr><td>{key}</td><td>{value}</td></tr>")
    Result.append("</table><pre>")

    if request.headers.get('Authorization'):
        Result.append('Authorization')
        Result.append(request.headers.get('Authorization'))
    else:
        Result.append("NoAuth header")

    for key in [ 'apikey', 'Apikey' ]:

        apiKey=request.headers.get(key)
        if apiKey:
            Result.append(f"<font color=red>Auth recebida {key} !!!</font> Revise <i>hide_credentials</i>")
            break


    if not request.headers.get('X-Consumer-Id') and not request.headers.get('X-Consumer-Custom-Id'):
        Result.append(f"<font color=red>X-Consumer-Id/X-Consumer-Custom-Id ausentes!!!</font> Revise dependencia entre service e <i>plugins</i>")
    
    else:
            # Este acesso é opcional.
            #  Validacao de Credential-ID

            credentialId=request.headers.get('X-Credential-Identifier')
            consumerCustomId=request.headers.get('X-Consumer-Custom-Id')
            consumerId=request.headers.get('X-Consumer-Id')
            if consumerId and credentialId:
                url = f"{kongAdmin}/consumers/{consumerId}/key-auth/{credentialId}"
                response = requests.request("GET", url)
                if response.status_code == 200:
                    Result.append("X-Consumer-Id/X-Credential-Identifier validado")
                else:
                    Result.append("X-Consumer-Id/X-Credential-Identifier <b>invalido</b>")
            if credentialId:
                url = f"{kongAdmin}/key-auths/{credentialId}/consumer"
                response = requests.request("GET", url)
                if response.status_code == 200:
                    Result.append("X-Credential-Identifier validado")
                else:
                    Result.append("X-Credential-Identifier <b>invalido</b>")
            if consumerId and consumerCustomId:
                valid = False
                url = f"{kongAdmin}/consumers/{consumerId}"
                response = requests.request("GET", url)
                if response.status_code == 200:
                    data = response.json()
                    valid = 'custom_id' in data and data['custom_id'] == consumerCustomId

                if valid:
                    Result.append("X-Consumer-Id/X-Credential-Identifier validado")
                else:
                    Result.append("X-Consumer-Id/X-Credential-Identifier <b>invalido</b>")



    return "\n".join(Result), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
