"""Conditional campaign economics. Dollars follow the source; no observed profit."""
from dataclasses import dataclass, asdict, replace
import math
import pandas as pd
from src.config import ARMS

@dataclass(frozen=True)
class Assumptions:
    audience: int | None = None
    margin: float | None = None
    delivery_cost: float | None = None
    fixed_cost: float | None = None
    multiplier: float | None = 1.0

    def validate(self):
        for name, value in asdict(self).items():
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError(f'{name} must be finite numeric or missing')
            maximum = 1 if name in ('margin', 'multiplier') else 1e12
            if not 0 <= value <= maximum:
                raise ValueError(f'{name} must be between 0 and {maximum:g}')
            if name == 'audience' and int(value) != value:
                raise ValueError('audience must be a whole number')
        return [name for name, value in asdict(self).items() if value is None]

OUTPUTS = ['effective_uplift','revenue','gross_contribution','variable_cost','total_cost',
           'net_value','net_low','net_high','break_even_uplift','break_even_margin',
           'max_delivery_cost','net_return_on_cost']

def evaluate(effect, low, high, assumptions, treatment="Men's email"):
    missing = assumptions.validate()
    if treatment not in ARMS:
        raise ValueError('Unknown treatment')
    if any(not math.isfinite(x) for x in [effect, low, high]) or low > high:
        raise ValueError('Require finite effect and ordered interval')
    result = {'treatment':treatment, **asdict(assumptions), 'source_effect':effect,
              'source_low':low,'source_high':high,'assumption_basis':'hypothetical',
              **dict.fromkeys(OUTPUTS), 'classification':'missing assumptions',
              'missing':', '.join(missing)}
    if treatment == 'Control':
        result.update(dict.fromkeys(OUTPUTS, 0.0))
        for key in ['break_even_uplift','break_even_margin','max_delivery_cost','net_return_on_cost']:
            result[key] = None
        result.update(source_effect=0.,source_low=0.,source_high=0.,classification='incremental baseline',missing='')
        return result
    if missing:
        return result
    n,m,c,f,k = (assumptions.audience, assumptions.margin, assumptions.delivery_cost,
                 assumptions.fixed_cost, assumptions.multiplier)
    uplift = effect*k
    revenue = n*uplift
    variable = n*c
    costs = variable+f  # Fixed setup is incurred even when audience is zero.
    contribution = revenue*m
    net = contribution-costs
    result.update(effective_uplift=uplift,revenue=revenue,gross_contribution=contribution,
                  variable_cost=variable,total_cost=costs,net_value=net,
                  net_low=n*k*m*low-costs,net_high=n*k*m*high-costs,
                  break_even_uplift=costs/(n*m) if n*m>0 else None,
                  break_even_margin=costs/revenue if revenue>0 else None,
                  max_delivery_cost=uplift*m-f/n if n>0 else None,
                  net_return_on_cost=net/costs if costs>0 else None,
                  classification='break-even' if abs(net)<=1e-9 else ('favorable' if net>0 else 'unfavorable'))
    return result

def compare(revenue_table, assumptions):
    """Both email interventions versus no-email under the same commercial assumptions."""
    required = revenue_table.loc[revenue_table.reference=='Control']
    if len(required)!=2 or set(required.treatment)!=set(ARMS[1:]):
        raise ValueError('Require exactly one contrast versus control per email')
    rows=[evaluate(0.,0.,0.,assumptions,'Control')]
    for arm in ARMS[1:]:
        r=required.loc[required.treatment==arm].iloc[0]
        rows.append(evaluate(float(r.effect),float(r.ci_low),float(r.ci_high),assumptions,arm))
    return pd.DataFrame(rows)

def sensitivity(revenue_table, assumptions):
    if assumptions.validate():
        return pd.DataFrame()
    grids={'margin':[0,.1,.2,.3,.4,.5,.75,1],
           'delivery_cost':[0,.02,.05,.1,.2,.3,.5,1],
           'audience':[0,1000,5000,10000,25000,50000,100000]}
    frames=[]
    for driver, values in grids.items():
        for value in sorted(set(values+[getattr(assumptions,driver)])):
            frame=compare(revenue_table,replace(assumptions,**{driver:value}))
            frame['driver']=driver;frame['driver_value']=value;frames.append(frame)
    return pd.DataFrame([row for frame in frames for row in frame.to_dict('records')])

DEMO = Assumptions(audience=10000,margin=.4,delivery_cost=.05,fixed_cost=500.,multiplier=1.)
