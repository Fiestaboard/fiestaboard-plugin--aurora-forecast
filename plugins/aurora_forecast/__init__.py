"""Display the current geomagnetic storm (Kp) index and aurora activity forecast."""

from __future__ import annotations

import logging
from typing import Any, Dict, List
import requests

from src.plugins.base import PluginBase, PluginResult

logger = logging.getLogger(__name__)

API_URL = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
USER_AGENT = "FiestaBoard Aurora Forecast Plugin (https://github.com/Fiestaboard/fiestaboard-plugin--aurora-forecast)"


class AuroraForecastPlugin(PluginBase):
    """Aurora Forecast plugin for FiestaBoard."""

    @property
    def plugin_id(self) -> str:
        return "aurora_forecast"

    def fetch_data(self) -> PluginResult:
        try:
            response = requests.get(
                API_URL,
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            response.raise_for_status()
            records = response.json()

            if not records:
                return PluginResult(available=False, error="No Kp data returned")

            # Most recent record
            latest = records[-1]
            kp = float(latest.get("kp_index", 0))

            # Map Kp to activity label
            if kp < 1:
                activity = "Quiet"
            elif kp < 2:
                activity = "Very Quiet"
            elif kp < 3:
                activity = "Unsettled"
            elif kp < 4:
                activity = "Active"
            elif kp < 5:
                activity = "Minor Storm"
            elif kp < 6:
                activity = "Moderate Storm"
            elif kp < 7:
                activity = "Strong Storm"
            elif kp < 8:
                activity = "Severe Storm"
            else:
                activity = "Extreme Storm"

            aurora_visible = "Yes" if kp >= 5 else "No"

            return PluginResult(
                available=True,
                data={
                    "kp_index": round(kp, 2),
                    "activity": activity,
                    "aurora_visible": aurora_visible,
                },
            )
        except Exception as e:
            logger.exception("Error fetching aurora forecast")
            return PluginResult(available=False, error=str(e))

    def validate_config(self, config: Dict[str, Any]) -> List[str]:
        return []

    def cleanup(self) -> None:
        pass
