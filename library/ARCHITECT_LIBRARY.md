# Единая библиотека архитектора FATHER

Назначение библиотеки — не хранить пиратские копии книг, а связывать проверенные библиографические карточки, официальные источники, учебные конспекты, уроки OTUS, архитектурные решения и навыки агента.

## Приоритеты

- **P0 — ядро:** прочитать полностью или сделать подробный конспект.
- **P1 — рабочая полка:** читать по главам при прохождении соответствующего урока.
- **P2 — справочник:** обращаться по задаче.

## P0 — ядро архитектора

1. Саймон Браун. «Программная архитектура как код» — C4, Structurizr, архитектура как код. Уроки 4–5.
2. Марк Ричардс, Нил Форд. «Основы программной архитектуры» — стили, характеристики качества, компромиссы. Уроки 1–10.
3. Нил Форд и др. «Программная архитектура: трудные решения» — анализ компромиссов распределённых систем. Уроки 8–10, 21–24.
4. Мартин Клеппман, Крис Риккомини. *Designing Data-Intensive Applications*, 2-е изд. — данные, распределённые системы, надёжность и эволюция. Уроки 12, 21–24.
5. Chip Huyen. *Designing Machine Learning Systems* — полный жизненный цикл ML-систем. Уроки 12–20.
6. Майкл Нюгард. *Release It!* — готовность к промышленной эксплуатации. Уроки 15, 20–24.
7. Вигерс, Битти. «Разработка требований к программному обеспечению» — требования и трассировка. Уроки 1–3.
8. Адам Шостак. «Моделирование угроз» — Security by Design. Урок 14.
9. Зхамак Дехгани. *Data Mesh* — архитектура и владение данными. Уроки 12, 25–27.
10. Мэтью Скелтон, Мануэль Пайс. *Team Topologies* — границы команд и закон Конвея. Уроки 4, 10, 29.

## P1 — официальный стартовый список курса

1. Abbott, Fisher — *The Art of Scalability*.
2. Aken — *Composing Datasets for Large Language Models*.
3. Allspaw — *The Art of Capacity Planning*.
4. Arundel, Domingus — *Cloud Native DevOps with Kubernetes*.
5. Hutter, Kotthoff, Vanschoren (eds.) — *Automated Machine Learning*.
6. Bonawitz et al. — *Federated Learning*.
7. Briggs, Scheutz — *The Ethics of Artificial Intelligence*.
8. Burkov — *Machine Learning Engineering*.
9. Dehghani — *Data Mesh*.
10. Indrasiri, Senaratne — *Microservices for the Enterprise, Vol. 2*.
11. Jacobson, Woods, Brail — *APIs: A Strategy Guide*.
12. Janca — *Alice and Bob Learn Application Security*.
13. Jones — *The Tech Lead's Manual*.
14. von Laszewski — *Event-Driven Architecture*.
15. Linthicum — *An Insider's Guide to Multi-Cloud*.
16. Majors, Fong-Jones, Miranda — *Observability Engineering*.
17. Nygard — *Release It!*.
18. Pahl et al. — *Software Architecture: A Comprehensive Framework*.
19. Roberts — *Programming Serverless*.
20. Rosenthal, Jones — *Chaos Engineering*.
21. Tornhill — *Software Design X-Rays*.
22. Storment, Fuller — *Cloud FinOps*.
23. Браун — «Программная архитектура как код».
24. Вейс, Аффало — «Проектирование и создание приложений с LLM».
25. Вигерс, Битти — «Разработка требований к программному обеспечению».
26. Гамма, Хелм, Джонсон, Влиссидес — «Паттерны проектирования».
27. Рассел, Норвиг — «Искусственный интеллект. Современный подход».
28. Форд и др. — «Программная архитектура: трудные решения».
29. Форд и др. — «Эволюционная архитектура».
30. Хоп, Вульф — «Шаблоны интеграции корпоративных приложений».
31. Шостак — «Моделирование угроз».

## P1 — список из урока 4

1. Саймон Браун — «Программная архитектура как код».
2. Марк Ричардс, Нил Форд — «Основы программной архитектуры».
3. Роберт Мартин — «Чистая архитектура».
4. Пол Клементс и др. — «Документирование архитектуры ПО».
5. Gregor Hohpe — *The Software Architect Elevator*.
6. Eóin Woods et al. — *Software Systems Architecture: Working with Stakeholders Using Viewpoints and Perspectives*.

## Дополнения FATHER

1. Eric Evans — *Domain-Driven Design* — модель предметной области и bounded contexts.
2. Vaughn Vernon — *Implementing Domain-Driven Design* — практическая реализация DDD.
3. Nicole Forsgren, Jez Humble, Gene Kim — *Accelerate* — измерение способности поставки.
4. Martin Fowler — *Patterns of Enterprise Application Architecture* — прикладные архитектурные паттерны.
5. Sam Newman — *Building Microservices* — границы сервисов и эволюция.
6. Sam Newman — *Monolith to Microservices* — стратегия миграции.
7. Michael Feathers — *Working Effectively with Legacy Code* — безопасное изменение наследуемых систем.
8. Kelsey Hightower, Brendan Burns, Joe Beda — *Kubernetes: Up & Running* — эксплуатационная основа.
9. Andriy Burkov — *The Hundred-Page Machine Learning Book* — компактная база ML.
10. Lewis Tunstall, Leandro von Werra, Thomas Wolf — *Natural Language Processing with Transformers* — практический NLP/LLM.

## Маршрут чтения по курсу

| Этап | Уроки | Основные книги | Артефакт FATHER |
|---|---:|---|---|
| Требования и стратегия | 1–3 | Вигерс; Ричардс/Форд; Abbott/Fisher | Vision, требования, риски, roadmap |
| HLD и LLD | 4–5 | Браун; Клементс; Мартин; Woods | C1/C2/C3, HLD, границы компонентов |
| AI-паттерны | 6–7 | Вейс/Аффало; Burkov; NLP with Transformers | RAG/Agent pattern catalog |
| Решения и интеграции | 8–11 | Ford; Hohpe; EIP; API Strategy | ADR, integration map, API contracts |
| Данные, качество, безопасность | 12–15 | DDIA; Designing ML Systems; Шостак; Janca | Data architecture, quality gates, threat model |
| Поставка | 16–20 | Capacity Planning; Kubernetes; Observability; Release It! | Sizing, IaC, MLOps, deployment |
| Надёжность и масштаб | 21–27 | Scalability; Chaos Engineering; Data Mesh; Multi-Cloud | HA/DR, EDA, high-load, privacy |
| Экономика и управление | 28–31 | Cloud FinOps; Team Topologies; Evolutionary Architecture | TCO, radar, governance, API product |

## Правило пополнения

Каждая карточка должна содержать: стабильный ID, авторов, название, издание, язык, источник происхождения, официальный URL, темы, уроки, приоритет, статус чтения, конспект, извлечённые правила, связанные решения и проверочные вопросы. Полные тексты защищённых книг в публичный репозиторий не помещаются.
