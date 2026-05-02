# Aurora Forecast Setup Guide

Display the current geomagnetic storm (Kp) index and aurora activity forecast.

## Overview

The Aurora Forecast plugin queries NOAA's Space Weather Prediction Center (SWPC) for the current planetary Kp index, which indicates geomagnetic activity. A Kp of 5+ means aurora may be visible at mid-latitudes. No API key required.

- API reference: https://www.swpc.noaa.gov/products/planetary-k-index

### Prerequisites

No API key or account required.

## Quick Setup

1. **Enable** — Go to **Integrations** in your FiestaBoard settings and enable **Aurora Forecast**.
2. **Configure** — Fill in the plugin settings (see Configuration Reference below).
3. **Template** — Add a page using the `aurora_forecast` plugin variables:
   ```
   {{{ aurora_forecast.status }}}
   ```
4. **View** — Navigate to your board page to see the live display.

## Template Variables

| Variable | Description | Example |
|---|---|---|
| `aurora_forecast.kp_index` | Current Kp index (0-9) | `3.67` |
| `aurora_forecast.activity` | Activity level description | `Quiet` |
| `aurora_forecast.aurora_visible` | Yes if aurora likely visible at mid-latitudes | `No` |

## Configuration Reference

| Setting | Name | Description | Default |
|---|---|---|---|
| `enabled` | Enabled |  | `False` |
| `refresh_seconds` | Refresh Interval (seconds) | How often to fetch aurora data. | `300` |

## Troubleshooting

- **No data** — verify connectivity to `services.swpc.noaa.gov`.
- **Stale Kp** — SWPC updates every 1 minute; refresh interval of 5 min is fine.

