import json

# Define os tipos válidos de mensagens (pode ser expandido)
TIPOS_MENSAGEM = {
    "LOGIN",
    "CADASTRO",
    "CRIAR_LOJA",
    "CADASTRAR_PRODUTO",
    "LISTAR_PRODUTOS",
    "COMPRAR_PRODUTO",
    "RELATORIO",
    "ERRO",
    "SUCESSO"
}

# ===== Envia mensagens padronizadas =====

def criar_mensagem(tipo: str, dados: dict) -> bytes:
    """
    Cria uma mensagem formatada como JSON e codificada em bytes para envio.
    """
    if tipo not in TIPOS_MENSAGEM:
        raise ValueError(f"Tipo de mensagem '{tipo}' não é reconhecido.")
    
    estrutura = {
        "tipo": tipo,
        "dados": dados
    }
    try:
        return json.dumps(estrutura).encode("utf-8")
    except (TypeError, ValueError) as e:
        raise ValueError("Erro ao converter mensagem para JSON") from e


# ===== Recebe e interpreta mensagens =====

def interpretar_mensagem(mensagem_bytes: bytes) -> dict:
    """
    Converte uma mensagem recebida em bytes para dicionário Python.
    """
    try:
        decoded = mensagem_bytes.decode("utf-8")
        mensagem = json.loads(decoded)
        if "tipo" not in mensagem or "dados" not in mensagem:
            raise ValueError("Mensagem malformada: faltam campos obrigatórios")
        return mensagem
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
        raise ValueError("Erro ao interpretar mensagem recebida") from e


# ===== Criadores de mensagens de erro e sucesso =====

def mensagem_erro(motivo: str) -> bytes:
    return criar_mensagem("ERRO", {"motivo": motivo})

def mensagem_sucesso(resposta: dict = None) -> bytes:
    return criar_mensagem("SUCESSO", resposta or {})