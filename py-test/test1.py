import pafy


def main():
    url = "https://youtu.be/4eJJUlCHcKg"
    video = pafy.new(url)
    print(video.title)
    print(video.rating)
    print(video.viewcount, video.author, video.length)
    print(video.description)
    streams = video.streams
    for s in streams:
        print(s)
    for s in streams:
        print(s.resolution, s.extension, s.get_filesize(), s.url)
    best = video.getbest()
    print(best.resolution, best.extension)
    print(best.url)
    # best.download(quit=false)
    # filename = best.download(filepath="/tmp/")
    # filename = best.download(filepath="/tmp/Game." + best.extension)
    audiostreams = video.audiostreams
    for a in audiostreams:
        print(a.bitrate, a.extension, a.get_filesize())
    # audiostreams[1].download()
    bestaudio = video.getbestaudio()
    print(bestaudio.bitrate)
    # bestaudio.download()
    allstreams = video.allstreams
    for s in allstreams:
        print(s.mediatype, s.extension, s.quality)


main()
