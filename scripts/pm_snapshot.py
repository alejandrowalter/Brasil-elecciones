#!/usr/bin/env python3
"""Copia de Polymarket para la página (solo librería estándar).

Descarga lo mismo que usa el panel Polymarket de index.html y lo guarda en pm.json,
para que la página pueda leerlo desde su propio dominio cuando el navegador no
alcanza a gamma-api / clob.polymarket.com (p. ej. bloqueo del operador en Colombia).

Uso:  python3 scripts/pm_snapshot.py [salida]     (por defecto ./pm.json)
"""
import json, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone

GAMMA = 'https://gamma-api.polymarket.com'
CLOB = 'https://clob.polymarket.com'
PRES = 'brazil-presidential-election'
MARGIN = 'brazil-presidential-election-second-round-margin-of-victory'
GOV = {
    'ac': 'acre-governor-election-winner',
    'am': 'amazonas-governor-election-winner',
    'df': 'federal-district-governor-election-winner',
    'es': 'espirito-santo-governor-election-winner-20260611183840001',
    'rn': 'rio-grande-do-norte-governor-election-winner',
    'to': 'tocantins-governor-election-winner',
}
EV_KEYS = ('slug', 'title', 'volume', 'volume24hr', 'liquidity', 'endDate')
MK_KEYS = ('groupItemTitle', 'question', 'slug', 'clobTokenIds', 'closed', 'active', 'volume',
           'liquidity', 'bestBid', 'bestAsk', 'lastTradePrice', 'outcomePrices')
UA = {'User-Agent': 'brasil-elecciones-pm-snapshot/1.0', 'Accept': 'application/json'}


def get(url, data=None, tries=3):
    body = json.dumps(data).encode() if data is not None else None
    hdr = dict(UA, **({'Content-Type': 'application/json'} if body else {}))
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=body, headers=hdr, method='POST' if body else 'GET')
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.load(r)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            if i == tries - 1:
                raise RuntimeError(f'{url.split("?")[0]}: {e}')
            time.sleep(2 * (i + 1))


def tok0(m):
    try:
        return json.loads(m.get('clobTokenIds') or '[]')[0]
    except (ValueError, IndexError):
        return None


def main(out='pm.json'):
    slugs = [PRES, MARGIN, *GOV.values()]
    evs = get(f'{GAMMA}/events?' + '&'.join('slug=' + s for s in slugs) + f'&_={int(time.time())}')
    events = []
    for e in evs:
        mk = [{k: m.get(k) for k in MK_KEYS} for m in e.get('markets', []) if not m.get('closed') and m.get('active')]
        events.append(dict({k: e.get(k) for k in EV_KEYS}, markets=mk))
    found = {e['slug'] for e in events}
    missing = [s for s in slugs if s not in found]
    if PRES not in found:
        raise SystemExit('Gamma no devolvió el mercado presidencial')

    tok = {}
    for m in next(e for e in events if e['slug'] == PRES)['markets']:
        g = (m.get('groupItemTitle') or '').upper()
        if 'FL' in g and 'BOLSONARO' in g:
            tok['F'] = tok0(m)
        elif 'LULA' in g:
            tok['L'] = tok0(m)
    if not tok.get('F') or not tok.get('L'):
        raise SystemExit(f'No encontré los tokens de Flávio/Lula: {tok}')

    toks = list(dict.fromkeys([tok['F'], tok['L']] + [tok0(m) for e in events if e['slug'] != PRES for m in e['markets']]))
    toks = [t for t in toks if t]
    payload = [{'token_id': t} for t in toks]
    mids = get(f'{CLOB}/midpoints', payload)
    lasts = get(f'{CLOB}/last-trades-prices', payload)
    history = {k: get(f'{CLOB}/prices-history?market={tok[k]}&interval=1d&fidelity=5').get('history', []) for k in ('F', 'L')}

    snap = {
        'generated_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'source': 'gamma-api.polymarket.com + clob.polymarket.com',
        'tok': tok,
        'events': events,
        'mids': mids,
        'lasts': lasts,
        'history': history,
        'missing_slugs': missing,
    }
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(snap, f, ensure_ascii=False, separators=(',', ':'))
    print(f'ok {out}: {len(events)} eventos, {len(toks)} tokens, {len(mids)} midpoints, '
          f'{len(lasts)} últimos trades, historial F={len(history["F"])} L={len(history["L"])}, '
          f'Flávio={mids.get(tok["F"])} Lula={mids.get(tok["L"])}' + (f', faltan {missing}' if missing else ''))


if __name__ == '__main__':
    main(*sys.argv[1:2])
