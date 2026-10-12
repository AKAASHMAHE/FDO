def fake_google_maps_baseline(**kwargs):
    return {
        "functions": [
            {
                "function_name": "Turn-by-turn navigation",
                "description": "Provide navigation and routing functionality.",
                "expected_data": [
                    {
                        "data_type": "DATA.LOCATION.PRECISE",
                        "necessity": "REQUIRED",
                        "purpose": "Route/navigation",
                        "justification": (
                            "Precise location is needed to provide "
                            "turn-by-turn navigation."
                        ),
                        "confidence": 0.90,
                    }
                ],
            }
        ]
    }