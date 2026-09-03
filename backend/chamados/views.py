from rest_framework import generics
from rest_framework.exceptions import ValidationError

from .models import Chamado
from .serializers import ChamadoSerializer


class ChamadoListCreateView(generics.ListCreateAPIView):
    """
    Lista e cria chamados.

    A listagem aceita o filtro opcional `?status=`, por exemplo:
    `GET /api/chamados/?status=ABERTO`.
    """

    serializer_class = ChamadoSerializer

    def get_queryset(self):
        chamados = Chamado.objects.all().order_by("-criado_em")

        status = self.request.query_params.get("status")
        if not status:
            return chamados

        status = status.strip().upper()
        if status not in Chamado.Status.values:
            raise ValidationError(
                {
                    "status": [
                        "Status inválido. Valores aceitos: "
                        + ", ".join(Chamado.Status.values)
                        + "."
                    ]
                }
            )

        return chamados.filter(status=status)


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer
