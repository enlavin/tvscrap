import re


RX_EPISODE = re.compile(u'(?P<episode_name>S[0-9]{2}E[0-9]{2})')
RX_EPISODE_ALT = re.compile(u'(?P<episode_name>[0-9]{1,2}x[0-9]{1,2})')


class InvalidEpisodeName(Exception):
    pass


def get_episode_number(name):
    try:
        # SxxEyy numbering scheme
        episode_name = RX_EPISODE.findall(name)[0]
    except IndexError:
        try:
            # SxEE numbering scheme
            episode_name = RX_EPISODE_ALT.findall(name)[0]
            # Normalizes episode numbering to SxxEyy
            episode_name_parts = episode_name.split('x')
            episode_name = 'S%02dE%02d' % tuple(int(n) for n in episode_name_parts[:2])
        except IndexError:
            raise InvalidEpisodeName(episode_name)
    return episode_name
