# 19 · MLOps

## Задача этапа

Dataset/knowledge change → validation → retrain/reindex → eval → registry → release trigger.

## Вход

Утверждённые артефакты этапа 18.

## Что делаем

1. Фиксируем решение в versioned artifacts.
2. Связываем требования, риски, решения и evidence.
3. Не объявляем M2/M3 без проверяемого evidence.
4. Передаём результат следующему этапу через явный контракт.

## Выход

`MLOPS_PIPELINE.md · MODEL_REGISTRY.md`

## Связь со сквозным проектом

Проект один: **Secure AI Knowledge Assistant**. На этом уроке не создаётся новая демонстрационная система; расширяется уже существующая архитектура.

## Status

`DESIGN / M1` до появления runtime/evidence, если отдельный артефакт не доказывает более высокий уровень.
