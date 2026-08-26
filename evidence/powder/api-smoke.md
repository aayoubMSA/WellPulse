# POWDER early-window availability search

- Checked UTC: 2026-08-26T09:51:08Z
- WellPulse SHA: be2b5cec71d722f07dad8c473ceee454da13d3a7
- Request: `nuc1 x1 + nuc2 x1`, Emulab, project `WellPulse`
- Resource mutation attempted: **NONE**
- 3-hour search exit: `0`
- 2-hour search exit: `0`
- Token content recorded: **NO**

## 3-hour result

```json
{
  "expires_at": "2026-08-27T19:00:00+00:00",
  "start_at": "2026-08-27T16:00:00+00:00"
}
```

## 2-hour result

```json
{
  "expires_at": "2026-08-27T18:00:00+00:00",
  "start_at": "2026-08-27T16:00:00+00:00"
}
```

## CLI search help

```text
[1m                                                                                [0m
[1m [0m[1;33mUsage: [0m[1mportal-cli resgroup search_raw [OPTIONS][0m[1m                               [0m[1m [0m
[1m                                                                                [0m
 Search for a free time slot where a resgroup can be scheduled                  
                                                                                
[2m╭─[0m[2m Options [0m[2m───────────────────────────────────────────────────────────────────[0m[2m─╮[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-duration[0m        [1;33mINTEGER       [0m  Number of hours the reservation group   [2m│[0m
[2m│[0m                                      is requesting                           [2m│[0m
[2m│[0m                                      [2;31m[required]                             [0m [2m│[0m
[2m│[0m [31m*[0m  [1;36m-[0m[1;36m-body[0m            [1;33mRESGROUPSEARCH[0m  A cloudlab reservation group search     [2m│[0m
[2m│[0m                                      request                                 [2m│[0m
[2m│[0m                                      [2;31m[required]                             [0m [2m│[0m
[2m│[0m    [1;36m-[0m[1;36m-help[0m            [1;33m              [0m  Show this message and exit.             [2m│[0m
[2m╰──────────────────────────────────────────────────────────────────────────────╯[0m


```
