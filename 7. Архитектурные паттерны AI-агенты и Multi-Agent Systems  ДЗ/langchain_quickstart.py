"""Учебный пример LangChain-агента для базы знаний архитектора.

Перед запуском установите зависимости и задайте ключ выбранного провайдера.
Модель можно изменить через переменную MODEL_NAME.
"""

import os

from langchain.agents import create_agent
from langchain.tools import tool


ARCHITECTURE_KB = {
    "c4": (
        "C4 описывает систему на уровнях System Context, Container, "
        "Component и Code. Источник: lesson-06-c4-model."
    ),
    "rag": (
        "RAG объединяет ingestion, retrieval, augmentation и generation. "
        "Источник: lesson-07-rag-pipeline."
    ),
}


@tool
def search_architecture_kb(query: str) -> str:
    """Найти подтверждённый фрагмент в учебной базе знаний архитектуры."""
    normalized = query.lower()
    matches = [text for key, text in ARCHITECTURE_KB.items() if key in normalized]
    if not matches:
        return "NO_EVIDENCE: подтверждённый материал не найден"
    return "\n".join(matches)


SYSTEM_PROMPT = """Ты — учебный помощник архитектора FATHER.
Для фактических утверждений сначала используй search_architecture_kb.
Не выдумывай источники. Если инструмент вернул NO_EVIDENCE, сообщи,
что подтверждённых данных недостаточно. В конце ответа укажи источник."""


def main() -> None:
    model_name = os.getenv("MODEL_NAME", "openai:gpt-5.5")
    agent = create_agent(
        model=model_name,
        tools=[search_architecture_kb],
        system_prompt=SYSTEM_PROMPT,
    )
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Объясни уровни C4 и укажи источник.",
                }
            ]
        }
    )
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
