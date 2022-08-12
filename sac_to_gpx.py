from pyproj import Transformer
import gpxpy
import gpxpy.gpx
import json
import requests
import argparse
import browser_cookie3

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Converts SAC routes to GPX files')
    parser.add_argument('id', metavar='route_id', type=int, help='SAC ID of the route (last part of the URL)')
    parser.add_argument('-lang', type=str, default="de", help="language [de/en/it/fr]")

    args = parser.parse_args()

    cj = browser_cookie3.chrome()
    with requests.get(f"https://www.sac-cas.ch/de/?type=1567765346410&tx_usersaccas2020_sac2020%5BrouteId%5D={args.id}&output_lang={args.lang}", cookies=cj) as url:
        data = json.loads(url.content)

    gpx = gpxpy.gpx.GPX()
    gpx.name = f'{data["destination_poi"]["display_name"]} ({data["title"]})'
    gpx.description = data["teaser"]
    gpx.author_name = data["author"]["full_name"]

    transformer = Transformer.from_crs('epsg:2056', 'epsg:4326')

    for seg in data['segments']:
        gpx_track = gpxpy.gpx.GPXTrack(name=seg['title'],description=seg['description'])
        gpx.tracks.append(gpx_track)
        gpx_segment = gpxpy.gpx.GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)

        if 'geom' in seg and seg['geom']:
            for x,y in map(lambda xy: transformer.transform(*xy),seg['geom']['coordinates']):
                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(x,y))

    wps = [data['departure_point']] + [wp['reference_poi'] for wp in data['waypoints']] + [data['destination_poi']]
    for wp in wps:
        gpx_wp=gpxpy.gpx.GPXWaypoint(*transformer.transform(*wp['geom']['coordinates']),name=wp['display_name'])
        gpx.waypoints.append(gpx_wp)

    with open(f'SAC-{args.id} {gpx.name}.gpx','w') as f:
        f.write(gpx.to_xml())