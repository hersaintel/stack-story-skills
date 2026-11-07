"""Install this pack without replacing existing skills. No dependencies installed."""
import argparse
import os
import pathlib
import shutil
import tempfile

NAMES = ('stack-diagram', 'stack-video')


def install(source: pathlib.Path, target: pathlib.Path, names: list) -> list:
    """Stage complete copies then promote; rollback this process's promotions on error.

    Refuses symlink targets and existing names. Not a crash-safe transaction or a
    defense against concurrent filesystem writers; install in a quiescent profile.
    """
    if not names or len(set(names)) != len(names) or any(name not in NAMES for name in names):
        raise ValueError('select stack-diagram, stack-video, or both once each')
    source, target = pathlib.Path(source), pathlib.Path(target).absolute()
    if any(part.is_symlink() for part in (target, *target.parents)):
        raise ValueError('skills destination and its parents must not be symlinks')
    for name in names:
        destination = target / name
        if destination.exists() or destination.is_symlink():
            raise FileExistsError(f'refusing to overwrite {destination}')
        directory = source / name
        if not (directory / 'SKILL.md').is_file():
            raise ValueError(f'incomplete source skill: {name}')
        if any(path.is_symlink() for path in directory.rglob('*')):
            raise ValueError(f'source skill contains symlinks: {name}')
    target.mkdir(parents=True, exist_ok=True)
    installed = []
    with tempfile.TemporaryDirectory(prefix='.stack-story-', dir=target) as tmp:
        stage = pathlib.Path(tmp)
        try:
            for name in names:
                shutil.copytree(source / name, stage / name, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            for name in names:
                destination = target / name
                # mkdir is exclusive, even if another installer creates the name.
                destination.mkdir()
                installed.append(destination)
                for child in (stage / name).iterdir():
                    child.rename(destination / child.name)
        except BaseException:
            for directory in reversed(installed):
                shutil.rmtree(directory)
            raise
    return installed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skills-dir', type=pathlib.Path, default=pathlib.Path(os.environ.get('HERMES_HOME', pathlib.Path.home() / '.hermes')) / 'skills')
    parser.add_argument('--skill', choices=NAMES, help='omitted installs both')
    args = parser.parse_args()
    try:
        paths = install(pathlib.Path(__file__).resolve().parents[1] / 'skills', args.skills_dir, [args.skill] if args.skill else list(NAMES))
        for path in paths:
            print(f'Installed {path.name}: {path}')
        print('Start a new Hermes session to refresh the skill catalog.')
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == '__main__':
    main()
