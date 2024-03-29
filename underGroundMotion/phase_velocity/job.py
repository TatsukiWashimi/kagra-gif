body = '''
Universe       = vanilla 
GetEnv         = True
Initialdir     = /home/kouseki.miyo/kagra-gif/underGroundMotion/phase_velocity
Notification   = Never
+Group         = "Xc"
request_memory = 1 GB

Executable = /usr/bin/python 
Error      = ./log/main.$(Process).err
Log        = ./log/main.$(Process).log
Output     = ./log/main.$(Process).out
'''

queue = '''
RequestCpus    = 2
Arguments  = ./main.py --start {0} --end {1} --nproc 2
Queue
'''

jobs = 32
tlen = 2**25
bins = tlen/jobs
segments = zip(range(1211817600     ,1245372032+1,bins),
               range(1211817600+bins,1245372032+1,bins))

text = body
for start,end in segments:
    body += queue.format(start,end)

with open('main_multi.job','w') as f:
    f.write(body)
