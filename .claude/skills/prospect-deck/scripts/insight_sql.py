#!/usr/bin/env python3
"""Write the four cheap Athena queries behind a prospect deck's numbers. Aggregates only, never an address.

  probe_<tag>.sql      is the prospect labelled on-chain at all? (research list, ~0.3 GB). Decides direct vs proxy mode.
  benchmark_<tag>.sql  the set's depositors in the window: how many use other venues too, how concentrated the money
                       is, and how many are small here but big elsewhere (the hidden VIPs). One row.
  overlap_<tag>.sql    the other venues the set's depositors fund most, with the money they put there.
  momentum_<tag>.sql   depositors and deposit value per venue, last N days vs the N days before (urgency from our data).

"The set" (--entities) is the prospect's own label in direct mode, or two to five companies like it in proxy mode.
Everything reads apollo.account_to_deposit_address_metadata on its ts_day partition: about 1 to 2 GB each for a
90-day window (measured 16 Nov 2026: benchmark on three casinos, 90 days, 1.2 GB, $0.01, 7 s).

usage:
  insight_sql.py --name Examplex --entities "Roobet,Rainbet.com,Shuffle.com" --sector casino
                 [--days 90] [--end 2026-11-16] [--countries BR,AR] [--small 500] [--big 5000]
                 [--exclude-chains 728126428] [--tag examplex] --out <dir>

--entities   entity_name spellings exactly as the probe returns them, comma-separated
--sector     casino or sportsbook (entity_type 'Gambling Platform'; for a sportsbook choose sports-led brands as the
             set), exchange ('Exchange', 'Regional Exchange') or brokerage (FX and CFD: 'Retail Brokerage' plus both
             exchange types). "Elsewhere" is measured inside the same sector. Prediction markets and perp DEXs are
             contracts, not deposit addresses: use hidden-vip-packs or sales-reports for them (assets/verticals.json)
--countries  ISO2 list: keep only wallets located there (apollo.wallet_locations). Omit for all wallets. Most wallets
             have no country, so a country cut is a smaller, device-linked population: say so on the method slide.
Fix problems here and regenerate; never hand-edit one .sql file.
"""
import argparse, datetime as dt, os, re

SECTORS = {'casino': ["Gambling Platform"], 'sportsbook': ["Gambling Platform"],          # sports-led brands carry the same label
           'exchange': ["Exchange", "Regional Exchange"],
           'brokerage': ["Retail Brokerage", "Exchange", "Regional Exchange"]}          # FX and CFD brokers: proxy on brokerages and exchanges
KNOWN_STARTS = {728126428: ('Tron', dt.date(2026, 11, 3))}     # first ts_day with rows in the deposit table

lst = lambda s: [x.strip() for x in (s or '').split(',') if x.strip()]
q = lambda s: "'" + s.replace("'", "''") + "'"
inl = lambda xs: ', '.join(q(x) for x in xs)
day = lambda d: f"to_unixtime(timestamp '{d.isoformat()} 00:00:00')"

LOC = """loc_raw AS (
  SELECT lower(address) address, primal_country_iso2 c,
         CASE source WHEN 'sdk' THEN 3 WHEN 'matches' THEN 2 ELSE 1 END pr
  FROM apollo.wallet_locations
),
loc AS (SELECT address, max_by(c, pr) country FROM loc_raw GROUP BY address HAVING max_by(c, pr) IN ({cs})),
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--name', required=True, help="the prospect's name, for the probe")
    ap.add_argument('--entities', default='', help='the set: the prospect itself (direct) or companies like it (proxy)')
    ap.add_argument('--sector', choices=sorted(SECTORS), default='casino')
    ap.add_argument('--days', type=int, default=90)
    ap.add_argument('--end', default=dt.date.today().isoformat(), help='window end, exclusive (YYYY-MM-DD)')
    ap.add_argument('--countries', default='')
    ap.add_argument('--small', type=int, default=500, help='"small here": deposits to the set under this, USD')
    ap.add_argument('--big', type=int, default=5000, help='"big elsewhere": deposits to other venues of at least this, USD')
    ap.add_argument('--momentum-days', type=int, default=30)
    ap.add_argument('--exclude-chains', default='')
    ap.add_argument('--tag', default='')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()

    ents, cs = lst(a.entities), [c.upper() for c in lst(a.countries)]
    end = dt.date.fromisoformat(a.end)
    start = end - dt.timedelta(days=a.days)
    m1, m0 = end - dt.timedelta(days=a.momentum_days), end - dt.timedelta(days=2 * a.momentum_days)
    xch = [int(x) for x in lst(a.exclude_chains)]
    for cid, (nm, first) in KNOWN_STARTS.items():
        if cid not in xch and min(start, m0) < first < end:
            print(f'WARNING: {nm} (chain {cid}) has no rows before {first}, inside these windows. Momentum would show a fake '
                  f'rise and the benchmark would mix two populations. Regenerate with --exclude-chains {cid} and say on the '
                  f'method slide which chains are compared.')
    tag = a.tag or re.sub(r'[^a-z0-9]+', '-', a.name.lower()).strip('-')
    types = inl(SECTORS[a.sector])
    base = f"NOT d.is_depositor_entity AND d.entity_type IN ({types})"
    if xch:
        base += f" AND cardinality(filter(d.chain_ids, x -> x IN ({', '.join(map(str, xch))}))) = 0"
    loc = LOC.format(cs=inl(cs)) if cs else ''
    join_loc = 'JOIN loc l ON l.address = d.depositor' if cs else ''
    scope = f"{', '.join(ents) or '(set --entities)'}; {a.sector}; {start} .. {end - dt.timedelta(days=1)}; countries {', '.join(cs) or 'all'}"

    needle = re.sub(r'[^a-z0-9]', '', re.split(r'[\s.]', a.name.strip().lower())[0])
    match = (f"regexp_replace(lower(entity_name), '[^a-z0-9]', '') LIKE '%{needle}%'" if len(needle) >= 3
             else f"regexp_replace(lower(split_part(entity_name, '.', 1)), '[^a-z0-9]', '') = '{needle}'")
    probe = f"""-- probe: is "{a.name}" labelled on-chain? Rows = yes (direct mode, after the user confirms the match). No rows = proxy mode.
-- The names stay in chat. Never say how many entities the list holds.
SELECT entity_name, entity_type, sector, count(*) deposit_addresses
FROM research.deposit_address_name
WHERE entity_name IS NOT NULL AND {match}
GROUP BY 1, 2, 3 ORDER BY 4 DESC LIMIT 10
"""

    d_cte = f"""d AS (   -- one row per wallet and venue in the window
  SELECT d.depositor w, d.entity_name ex, sum(d.amount_usd) usd
  FROM apollo.account_to_deposit_address_metadata d
  {join_loc}
  WHERE {base}
    AND d.ts_day >= {day(start)} AND d.ts_day < {day(end)}
  GROUP BY 1, 2
),
setw AS (SELECT w, sum(least(usd, 1e7)) usd_set FROM d WHERE ex IN ({inl(ents)}) GROUP BY 1),
allw AS (SELECT w, count(*) n_all, sum(least(usd, 1e7)) usd_all FROM d GROUP BY 1)"""

    bench = f"""-- benchmark: {scope}
-- One row. Each wallet's deposits capped at $10M per venue. "Elsewhere" = other {a.sector} venues, same window.
--   users                     depositors of the set
--   multi_venue_users         of them, also funded at least one other venue
--   hidden_vips               under ${a.small:,} at the set and ${a.big:,}+ elsewhere
--   usd_top1pct / usd_set     share of the set's deposits that comes from its top 1% of depositors
--   median_else_hidden        median deposited elsewhere by a hidden VIP
WITH {loc}{d_cte},
j AS (
  SELECT s.w, s.usd_set, a.n_all, a.usd_all - s.usd_set usd_else, ntile(100) OVER (ORDER BY s.usd_set DESC) pct
  FROM setw s JOIN allw a ON a.w = s.w
)
SELECT count(*) users,
       count_if(n_all >= 2) multi_venue_users,
       count_if(usd_set < {a.small} AND usd_else >= {a.big}) hidden_vips,
       round(sum(usd_set)) usd_set,
       round(sum(usd_else)) usd_elsewhere,
       round(sum(usd_set) FILTER (WHERE pct = 1)) usd_top1pct,
       round(approx_percentile(usd_else, 0.5) FILTER (WHERE usd_set < {a.small} AND usd_else >= {a.big})) median_else_hidden,
       round(sum(usd_else) FILTER (WHERE usd_set < {a.small} AND usd_else >= {a.big})) usd_else_hidden
FROM j LIMIT 1
"""

    overlap = f"""-- overlap: {scope}
-- The other venues the set's depositors fund, by shared depositors. Rows under 3 people are dropped.
-- Before a venue is named on a slide: check it is not an Addressable client (HubSpot); if it is, ask the user first.
WITH {loc}{d_cte}
SELECT d.ex other_venue, count(*) shared_users, round(sum(least(d.usd, 1e7))) usd_there,
       round(approx_percentile(d.usd, 0.5)) median_usd_there
FROM d JOIN setw s ON s.w = d.w
WHERE d.ex NOT IN ({inl(ents)})
GROUP BY 1 HAVING count(*) >= 3
ORDER BY 2 DESC LIMIT 12
"""

    momentum = f"""-- momentum: last {a.momentum_days} days ({m1} .. {end - dt.timedelta(days=1)}) vs the {a.momentum_days} before ({m0} .. {m1 - dt.timedelta(days=1)}); {a.sector}; countries {', '.join(cs) or 'all'}
-- Per venue: depositors and deposit value in each window. in_set marks the set. Top 25 by recent depositors, at least 3 each.
-- A partial last day or a chain that starts mid-window fakes a trend: check dates and --exclude-chains before quoting.
WITH {loc}d AS (
  SELECT d.entity_name ex, d.depositor w, d.ts_day >= {day(m1)} recent, sum(d.amount_usd) usd
  FROM apollo.account_to_deposit_address_metadata d
  {join_loc}
  WHERE {base}
    AND d.ts_day >= {day(m0)} AND d.ts_day < {day(end)}
  GROUP BY 1, 2, 3
)
SELECT ex, ex IN ({inl(ents)}) in_set,
       count_if(NOT recent) depositors_before, count_if(recent) depositors_recent,
       round(sum(least(usd, 1e7)) FILTER (WHERE NOT recent)) usd_before,
       round(sum(least(usd, 1e7)) FILTER (WHERE recent)) usd_recent
FROM d GROUP BY 1, 2 HAVING count_if(recent) >= 3 AND count_if(NOT recent) >= 3
ORDER BY 4 DESC LIMIT 25
"""

    os.makedirs(a.out, exist_ok=True)
    files = [(f'probe_{tag}.sql', probe)]
    if ents:
        files += [(f'benchmark_{tag}.sql', bench), (f'overlap_{tag}.sql', overlap), (f'momentum_{tag}.sql', momentum)]
    else:
        print('no --entities yet: wrote the probe only. Run it, pick the set, then rerun with --entities.')
    for name, sql in files:
        p = os.path.join(a.out, name)
        open(p, 'w').write(sql)
        print('wrote', p)


if __name__ == '__main__':
    main()
