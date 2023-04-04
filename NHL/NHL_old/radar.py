import asyncio
from env_canada import ECRadar

radar_coords = ECRadar(coordinates=(50, -100))

# Conditions Available
animated_gif = asyncio.run(radar_coords.get_loop())
latest_png = asyncio.run(radar_coords.get_latest_frame())