import dlt

from spotify_pipeline import (
    spotify_album_data,
    spotify_artist_data,
    spotify_top_tracks_in_kenya,
    spotify_track_metrics_data,
)

pipeline = dlt.pipeline(
    pipeline_name="spotify_pipeline",
    destination="duckdb",
    dataset_name="spotify_data",
    dev_mode=True,
)

load_info = pipeline.run(
    [
        spotify_artist_data("Simmy"),
        spotify_album_data("Simmy"),
        spotify_track_metrics_data("Simmy"),
        spotify_top_tracks_in_kenya("Simmy"),
    ],
    write_disposition="replace",
)

print(load_info)
