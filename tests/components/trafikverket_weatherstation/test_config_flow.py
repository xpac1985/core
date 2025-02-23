"""Test the Trafikverket weatherstation config flow."""
from __future__ import annotations

from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_MONITORED_CONDITIONS, CONF_NAME
from homeassistant.core import HomeAssistant

DOMAIN = "trafikverket_weatherstation"
CONF_STATION = "station"


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["errors"] == {}

    with patch(
        "homeassistant.components.trafikverket_weatherstation.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {
                CONF_NAME: "Vallby Vasteras",
                CONF_API_KEY: "1234567890",
                CONF_STATION: "Vallby",
                CONF_MONITORED_CONDITIONS: ["air_temp", "road_temp"],
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == "create_entry"
    assert result2["title"] == "Vallby Vasteras"
    assert result2["data"] == {
        "name": "Vallby Vasteras",
        "api_key": "1234567890",
        "station": "Vallby",
        "monitored_conditions": ["air_temp", "road_temp"],
    }
    assert len(mock_setup_entry.mock_calls) == 1


async def test_import_flow_success(hass: HomeAssistant) -> None:
    """Test a successful import of yaml."""

    with patch(
        "homeassistant.components.trafikverket_weatherstation.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        result2 = await hass.config_entries.flow.async_init(
            DOMAIN,
            context={"source": config_entries.SOURCE_IMPORT},
            data={
                CONF_NAME: "Vallby Vasteras",
                CONF_API_KEY: "1234567890",
                CONF_STATION: "Vallby",
                CONF_MONITORED_CONDITIONS: ["air_temp", "road_temp"],
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] == "create_entry"
    assert result2["title"] == "Vallby Vasteras"
    assert result2["data"] == {
        "name": "Vallby Vasteras",
        "api_key": "1234567890",
        "station": "Vallby",
        "monitored_conditions": ["air_temp", "road_temp"],
    }
    assert len(mock_setup_entry.mock_calls) == 1
