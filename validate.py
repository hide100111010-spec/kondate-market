"""market.json が献立コックピットで読める形かを確認する（スケジュール実行時に使う）"""
import json, sys, datetime

STAPLE = ['卵','米','鶏むね肉','鶏もも肉','豚こま・豚肉','牛肉','ひき肉','牛乳・ヨーグルト','豆腐・納豆','もやし','食用油','パン・麺・小麦粉']
SEASONAL = ['キャベツ','白菜','レタス','トマト','きゅうり','玉ねぎ','にんじん','じゃがいも','大根','ほうれん草・小松菜','ブロッコリー','きのこ類','サバ・アジなど青魚','鮭','ブリ・タラなど旬の魚']
LEVELS = {'高い','やや高い','平年並み','やや安い','安い'}
TRENDS = {'上昇','横ばい','下落'}

def main(path='market.json'):
    d = json.load(open(path, encoding='utf-8'))
    errs = []
    for k in ['version','fetchedAt','asOf','summary','newsAlerts','watchlist','bestValueVegetables','bestValueSeafood','highPriceAlerts','stapleStrategy','sources']:
        if k not in d: errs.append(f'missing key: {k}')
    try:
        t = datetime.datetime.fromisoformat(d['fetchedAt'])
        age = (datetime.datetime.now(t.tzinfo) - t).total_seconds() / 86400
        if age > 1: errs.append(f'fetchedAt is {age:.1f} days old (should be now)')
    except Exception as e:
        errs.append(f'bad fetchedAt: {e}')
    items = {w.get('item') for w in d.get('watchlist', [])}
    for it in STAPLE + SEASONAL:
        if it not in items: errs.append(f'watchlist missing item: {it}')
    for w in d.get('watchlist', []):
        if w.get('level') not in LEVELS: errs.append(f"bad level for {w.get('item')}: {w.get('level')}")
        if w.get('trend') not in TRENDS: errs.append(f"bad trend for {w.get('item')}: {w.get('trend')}")
        if w.get('item') in STAPLE and w.get('category') != '定番': errs.append(f"category should be 定番: {w.get('item')}")
        if not w.get('source'): errs.append(f"missing source: {w.get('item')}")
    if not d.get('bestValueVegetables') and not d.get('bestValueSeafood'): errs.append('bestValue lists are empty')
    for s in d.get('sources', []):
        if not str(s.get('uri','')).startswith('http'): errs.append(f'bad source uri: {s}')
    if errs:
        print('NG'); print('\n'.join(errs)); sys.exit(1)
    print(f"OK: watchlist {len(d['watchlist'])}, news {len(d['newsAlerts'])}, sources {len(d['sources'])}")

if __name__ == '__main__':
    main(*sys.argv[1:])
