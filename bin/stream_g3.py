#!/usr/bin/env python3

USAGE="""
SDDataSource demo tool.

Invoke as
    ./sd_demo.py config

Then run lyrebird:
    ./lyrebird sd_demo.json

Then start the data stream:
    ./sd_demo.py stream

"""

import optparse as o
o = o.OptionParser(usage=USAGE)
o.add_option('--num-pix', type=int, default=1024)
opts, args = o.parse_args()

from spt3g import core
import numpy as np
import time




counter = 0

N_CHROIC = 2
N_POL = 2
N_COLOC = N_CHROIC * N_POL
n = opts.num_pix * N_COLOC
idx = np.arange(n)
pi, di = idx // N_COLOC, idx % N_COLOC   #pixel index, coloc index.
x = np.array(pi % 32) * 1.
y = np.array(pi // 32) * 1.
ci, ri = di//2, di%2  # color idx, rot idx
rot = (((pi % 32 % 2)^(pi // 32 % 2)) + 2*ri) * np.pi/4

cname = ['test_%04i' % i for i in idx]
equations = ['/ + 1 s %s 2' % _c for _c in cname]
cmaps = [["red_cmap","bolo_blue_cmap"][_ci] for _ci in ci]

tplates = ['template_c%i_p0' % _ci for _ci in ci]

data = np.zeros(n)

# network_sender = core.G3NetworkSender(hostname='localhost', port=8675, max_queue_size=1000)

# Load up the data description.
f = core.G3Frame()
f.type = core.G3FrameType.Scan
f['x'] = core.G3VectorDouble(x)
f['y'] = core.G3VectorDouble(y)
f['rotation'] = core.G3VectorDouble(rot)
f['cname'] = core.G3VectorString(cname)
f['equations'] = core.G3VectorString(equations)
f['cmaps'] = core.G3VectorString(cmaps)
f['templates'] = core.G3VectorString(tplates)
# network_sender(f)

stream_rate = 90 # [Hz]

class Pacer:
    def __init__(self):
        pass

    def __call__(self, frame):
        time.sleep(frame['duration'])
        return frame


def formatG3(frame):
    if frame.type == core.G3FrameType.Housekeeping:
        return []

    ts = frame['data']['0']
    elapsed = (ts.stop.time - ts.start.time) / core.G3Units.sec
    sample_rate = ts.sample_rate * core.G3Units.sec
    num_frames = int(len(ts) // sample_rate * stream_rate)

    data = np.zeros((num_frames, n))
    for i in range(len(data)):
        # Timestream split into n even parts
        chunks = np.array_split(frame['data'][str(i)], num_frames)
        for j, chunk in enumerate(chunks):
            data[j][i] = np.average(chunk)

    out_frames = [core.G3Frame(core.G3FrameType.Scan) for _ in range(num_frames)]
    for i, f in enumerate(out_frames):
        f['duration'] = elapsed / num_frames
        f['data'] = core.G3VectorDouble(data[i])

    out_frames[0]['first'] = 1

    return out_frames


pipe = core.G3Pipeline()
# pipe.Add(gen)
pipe.Add(core.G3Reader, filename='tcp://localhost:4536')
pipe.Add(formatG3)
pipe.Add(Pacer)
pipe.Add(core.Dump)
# pipe.Add(network_sender)
pipe.Run(profile=True)