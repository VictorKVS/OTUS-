# SADEQ Kubernetes — Twelve-Factor Architecture Baseline v0.1
**Дата:** 2026-11-27 · **Статус:** PROPOSED / NOT_DEPLOYED / NOT_QUALIFIED.

## Метод
Оригинальная [The Twelve-Factor App](https://12factor.net/) состоит из 12 факторов приложения, а **не** встроенных 12 правил Kubernetes. Обеспечиваем соответствие с явными проектными контрактами. Применяем к двум продуктовым контурам: SADEQ Engineering Platform и UAA Runtime.

## Исходные требования
1. Итоговый OTUS MVP — **strict air-gapped on-prem** без внешних model APIs; все модели, образы, пакеты локальны.
2. Kubernetes в OTUS — масштабируемый вариант внедрения, а не требование запускать многосервисный K8s на одной RTX 3060. Для первой демонстрации Compose и локальные DB допустимы, но контракты должны быть Kubernetes-compatible.
3. Изоляция безопасности пользователя и арендатора не делегируется LLM. Допуск не self-approved.
4. UAA agent process stateless; sessions, event store, graph, checkpoints, audit, idempotency, tool execution outcomes must persist outside Pods.
5. Схемы и manifests — проектная документация, без подтверждения запуска.

## Пакет
- [Архитектурная матрица 12 факторов](01_TWELVE_FACTOR_MAPPING.md)
- [C4 / Deployment / Sizing / K8s services](02_KUBERNETES_ARCHITECTURE.md)
- [Дорожная карта реализации и квалификационные ворота](03_IMPLEMENTATION_ROADMAP_AND_TESTS.md)
- [ADR: Twelve Factor и границы AI workload](04_ADR_TWELVE_FACTOR.md)
- [Mermaid схема](diagram.mmd)
- [Концептуальные Kubernetes-манифесты](manifests/namespace-and-api.yaml)

## Первоисточники
- https://12factor.net/
- https://kubernetes.io/docs/concepts/configuration/
- https://kubernetes.io/docs/concepts/security/
- https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
- https://kubernetes.io/docs/concepts/storage/persistent-volumes/
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/

## Внимание
Образ `registry.internal/sadeq/api:0.1.0` и его хэш в примере не существуют как подтверждённый артефакт. Манифесты **не должны применяться в production**, пока не настроены сетевой plugin с поддержкой NetworkPolicy, проверка изображений по digest, secrets management, backed databases, service account permissions, реальные readiness/liveness probes и policies на egress. 
