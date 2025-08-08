from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from app.application.tool import get_budget_info
import logging
import os

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

    def _create_budget_agent(self):
        """
        Cria o agente de orçamento.
        """

        return create_react_agent(
            model=self.model,
            tools=[get_budget_info],
            prompt=(
                "Você é um especialista em orçamentos da Dr. Sofá. "
                "Seu objetivo é criar orçamentos personalizados para clientes. "
                "Use a tool get_budget_info para buscar preços de serviços específicos. "
                "Sempre forneça informações claras sobre valores padrão e mínimos. "
                "Seja prestativo e detalhado nas suas respostas sobre serviços e preços."
            ),
            name="budget_agent"
        )

    def build(self):
        """
        Constrói o agente de orçamento.
        """

        budget_agent = self._create_budget_agent()

        supervisor = create_supervisor(
            agents=[budget_agent],
            model=self.model,
            prompt=(
                "Você é um supervisor de agentes de orçamento da Dr. Sofá. "
                "Seu objetivo é supervisionar o agente de orçamento para garantir "
                "que forneça informações precisas e completas sobre preços e serviços. "
                "Certifique-se de que o agente use as tools disponíveis adequadamente."
            )
        )

        logger.info("Agente de orçamento construído com sucesso")

        return supervisor

    def compile(self):
        """
        Compila o agente de orçamento.
        """

        compiled_supervisor = self.build().compile()

        logger.info("Agente de orçamento compilado com sucesso")

        return compiled_supervisor
