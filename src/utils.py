from collections import Counter
from copy import deepcopy

from comment import Comment
from channel import Channel

from typing import List

def aggregate_channels(replies: List[Comment]) -> List[Channel]:
    """
    Return a list of channels sorted by the number of replies made.
    """
    channel_count = Counter([reply.channel for reply in replies])
    return [data[0] for data in channel_count.most_common()]

def aggregate_replies(replies: List[Comment], minimum: int) -> List[Comment]:
    """
    Return a list of replies sorted by frequency that appear at least minimum
    times.
    """
    reply_count = Counter(replies)
    return [data[0] for data in reply_count.most_common()
            if data[1] >= minimum]

def filter_replies(replies: List[Comment], channels: List[Channel],
                   top: int=None, sample: int=None) -> List[Comment]:
    """
    Return a list of replies that are not replies to other comments and were
    made by one of the top channels.
    """
    filtered_replies = []
    filtered_channels = deepcopy(channels)
    for reply in replies:
        if "@" == reply.content[0]:
            if reply.channel in filtered_channels:
                filtered_channels.remove(reply.channel)
        else:
            filtered_replies.append(reply)

    if top is None:
        top = len(filtered_channels)
    result = []
    for channel in filtered_channels[:top]:
        channel_replies = [
            reply for reply in filtered_replies if reply.channel == channel
        ]
        if sample is None:
            sample = len(channel_replies)
        result.extend(channel_replies[:sample])
    return result

def get_top_filtered_replies(replies: List[Comment], n_channels: int=None,
                             minimum: int=1, sample: int=3,
                             duplicates=False) -> List[Comment]:
    """
    Return a list of replies with replies from each of the top
    commenters that appear at least a certain amount of times.

    n_channels: the number of channels to show comments from
    minimum: amount of times a comment must appear to be shown
    sample: the number of comments to show from each channel
    duplicates: show duplicates comments if True
    """
    top_channels = aggregate_channels(replies)
    filtered_replies = filter_replies(replies, top_channels,
                                      top=n_channels, sample=sample)

    top_replies = aggregate_replies(filtered_replies, minimum)
    result = [reply for reply in filtered_replies if reply in top_replies]

    if duplicates:
        return result
    else:
        return list(dict.fromkeys(result))
