from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado

        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]

        # O título é obrigatório. Sem `allow_blank`, o DRF também rejeita
        # strings vazias e compostas apenas de espaços (trim_whitespace é o
        # padrão), respondendo 400 com a mensagem abaixo.
        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
                "error_messages": {
                    "required": "O título é obrigatório.",
                    "blank": "O título é obrigatório.",
                    "null": "O título é obrigatório.",
                },
            },
        }

        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]
