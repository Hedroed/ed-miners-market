# SQL queries

```sql
select b.commodity_id, b.market_id, c.system, c.station, max(a.sell_price) as max_price, datetime(b.last_ts, 'unixepoch') from commoditiesPrice a, (select commodity_id, market_id, max(timestamp) as last_ts from commoditiesPrice group by commodity_id, market_id having commodity_id = 144) b, markets c where a.commodity_id = b.commodity_id and a.market_id = b.market_id and a.timestamp = b.last_ts and a.market_id = c.id group by b.commodity_id, b.market_id, b.last_ts order by max_price;
```

```sql
select b.commodity_id, b.market_id, c.system, c.station, max(a.sell_price) as max_price, datetime(b.last_ts, 'unixepoch')
from commoditiesPrice a, (
    select commodity_id, market_id, max(timestamp) as last_ts
    from commoditiesPrice
    where timestamp <= 1589025600
    group by commodity_id, market_id having commodity_id = 144
) b,
markets c
where a.commodity_id = b.commodity_id and a.market_id = b.market_id and a.timestamp = b.last_ts and a.market_id = c.id
group by b.commodity_id, b.market_id, b.last_ts
order by max_price;
```

```sql
select *, datetime(timestamp, 'unixepoch') from commoditiesPrice where market_id = 3228369152 and commodity_id=144 order by timestamp;
```

- Strange market:
    + id: 3222955520
    + system: CD-52 557
    + station: Sewell Port

me : 4ec08ece1433ddfc1b61e259e907771cc89709cc

uploader on 3222955520:
    - 1a3920e2fe4f57be8141d71b9eba61f66bb93a61 -> 1139697
    - 1a3920e2fe4f57be8141d71b9eba61f66bb93a61 -> 1139697
    - 8ab9af24f252ae14d4d2a9441df4e9ac7f60cc54 -> 747563
    - 8ab9af24f252ae14d4d2a9441df4e9ac7f60cc54 -> 747563
    - 3520dde5406414e77464b8bb43c8efa8ee3c66c0 -> 1171278
    - 138ae15cd9cacca3a081124a958ae1e01208ab5a -> 1550000

uploader on 128061450:
    - 3b8518fc3a4e4dbb525b2bba5badcc71bbcafa14