from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from app.application.tool import get_budget_info
import logging
import os
from langchain_core.messages import HumanMessage
from app.application.model.output import OutputBudget

logger = logging.getLogger(__name__)

class BudgetAgentBuilder:
    """
    Classe responsável por construir o agente de orçamento.
    """

    def __init__(self):
        """
        Inicializa o construtor do agente de orçamento.
        """

        self.model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY"),
        )

        self.agent = create_react_agent(
            model=self.model,
            tools=[get_budget_info],
            prompt=(
                "Você é um especialista em orçamentos da Dr. Sofá. "
                "Seu objetivo é criar orçamentos personalizados para clientes. "
                "IMPORTANTE: Use a tool get_budget_info APENAS UMA VEZ com a consulta completa do usuário. "
                "NÃO faça múltiplas buscas separadas. "
                "Consolide todas as informações em uma única consulta eficiente. "
                "Sempre forneça informações claras sobre valores padrão e mínimos. "
                "IMPORTANTE:"
                    "Se a entrada do usuário for algo relacionado a Impermeabilização de algum produto, atualize o campo requested_service_id do state com o id 3. "
                    "Se a entrada do usuário for algo relacionado a limpeza, atualize o campo requested_service_id do state com o id 2."
                    "Qualquer outra entrada, atualize o campo requested_service_id do state com o id 1."
                "Identifique a palavra chave que é o movel que o usuário precisa limpar ou impermeabilizar da consulta do usuário e atualize o campo key_words do state com a lista de palavras chaves."
                "Nao inclua o tipo de serviço como key_words, apenas as palavras chaves do produto que o usuário precisa limpar ou impermeabilizar."
                "Seja prestativo e detalhado nas suas respostas sobre serviços e preços."
                "Nao altere a estrutura do state nem os dados do state, apenas atualize os campos necessários."
            ),
            response_format=OutputBudget,
            name="budget_agent"
        )

    async def process_budget_agent(self, message: str):
        """
        Processa o agente de orçamento de forma assíncrona.
        """

        state_initial = {"messages": [HumanMessage(content=message)]}
        
        result = await self.agent.ainvoke(state_initial)

        return result["structured_response"]

    # def _create_budget_agent(self):
    #     """
    #     Cria o agente de orçamento.
    #     """

    #     return create_react_agent(
    #         model=self.model,
    #         tools=[get_budget_info],
    #         prompt=(
    #             "Você é um especialista em orçamentos da Dr. Sofá. "
    #             "Seu objetivo é criar orçamentos personalizados para clientes. "
    #             "Use a tool get_budget_info para buscar preços de serviços específicos. "
    #             # "Sempre forneça informações claras sobre valores padrão e mínimos. "
    #             # "Seja prestativo e detalhado nas suas respostas sobre serviços e preços."
    #         ),
    #         name="budget_agent"
    #     )

    # def build(self):
    #     """
    #     Constrói o agente de orçamento.
    #     """

    #     budget_agent = self._create_budget_agent()

    #     supervisor = create_supervisor(
    #         agents=[budget_agent],
    #         model=self.model,
    #         prompt=(
    #             "Você é um supervisor de agentes de orçamento da Dr. Sofá. "
    #             "Seu objetivo é supervisionar o agente de orçamento para garantir "
    #             "que forneça informações precisas e completas sobre preços e serviços. "
    #             "Certifique-se de que o agente use as tools disponíveis adequadamente."
    #         )
    #     )

    #     logger.info("Agente de orçamento construído com sucesso")

    #     return supervisor

    # def compile(self):
    #     """
    #     Compila o agente de orçamento.
    #     """

    #     compiled_supervisor = self.build().compile()

    #     logger.info("Agente de orçamento compilado com sucesso")

    #     return compiled_supervisor
