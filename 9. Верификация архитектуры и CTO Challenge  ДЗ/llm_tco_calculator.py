"""Сценарный расчёт месячной стоимости LLM-инфраструктуры."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ApiScenario:
    requests: int
    input_tokens_per_request: int
    output_tokens_per_request: int
    input_rate_per_million: float
    output_rate_per_million: float

    def monthly_cost(self) -> float:
        input_cost = (
            self.requests
            * self.input_tokens_per_request
            * self.input_rate_per_million
            / 1_000_000
        )
        output_cost = (
            self.requests
            * self.output_tokens_per_request
            * self.output_rate_per_million
            / 1_000_000
        )
        return input_cost + output_cost


@dataclass(frozen=True)
class OnPremScenario:
    capex: float
    lifetime_months: int
    power_kw: float
    hours_per_month: float
    electricity_rate_per_kwh: float
    pue: float
    operations_and_maintenance: float
    utilization: float

    def monthly_cost(self) -> float:
        depreciation = self.capex / self.lifetime_months
        electricity = (
            self.power_kw
            * self.hours_per_month
            * self.electricity_rate_per_kwh
            * self.pue
        )
        return depreciation + electricity + self.operations_and_maintenance

    def effective_gpu_hour(self) -> float:
        useful_hours = self.hours_per_month * self.utilization
        if useful_hours <= 0:
            raise ValueError("utilization должна быть больше нуля")
        return self.monthly_cost() / useful_hours


def break_even_months(capex: float, external_monthly: float, onprem_opex: float):
    monthly_saving = external_monthly - onprem_opex
    return None if monthly_saving <= 0 else capex / monthly_saving


if __name__ == "__main__":
    api = ApiScenario(100_000, 2_000, 500, 2.0, 8.0)
    onprem = OnPremScenario(5_000, 36, 0.45, 730, 0.15, 1.2, 150, 0.6)

    print(f"API/month: {api.monthly_cost():.2f}")
    print(f"On-prem/month: {onprem.monthly_cost():.2f}")
    print(f"Effective GPU-hour: {onprem.effective_gpu_hour():.2f}")
