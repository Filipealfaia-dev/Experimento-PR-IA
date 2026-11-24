def processar_pedido(itens, estoque, saldo_cliente,
                     cupom_percentual=0, cliente_vip=False):
    """
    Processa um pedido realizando:
    - cálculo do total
    - aplicação de cupom
    - desconto VIP
    - validação de estoque
    - redução de estoque
    - validação de saldo

    Parâmetros:
        itens: lista de dicionários contendo:
            {
                "produto": str,
                "preco": float,
                "quantidade": int
            }

        estoque: dicionário no formato:
            {
                "Produto A": 10,
                "Produto B": 5
            }

        saldo_cliente: valor disponível para compra
        cupom_percentual: percentual de desconto do cupom
        cliente_vip: True ou False

    Retorna:
        dicionário com resultado da operação
    """

    total = 0

    # Verifica estoque e calcula total
    for item in itens:
        produto = item["produto"]
        quantidade = item["quantidade"]
        preco = item["preco"]

        if produto not in estoque:
            return {
                "sucesso": False,
                "mensagem": f"Produto '{produto}' não encontrado no estoque."
            }

        if estoque[produto] < quantidade:
            return {
                "sucesso": False,
                "mensagem": (
                    f"Estoque insuficiente para '{produto}'. "
                    f"Disponível: {estoque[produto]}"
                )
            }

        total += preco * quantidade

    # Aplica cupom
    total *= (1 - cupom_percentual / 100)

    # Aplica desconto VIP adicional de 10%
    if cliente_vip:
        total *= 0.90

    total = round(total, 2)

    # Verifica saldo
    if saldo_cliente < total:
        return {
            "sucesso": False,
            "mensagem": "Saldo insuficiente.",
            "total": total,
            "saldo_cliente": saldo_cliente
        }

    # Reduz estoque
    for item in itens:
        estoque[item["produto"]] -= item["quantidade"]

    saldo_restante = round(saldo_cliente - total, 2)

    return {
        "sucesso": True,
        "mensagem": "Pedido processado com sucesso.",
        "total": total,
        "saldo_restante": saldo_restante,
        "estoque_atualizado": estoque
    }