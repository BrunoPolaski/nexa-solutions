from django.urls import reverse
from rest_framework import status as http
from rest_framework.test import APITestCase

from .models import Chamado


class ChamadoCriacaoTests(APITestCase):
    """INC-01 — o título é obrigatório e dado inválido devolve 400, nunca 500."""

    def setUp(self):
        self.url = reverse("chamado-list-create")

    def test_cria_chamado_valido(self):
        resposta = self.client.post(
            self.url,
            {"titulo": "Impressora sem tinta", "descricao": "Setor financeiro"},
            format="json",
        )

        self.assertEqual(resposta.status_code, http.HTTP_201_CREATED)
        self.assertEqual(Chamado.objects.count(), 1)

        chamado = Chamado.objects.get()
        self.assertEqual(chamado.titulo, "Impressora sem tinta")
        # Status não informado deve assumir o padrão do modelo.
        self.assertEqual(chamado.status, Chamado.Status.ABERTO)

    def test_nao_cria_chamado_sem_titulo(self):
        resposta = self.client.post(
            self.url, {"descricao": "Chamado sem título"}, format="json"
        )

        self.assertEqual(resposta.status_code, http.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", resposta.data)
        self.assertEqual(str(resposta.data["titulo"][0]), "O título é obrigatório.")
        self.assertEqual(Chamado.objects.count(), 0)

    def test_nao_cria_chamado_com_titulo_vazio(self):
        resposta = self.client.post(
            self.url, {"titulo": "", "descricao": "x"}, format="json"
        )

        self.assertEqual(resposta.status_code, http.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chamado.objects.count(), 0)

    def test_nao_cria_chamado_com_titulo_apenas_espacos(self):
        resposta = self.client.post(
            self.url, {"titulo": "    ", "descricao": "x"}, format="json"
        )

        self.assertEqual(resposta.status_code, http.HTTP_400_BAD_REQUEST)
        self.assertEqual(Chamado.objects.count(), 0)


class ChamadoFiltroStatusTests(APITestCase):
    """INC-02 — filtro por status na listagem."""

    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("chamado-list-create")
        Chamado.objects.create(titulo="Rede lenta", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="VPN caiu", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="Troca de HD", status=Chamado.Status.EM_ANDAMENTO)
        Chamado.objects.create(titulo="Reset de senha", status=Chamado.Status.CONCLUIDO)

    def test_lista_todos_sem_filtro(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, http.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 4)

    def test_filtra_por_status(self):
        resposta = self.client.get(self.url, {"status": "ABERTO"})

        self.assertEqual(resposta.status_code, http.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 2)
        self.assertTrue(
            all(item["status"] == "ABERTO" for item in resposta.data),
            "A listagem filtrada retornou chamados de outro status.",
        )

    def test_filtro_aceita_valor_em_minusculas(self):
        resposta = self.client.get(self.url, {"status": "concluido"})

        self.assertEqual(resposta.status_code, http.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)

    def test_filtro_invalido_retorna_400(self):
        resposta = self.client.get(self.url, {"status": "NAO_EXISTE"})

        self.assertEqual(resposta.status_code, http.HTTP_400_BAD_REQUEST)
        self.assertIn("status", resposta.data)

    def test_filtro_vazio_lista_todos(self):
        resposta = self.client.get(self.url, {"status": ""})

        self.assertEqual(resposta.status_code, http.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 4)


class IndicadoresTests(APITestCase):
    """INC-06 — indicadores de volume de chamados."""

    def setUp(self):
        self.url = reverse("indicadores")

    def test_indicadores_sem_chamados(self):
        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, http.HTTP_200_OK)
        self.assertEqual(
            resposta.data,
            {"total": 0, "abertos": 0, "em_andamento": 0, "concluidos": 0},
        )

    def test_indicadores_contam_por_status(self):
        Chamado.objects.create(titulo="A", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="B", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="C", status=Chamado.Status.EM_ANDAMENTO)
        Chamado.objects.create(titulo="D", status=Chamado.Status.CONCLUIDO)

        resposta = self.client.get(self.url)

        self.assertEqual(resposta.status_code, http.HTTP_200_OK)
        self.assertEqual(
            resposta.data,
            {"total": 4, "abertos": 2, "em_andamento": 1, "concluidos": 1},
        )
