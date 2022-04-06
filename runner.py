import os
import sys



sort_directory=sys.argv[1]
output_file = sys.argv[2]
sort_type=sys.argv[3]
files_to_run= sys.argv[4]

if files_to_run == 'f':
    logfiles=['1.log',
    '2.log',
    '4.log',
    '8.log',
    '16.log',
    '32.log',
    '64.log',
    '128.log',
    '256.log',
    '512.log',
    '1024.log',
    '2048.log',
    '4096.log',
    '8192.log',
    '16384.log',
    '32768.log',
    '65536.log',
    '131072.log',
    '262144.log',
    '524288.log',
    '1048576.log',
    '2097152.log',
    '4194304.log']

else:
    logfiles=['1.log',
    '2.log',
    '4.log',
    '8.log',
    '16.log',
    '32.log',
    '64.log',
    '128.log',
    '256.log',
    '512.log',
    '1024.log',
    '2048.log',
    '4096.log',
    '8192.log',
    '16384.log',
    '32768.log',
    '65536.log',]



dir = f'/root/csc505-spring-2022/Project1/{sort_directory}'

for subdir, dirs, files in os.walk(dir):
    files.sort(key=lambda x: int(os.path.splitext(x)[0]))
    for file in files:
        if(file in logfiles):
    #WARMUP RUNS      
            for i in range(3):
                print(file)
                f = open(f'/root/505p1/output/OfficialRuns/{output_file}', "a")
               # f.write("WARMUP_RUN,")
                f.close()
                os.system(f'python3 /root/505p1/main.py ~/csc505-spring-2022/Project1/{sort_directory}/{file} /root/505p1/output/2048supertesting1.log {sort_type} c >> /root/505p1/output/OfficialRuns/{output_file}')
    #ACTUAL RUNS
            for i in range(10):
                print(file)
                f = open(f'/root/505p1/output/OfficialRuns/{output_file}', "a")
               # f.write("ACTUAL_RUN,")
                f.close()
                os.system(f'python3 /root/505p1/main.py ~/csc505-spring-2022/Project1/{sort_directory}/{file} /root/505p1/output/2048supertesting1.log {sort_type} c >> /root/505p1/output/OfficialRuns/{output_file}')







