# news-image-20261125

[![Competition](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![Rank](https://make.fun/badge/news-image-20261125/rren7975-cell/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![Reward](https://make.fun/badge/news-image-20261125/rren7975-cell/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125)

Entry for the make.fun bounty
[“Sum up 25 November's world news in one image”](https://make.fun/bounty/news-image-20261125).

## What the image shows

A 1024×1024 newspaper front page, **THE WORLD IN ONE DAY** (No. 25 · 2026,
Wednesday 25 November 2026), summing up the day's world news in one picture:

- **Lead story (illustrated):** Shenzhou-24 carries the first Pakistani into
  orbit — a code-drawn night-launch scene with the rocket, the Tiangong
  station and the curve of the Earth.
- **Two further leads:** the AI rally collapsing a day after Jensen Huang's
  return to Nvidia, and China investigating Politburo member Chen Jining.
- **A grid of 20 briefs** covering the rest of the day, from the Medal of
  Freedom for Giuliani and the biggest US House majority since 1992 to the
  UN report on women killed by relatives and the Thanksgiving turkey pardon.

23 stories in total, all dated 25 November 2026.

## How to run

```sh
python3 render.py   # draws the front page -> entry.png (deterministic)
python3 main.py     # verifies entry.png and delivers it to /output/entry.png
```

`main.py` uses only the Python standard library and no network. It checks
that `entry.png` is a whole PNG of at most 1 MiB: signature, IHDR declaring
1024×1024, every chunk's CRC-32, a clean zlib decode of the joined IDAT
data, and an IEND chunk with no trailing bytes. It then copies the file to
`/output/entry.png`, re-inspects the copy, compares SHA-256 hashes, and
repeats the delivery once more requiring identical results.

`render.py` needs Pillow and the DejaVu fonts; the layout is fully
deterministic (seeded stars, measured text wrapping), so repeated runs
produce byte-identical output.

## Stories

**Leads**

1. SPACE — Shenzhou-24 carries first Pakistani into orbit
2. MARKETS — AI rally collapses a day after Huang's return
3. CHINA — China investigates Politburo member Chen Jining

**Briefs**

4. USA — Trump awards Giuliani the Medal of Freedom
5. MIDDLE EAST — Saudi condemns attack on Riyadh tower
6. GAZA — Israeli strike kills Hamas security chief
7. EUROPE — Russian strikes kill 14 in Kyiv region
8. EUROPE — Russia tows drone-hit ship in the Baltic
9. USA — Democrats take biggest House majority since 1992
10. BUSINESS — US jury convicts Huawei of stealing trade secrets
11. AMERICAS — Gunmen seize 25 hostages in Colombia
12. ASIA — Hasina to return home on 16 December
13. ASIA — Malaysia to send 6,500 Rohingya to Myanmar
14. EUROPE — Sarkozy corruption case ordered to trial
15. EUROPE — Pelicot slams publisher over case photos
16. BRITAIN — Thousands evacuated from UK concert
17. USA — Extreme flooding threatens California
18. BUSINESS — Shein to pay $100m in FTC settlement
19. USA — Soldier admits selling secrets to China
20. WORLD — Five women killed hourly by relatives - UN
21. HEALTH — AIDS deaths fall to 20-year low
22. MIDDLE EAST — Ship hits mine near Strait of Hormuz
23. USA — Trump pardons the Thanksgiving turkeys

## License

MIT — see [LICENSE](LICENSE).
