workspace "AI RAG Assistant" "Архитектура корпоративного AI-помощника" {

    model {
        # --- Акторы ---
        employee = person "Сотрудник" "Пользователь корпоративной базы знаний"
		
		# [NEW] Специфичные для AI роли
        dataScientist = person "Data Scientist" "Анализирует логи, метрики качества RAG и управляет промптами" {
			tags "Internal_Technical_User" # Тег для технарей
		}
		
        annotator = person "Annotator" "Размечает данные для оценки качества (Golden Set) и валидирует ответы" {
			tags "Internal_Operations_User" # Тег для операционки
		}
		

        # --- Внешние системы ---
        llmProvider = softwareSystem "LLM Provider" "Внешний API для генерации текста (GPT-4)" {
            tags "External System"
        }
        
        knowledgeBase = softwareSystem "Confluence / Jira" "Корпоративный источник знаний" {
            tags "External System"
        }

        # --- Наша система (Boundary) ---
        aiSystem = softwareSystem "Knowledge Base Assistant" "RAG-система: семантический поиск и генерация ответов" {
            tags "Target System"

            # Контейнеры (Детализация Level 2)
            spa = container "SPA / Web App" "Интерфейс чата" "React / TypeScript" {
                tags "Web Browser"
            }
            
            backend = container "API Gateway / Backend" "Оркестрация запросов, управление сессиями" "Python / FastAPI"
            
            llmGateway = container "LLM Gateway" "Абстракция над внешними моделями, ретраи, подсчет токенов" "Python Service"

            vectorDb = container "Vector Database" "Хранение эмбеддингов и семантический поиск" "Milvus / Qdrant [High RAM]" {
                tags "Database" "Hardware_HighMem" # Можно комбинировать теги
            }
			
            # --- Раскрываем Контейнер ETL Worker на Компоненты ---
            etlWorker = container "ETL Worker" "Фоновая обработка документов" "Python [Requires GPU]" {
                
                # Компоненты (Level 3)
                docReader = component "Document Reader" "Читает PDF/Docx из источников" "LangChain / Unstructured"
                
                textSplitter = component "Text Splitter" "Разбивает текст на чанки (Chunking)" "RecursiveCharacterTextSplitter"
                
                embeddingClient = component "Embedding Client" "Отправляет текст в LLM для получения векторов" "OpenAI API Client"
                
                vectorDbClient = component "Vector DB Client" "Сохраняет вектора в базу" "Milvus SDK"

                # Внутренние связи компонентов
                docReader -> textSplitter "Передает сырой текст"
                textSplitter -> embeddingClient "Передает чанки"
                embeddingClient -> vectorDbClient "Передает вектора"
				
				tags "Hardware_GPU" # Специальный тег для GPU
            }
            
            # Внешние связи контейнера можно перепривязать к компонентам (опционально)
            # Например, ETL Worker берет данные из Knowledge Base
            docReader -> knowledgeBase "Скачивает документы" "REST API"
            
            # И пишет в Vector DB (это связь с другим Контейнером)
            vectorDbClient -> vectorDb "Сохраняет эмбеддинги" "gRPC"
			
			
			
        }

        # --- Связи (Relationships) ---
        
        # Уровень 1 (Context) - общие связи
        # Structurizr умеет наследовать связи: если Person связан с Container, то он связан и с System.
        # Но для явности уровня Context иногда их дублируют или полагаются на implied relationships.
        # Здесь мы опишем связи "снизу вверх" (от контейнеров), а на C1 они подтянутся автоматически.

        # 1. User Interaction Flow
        employee -> spa "Открывает чат, пишет вопрос"
        spa -> backend "Отправляет запрос" "HTTPS/JSON"
        backend -> vectorDb "1. Поиск релевантных контекстов" "gRPC"
        backend -> llmGateway "2. Отправка промпта с контекстом" "Internal HTTP"
        llmGateway -> llmProvider "3. Генерация ответа" "External API"

        # 2. Data Ingestion Flow (Async)
        etlWorker -> knowledgeBase "Периодический опрос изменений" "REST API"
        etlWorker -> vectorDb "Обновление векторного индекса" "gRPC"
		
		# [NEW] Связи для AI-команды (Data Scientist & Annotator)
        # Context Level (L1) - автоматически подтянутся, но можно обозначить логику
        dataScientist -> aiSystem "Мониторинг метрик и дообучение"
        annotator -> aiSystem "Разметка данных (Human Feedback)"

        # Container Level (L2) - детализация доступа
        # DS ходит напрямую в базу для инспекции индексов и в ETL для отладки
        dataScientist -> vectorDb "Анализ распределения векторов" "gRPC / SQL"
        dataScientist -> llmGateway "Просмотр трейсов и логов LLM" "Dashboard"
        
        # Аннотатор обычно работает через UI (админку или спец. режим)
        annotator -> spa "Валидация ответов (режим эксперта)"
		
		
		
		
		# === ДОБАВИТЬ ЭТОТ БЛОК ВНУТРЬ MODEL ===
        deploymentEnvironment "Production" {
            
            deploymentNode "User's Device" "Устройство сотрудника" "Microsoft Windows / macOS" {
                deploymentNode "Web Browser" "Google Chrome, Safari, Firefox" {
                    containerInstance spa
                }
            }

            deploymentNode "Corporate Cloud / K8s Cluster" "Корпоративный Kubernetes кластер" "Google GKE / AWS EKS" {
                
                deploymentNode "Services Namespace" "Окружение для синхронных сервисов" {
                    deploymentNode "API Pod" "Replica Set" {
                        containerInstance backend
                    }
                    deploymentNode "LLM Gateway Pod" "Replica Set" {
                        containerInstance llmGateway
                    }
                }

                deploymentNode "Data Processing Namespace" "Окружение для фоновых задач" {
                    deploymentNode "Worker Pod" "High Memory / CPU Node" {
                        containerInstance etlWorker
                    }
                }
            }

            deploymentNode "Data Infrastructure" "Слой хранения данных" {
                deploymentNode "Managed Vector Search" "Managed Milvus / Qdrant Cloud" {
                    containerInstance vectorDb
                }
            }
            
            deploymentNode "External SaaS" {
                softwareSystemInstance llmProvider
                softwareSystemInstance knowledgeBase
            }
        }
    }

    views {
        # --- Диаграмма 1: System Context (Level 1) ---
        systemContext aiSystem "ContextDiagram" {
            include *
            autoLayout lr
            title "C4 Level 1: System Context"
            description "Общая схема взаимодействия пользователя и систем."
        }

        # --- Диаграмма 2: Container View (Level 2) ---
        container aiSystem "ContainerDiagram" {
            include *
            autoLayout lr
            title "C4 Level 2: Containers"
            description "Детализация: контуры Inference и ETL."
        }
		
		
		
		# === ДОБАВИТЬ ЭТОТ БЛОК ВНУТРЬ VIEWS ===
        deployment aiSystem "Production" "DeploymentDiagram" {
            include *
            autoLayout lr
            title "C4 Deployment: Схема развертывания RAG-системы"
            description "Отображает распределение контейнеров по инфраструктуре (K8s + Managed Services)."
        }
		
		# --- НОВАЯ ДИАГРАММА: Component View (Level 3) ---
		component etlWorker "ETL_Components_View" {
			include *
			autoLayout lr
			title "C4 Level 3: Компоненты ETL Worker"
			description "Детализация пайплайна обработки документов."
		}

        # --- Стили (Общие для всех диаграмм) ---
        styles {
            element "Person" {
                shape Person
                background #08427b
                color #ffffff
            }
            element "Target System" {
                background #1168bd
                color #ffffff
            }
            element "External System" {
                background #999999
                color #ffffff
            }
            element "Database" {
                shape Cylinder
            }
            element "Web Browser" {
                shape WebBrowser
            }
			element "Component" {
                background #85bbf0
                color #000000
                shape Component
            }
			
			
			# Стили для Акторов
			element "Internal_Technical_User" {
				background #438dd5
				shape Robot 
				color #ffffff
			}
			
			element "Internal_Operations_User" {
				background #08427b
				shape Person
				color #ffffff
			}

			# Стиль для GPU (выделяем, например, фиолетовым или темным)
			element "Hardware_GPU" {
				background #be93d4 
				shape Component
				icon https://www.shutterstock.com/image-vector/gpu-icon-sign-graphics-card-260nw-1884606295.jpg	
				# Если иконки нет, цвет уже выделит элемент
			}

			# Стиль для High Memory (например, оранжевая обводка или особый фон)
			element "Hardware_HighMem" {
				shape Cylinder
				background #d46a1e 
				icon https://www.shutterstock.com/image-vector/ram-memory-icon-vector-black-260nw-2076753934.jpg
			}
			
        }
    }
}