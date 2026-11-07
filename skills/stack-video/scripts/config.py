"""Resolve stack-video configuration. This does not render or generate audio."""
import argparse
import json
import math
import pathlib

DEFAULTS = dict(format='landscape', duration=30, theme='dark', tone='explanatory', music='off', voice=False)


def resolve_config(project: dict, overrides: dict) -> dict:
    """Merge explicit overrides > project values > defaults; reject invalid inputs."""
    for label, source in [('project', project), ('overrides', overrides)]:
        if not isinstance(source, dict):
            raise ValueError(f'{label} configuration must be a JSON object')
        unknown = set(source) - set(DEFAULTS)
        if unknown:
            raise ValueError(f'unknown {label} keys: {", ".join(sorted(unknown))}')
    config = {**DEFAULTS, **project, **overrides}
    for key, values in [('format', ('landscape', 'vertical', 'square')), ('theme', ('light', 'dark'))]:
        if config[key] not in values:
            raise ValueError(f'{key} must be one of {", ".join(values)}')
    duration = config['duration']
    if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or not 10 <= duration <= 120:
        raise ValueError('duration must be a finite number from 10 to 120 seconds')
    if type(config['voice']) is not bool:
        raise ValueError('voice must be a JSON boolean')
    if not isinstance(config['tone'], str) or not config['tone'].strip():
        raise ValueError('tone must be a non-empty string')
    music = config['music']
    if not isinstance(music, str) or not music:
        raise ValueError('music must be "off" or an existing local audio file path')
    if music != 'off' and not pathlib.Path(music).is_file():
        raise ValueError(f'music file not found: {music}')
    return config


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=pathlib.Path, help='project JSON; omitted means defaults')
    parser.add_argument('--format', choices=['landscape', 'vertical', 'square'])
    parser.add_argument('--duration', type=float)
    parser.add_argument('--theme', choices=['light', 'dark'])
    parser.add_argument('--tone')
    parser.add_argument('--music', help='off or local file path (CLI paths relative to working directory)')
    voice = parser.add_mutually_exclusive_group()
    voice.add_argument('--voice', action='store_true', default=None)
    voice.add_argument('--no-voice', dest='voice', action='store_false')
    args = parser.parse_args()
    try:
        project = json.loads(args.config.read_text(encoding='utf-8')) if args.config else {}
        if isinstance(project, dict) and isinstance(project.get('music'), str) and project['music'] != 'off':
            project['music'] = str((args.config.resolve().parent / project['music']).resolve())
        overrides = {key: getattr(args, key) for key in DEFAULTS if getattr(args, key) is not None}
        if overrides.get('music') not in (None, 'off'):
            overrides['music'] = str(pathlib.Path(overrides['music']).resolve())
        print(json.dumps(resolve_config(project, overrides), indent=2, allow_nan=False))
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
