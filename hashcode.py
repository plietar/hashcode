from collections import defaultdict

[V, E, R, C, X] = map(int, raw_input().split())
VIDEOS = map(int, raw_input().split())
ENDPOINTS = []
REQUESTS = []
CACHES = defaultdict(lambda: set())
CACHE_CAPACITY = defaultdict(lambda: X)
BEST_CACHE_CACHE = defaultdict(lambda: None)

for i in range(E):
    [ld, k] = map(int, raw_input().split())
    e = (ld, dict())

    for j in range(k):
        [c, lc] = map(int, raw_input().split())
        e[1][c] = lc

    ENDPOINTS.append(e)

for i in range(R):
    REQUESTS.append(tuple(map(int, raw_input().split())))

def video_endpoint_cost(video, endpoint):
    if endpoint[1]:
        for (cache, latency) in endpoint[1].items():
            if video in CACHES[cache]:
                return latency
        else:
            return endpoint[0]
    else:
        return 0

def request_cost(r):
    return video_endpoint_cost(r[0], ENDPOINTS[r[1]]) * r[2]

vids = defaultdict(lambda: [0, []])
for r in REQUESTS:
    vids[r[0]][0] += request_cost(r)
    vids[r[0]][1].append(r)

def how_much_can_we_improve(video):
    video_index = video[0]
    video_size = VIDEOS[video_index]

    if BEST_CACHE_CACHE[video_index] is not None:
        best_cache = BEST_CACHE_CACHE[video_index]
        if video_size <= CACHE_CAPACITY[best_cache[0]]:
            return (best_cache[1], best_cache[0], video)

    requests = video[1][1]

    saved_time = defaultdict(lambda: 0)
    for r in requests:
        caches = ENDPOINTS[r[1]][1]
        latency = ENDPOINTS[r[1]][0]
        current_cost = min([c[1] for c in caches.items() if video[0] in CACHES[c[0]]] + [latency])

        for cache in caches.items():
            space_left = CACHE_CAPACITY[cache[0]]

            if video_size < space_left:
                if current_cost - cache[1] > 0:
                    saved_time[cache[0]] += (current_cost - cache[1]) * r[2]

    if not saved_time:
        del vids[video[0]]
        return (0, None, video)

    best_cache = sorted(saved_time.items(), key=lambda x: x[1], reverse=True)[0]

    # (time saved, cache, video)
    BEST_CACHE_CACHE[video_index] = best_cache
    return (best_cache[1], best_cache[0], video)

while vids:
    # Good for data 2 only
    # lambda x: x[0] / 
    (time_saved, cache, video) = max(map(how_much_can_we_improve, vids.items()), key=lambda x: VIDEOS[x[2][0]])
    if cache is None:
        continue

    video_index = video[0]
    video_size = VIDEOS[video_index]

    CACHES[cache].add(video_index)
    CACHE_CAPACITY[cache] -= video_size
    BEST_CACHE_CACHE[video_index] = None
    video[1][0] -= time_saved

#print "-----------------------"
#print CACHE_CAPACITY
print len(filter(lambda (c, v): v, CACHES.items()))
for cache, videos in CACHES.items():
    if videos:
        print cache, " ".join(map(str, list(videos)))
